"""
    Handling all of the preprocessing utilities that is
    essential step for generating the training and validation
    set

    By Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import src.utilities.view as view
import src.utilities.system as system
import numpy as np
import logging
from src.preprocessing.datafilter import AudioFilter
from src.preprocessing.feature import AudioFeature
import warnings
warnings.filterwarnings("ignore")

logging: object = logging.getLogger("src.preprocessing.audio")
    
def process_audio_file() -> None:
    audio_prep: object = AudioFilter()
    audio_feat: object = AudioFeature(audio_prep.process_audio)
    
def entry() -> None:
    logging.info("==== Audio Preprocessing ====")
    process_audio_file()
    logging.info("==== End of Audio Preprocessing ====")