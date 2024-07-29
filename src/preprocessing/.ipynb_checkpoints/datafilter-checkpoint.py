"""
    All standard filtering tools will be defined
    hear. Spectograms, and feature extraction
    is not included in this file

    By Dimaunahan, Isiah Jordan (NoobAtem)
"""
import os
import librosa
import src.utilities.view as view
import src.utilities.system as system
import numpy as np
import logging
import math
import warnings
warnings.filterwarnings("ignore")

logging: object = logging.getLogger("src.preprocessing.datafilter")

class AudioFilter:
    def __init__(self):
        self.config: dict = system.read_yaml(os.path.join("configs", "preprocess_config.yaml"))
        self.monitor: object = view.AudioDataSource()
        self.raw_audio: dict = self.loadAudio() # Live a copy of the original source
        self.process_audio: dict = self.raw_audio # Modify this instead
        
        logging.info("Checking configuration")
        if self.config["noise"]["status"]:
            self.process_audio = self.addNoise(self.process_audio)
        if self.config["segment"]["status"]:
            self.process_audio = self.segmentAudio(self.process_audio)
        if self.config["augmented"]["status"]:
            self.process_audio = self.augmentAudio(self.process_audio)

        logging.info(len(self.getSegmentedFile(self.process_audio)))
    
    def loadAudio(self) -> dict:
        _data: dict = {}
        for aud in self.monitor.getRawAudio():
            _audio, _sr = librosa.load(aud, mono=True)
            _data[system.get_filename(aud)] = {"audio": _audio, "rate": _sr}
        return _data
        
    def addNoise(self, y: dict) -> dict:
        logging.info("Adding noise to audio")

        audio_w_noise: dict = {}
        for key, aud in y.items():
            signal: np.array = np.interp(aud["audio"], (aud["audio"].min(), aud["audio"].max()), (-1, 1))
            noise: np.array = self.getWhiteNoise(signal, snr=self.config["noise"]["snr"])

            # In case that the two signal and noise do not match in size
            if(len(noise)>len(signal)):
                noise = noise[0:len(signal)]

            noise = self.getNoiseFromSound(signal, noise, snr=self.config["noise"]["snr"])
            audio_w_noise[key] = {"audio": signal + noise, "rate": y[key]["rate"]}

        return audio_w_noise

    def augmentAudio(self, y: dict) -> dict:
        logging.info("Adding augmentation to data")
        augmented_audio: dict = {}
        for key, val in y.items():
            audio_filter: np.array = self.timeShift(val["audio"], val["rate"], self.config["augmented"]["shift"]["step"])            
            audio_filter = self.timeStretch(audio_filter, self.config["augmented"]["stretch"]["factor"])
            audio_filter = self.pitchShift(audio_filter, val["rate"], self.config["augmented"]["shift"]["nsteps"])
            augmented_audio[key] = {"audio": audio_filter, "rate": val["rate"]}
        return augmented_audio
    
    def segmentAudio(self, y: dict) -> dict:
        logging.info("Segmenting and overlapping the audio")
        segmented_audio: dict = {}
        for key, val in y.items():
            if librosa.get_duration(y=val["audio"], sr=val["rate"]) > 5.0:
                _segment_audio: list = self.segmentOverlapAudio(val["audio"], val["rate"], 
                                         self.config["segment"]["duration"], self.config["segment"]["overlap"])
                for i in range(len(_segment_audio)):
                    segmented_audio[key + "-segmented" + str(i)] = _segment_audio[i]
            else:
                segmented_audio[key] = val
        return segmented_audio

    def getSegmentedFile(self, y:dict) -> dict:
        segmented_filename: dict = {}
        for key, val in y.items():
            if "segmented" in key.split("-"):
                segmented_filename[key] = val

        return segmented_filename
        
    @staticmethod
    def getNoiseFromSound(audio: np.array, noise:np.array, snr: float) -> np.array:
        rms_signal: np.array = AudioFilter.RMS(audio)
        #required RMS of noise
        rms_noise: np.array = math.sqrt(rms_signal**2/(pow(10,snr/10)))
        
        #current RMS of noise
        rms_noise_curr: np.array = AudioFilter.RMS(noise)
        noise: np.array = noise * (rms_noise/rms_noise_curr)
        
        return noise
        
    @staticmethod
    def signalToNoiseRatio(audio: np.array, noise: np.array) -> np.array:
        rms_signal: np.array = AudioFilter.RMS(audio)
        rms_noise: np.array = AudioFilter.RMS(noise)
        return 20*math.log(rms_signal/rms_noise, 10)

    @staticmethod
    # Additive White Gaussian Noise
    def getWhiteNoise(audio: np.array, snr: float) -> np.array:
        rms_signal: np.array = AudioFilter.RMS(audio)
        rms_noise: np.array = math.sqrt(rms_signal**2/(pow(10, snr/10)))
        std_n = rms_noise
        noise: np.array = np.random.normal(0, std_n, audio.shape[0])
        return noise

    @staticmethod
    def RMS(signal: np.array) -> np.array:
        return math.sqrt(np.mean(signal**2))

    @staticmethod
    def segmentOverlapAudio(audio: np.array, sr: int, duration: int = 500, overlap: int = 100) -> list:
        segment: int = int(sr *  duration/ 1000)
        overlap_segment: int = int(sr * overlap / 1000)
        segments: list = []
        start: int = 0
        while start < len(audio):
            end: int = start + segment
            segments.append(audio[start:end])
            start += segment - overlap_segment
    
        return segments

    @staticmethod
    def timeShift(audio: np.array, sr: int, step: int) -> np.array:
        return np.roll(audio, int(sr/step))

    @staticmethod
    def timeStretch(audio: np.array, factor: float) -> np.array:
        return librosa.effects.time_stretch(y=audio, rate=factor)

    @staticmethod
    def pitchShift(audio: np.array, sr: int, step: int) -> np.array:
        if step == 0:
            return audio
        step = int(sr/step)
        return librosa.effects.pitch_shift(audio, sr=sr, n_steps=step)

