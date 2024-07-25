"""
    Handling all of the preprocessing utilities that is
    essential step for generating the training and validation
    set

    By Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import matplotlib
import matplotlib.pyploy as plt
import librosa
import librosa.display
import src.utilities.view as view
import src.utilities.system as system
import numpy as np
import logging
import math

matplotlib.style.use("dark_background")

logging: object = logging.getLogger("src.preprocessing.audio")

class AudioPreprocess:
    def __init__(self):
        self.config: dict = system.read_yaml(os.path.join("configs", "preprocess_config.yaml"))
        self.monitor: object = view.AudioDataSource()
        self.raw_audio: dict = self.load_audio()

    def load_audio(self) -> dict:
        logging.info(f"Loading audio files from")
        return {aud: librosa.load(aud) for aud in self.monitor.getRawAudio()}
        
    def add_noise(self, y: dict) -> list:
        logging.info(f"Adding noise to audio")
        
        noisy_audio: list = []
        for aud in y:
            signal: np.array = np.interp(aud, (aud.min(), aud.max()), (-1, 1))
            noise: np.array = getWhiteNoise(signal, snr=self.config["snr"])

            # In case that the two signal and noise do not match in size
            if(len(noise)>len(signal)):
                noise = noise[0:len(signal)]

            noise = getNoiseFromSound(audio, noise, snr=self.config["snr"])
            noisy_audio: list = signal + noise

    @staticmethod
    def getNoiseFromSound(audio: np.array, noise:np.array, snr: float) -> np.array:
        rms_signal: np.array = math.sqrt(np.mean(audio**2))
        #required RMS of noise
        rms_noise: np.array = math.sqrt(rms_signal**2/(pow(10,snr/10)))
        
        #current RMS of noise
        rms_noise_curr: np.array = math.sqrt(np.mean(noise**2))
        noise: np.array = noise * (rms_noise/rms_noise_current)
        
        return noise
        
    @staticmethod
    def signalToNoiseRatio(audio: np.array, noise: np.array) -> np.array:
        logging.debug(f"Audio {audio}, Noise: {noise}")
        rms_signal: np.array = librosa.feature.rms(audio)
        rms_noise: np.array = librosa.feature.rms(noise)
        return 20*math.log(rms_signal/rms_noise, 10)

    @staticmethod
    # Additive White Gaussian Noise
    def getWhiteNoise(audio: np.array, snr: float) -> np.array:
        logging.debug(f"Audio {audio}, SNR: {snr}")
        rms_signal: np.array = librosa.feature.rms(audio)
        rms_noise: np.array = math.sqr(rms_signal**2/(pow(10, snr/10)))
        std_n = rms_noise
        noise: np.array = np.random.normal(0, std_n, audio.shape[0])
        return noise

def process_audio_file() -> None:
    audio_prep: object = AudioPreprocess()
    
def entry() -> None
    logging.info("==== Audio Preprocessing ====")
    process_audio_file()
    logging.info("==== End of Audio Preprocessing ====")