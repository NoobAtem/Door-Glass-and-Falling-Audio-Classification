"""
    Feature extraction for audio after
    passing in through DataFilter

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
import pandas as pd
import soundfile as sf
import src.utilities.view as view
import src.utilities.system as system
import numpy as np
import logging
import math
from IPython.display import display
import warnings
warnings.filterwarnings("ignore")
matplotlib.style.use("dark_background")

logging: object = logging.getLogger("src.preprocessing.feature")

class AudioFeature:
    """
        This handles the convertion
        from audio to spectogram or
        any usuable feature that I
        can include to my training
    """

    def __init__(self, audio: dict) -> None:
        """
            audio
            - filename: {audio, sr}
        """
        self.config = system.read_yaml(os.path.join("configs", "preprocess_config.yaml"))
        logging.info("Feature extraction")
        self.raw_audio: dict = audio # Live a copy of the original source
        self.process_audio: dict = self.raw_audio # Modify this instead

        self.initialize_intrim()

    def initialize_intrim(self) -> None:
        self.image_p: str = os.path.join(self.config["process"]["path"], "image")
        self.audio_p: str = os.path.join(self.config["process"]["path"], "audio")
        if system.is_not_a_path(self.image_p):
            os.mkdir(self.image_p)
        if system.is_not_a_path(self.audio_p):
            os.mkdir(self.audio_p)

        self.feature_csv: pd.DataFrame = pd.DataFrame(self.raw_audio.keys(), columns=["filename"])
        
        self.extractToCSV()
        self.extractToImage()
        self.generateTargetCSV()
        self.saveAudio()

    def saveAudio(self):
        logging.info("Saving processed audio")
        for key, val in self.process_audio.items():
            output: str = os.path.join(self.audio_p, key + ".wav")
            sf.write(output, val["audio"], val["rate"])
        
    def extractToImage(self):
        logging.info("Creating image features")
        if self.config["features"]["image"]:
            self.generateSpectogramImage(self.image_p)

    def generateSpectogramImage(self, destination: str) -> None:
        logging.info("Generating a spectogram image")
        if not os.path.exists(destination):
            logging.info("Created a directory")
            os.mkdir(destination)
        for key, val in self.process_audio.items():
            x = val["audio"]
            sr = val["rate"]
            x = librosa.stft(x)
            Xdb = librosa.amplitude_to_db(abs(x))
            plt.figure(figsize=(14, 5))
            librosa.display.specshow(Xdb, sr=sr)
            # Remove grid
            plt.xlabel("")
            plt.ylabel("")
            plt.title("")
            plt.grid(False)
            plt.yticks([])
            plt.xticks([])
            plt.legend([])
            plt.savefig(os.path.join(destination, key+".png"), bbox_inches="tight")

    def generateTargetCSV(self):
        if self.config["target"]["for_image"]:
            for file in os.listdir(self.image_p):
                print(file)
    
    def extractToCSV(self):
        logging.info("Creating CSV feature")
        if self.config["features"]["csv"]:
            self.createCSVFeature(self.feature_csv)
            display(self.feature_csv)

            filepath: str = os.path.join(self.config["process"]["path"], "feature.csv")
            self.feature_csv.to_csv(filepath, index=False)
        
    def createCSVFeature(self, dataset: pd.DataFrame) -> None:
        logging.info("Creating a process dataset")
        n_samples = dataset['filename'].shape[0]
        dataset['zero_crossing_rate'] = np.zeros(n_samples)
        dataset['chroma_stft'] = np.zeros(n_samples)
        dataset['rmse'] = np.zeros(n_samples)
        dataset['spectral_centroid'] = np.zeros(n_samples)
        dataset['spectral_bandwidth'] = np.zeros(n_samples)
        dataset['beat_per_minute'] = np.zeros(n_samples)
        dataset['rolloff'] = np.zeros(n_samples)
        for i in range(0, 20):
            dataset[f'mfcc_{i}'] = np.zeros((n_samples,))
    
        for i in range(n_samples):
            y = self.process_audio[dataset["filename"].iloc[i]]["audio"]
            sr = self.process_audio[dataset["filename"].iloc[i]]["rate"]
            dataset['rmse'][i] = np.mean(librosa.feature.rms(y=y))
            dataset['chroma_stft'][i] = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
            dataset['spectral_centroid'][i] = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            dataset['spectral_bandwidth'][i] = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
            dataset['rolloff'][i] = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            dataset['zero_crossing_rate'][i] = np.mean(librosa.feature.zero_crossing_rate(y))
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            dataset['beat_per_minute'][i] = tempo
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            for e in range(0, 20):
                dataset[f'mfcc_{e}'][i] = np.mean(mfcc[e])

            