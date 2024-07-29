"""
    This file objective is to manage all
    plotting and saving to png form.

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
import src.utilities.view as view
import src.utilities.system as system
import numpy as np
import logging
import math
matplotlib.style.use("dark_background")

logging: object = logging.getLogger("src.preprocessing.graph")

class AudioImage:
    """
        Plotting, saving, and viewing audio
        images in many formats
    """
    def __init__(self) -> None:
        self.config: dict = system.read_yaml(os.path.join("configs", "preprocess_config.yaml"))

    def saveForm(self, filename) -> None:
        folder_path: str = self.config["unprocess"]["display"]["path"]
        
        if system.is_not_a_path(folder_path):
            logging.info("Creating folder")
            os.mkdir(folder_path)

        logging.info("Saving audio wave form")
        _save: str =  folder_path + filename.lower().replace(" ", "-") + ".png"
        plt.savefig(_save)
        
    def plotWaveForm(self, audio: np.array, sr: int, title: str, is_save: bool = False) -> None:
        logging.info("Plotting Waveform")
        librosa.display.waveshow(audio, sr=sr)
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        
        if is_save:
            self.saveForm(title)
        else:
            logging.info("Plotting waveform")
            plt.show()
        