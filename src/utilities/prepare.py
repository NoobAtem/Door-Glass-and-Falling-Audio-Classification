"""
    This used for data preperation for the model
    that is found useful for the entire project
"""

import librosa
import numpy as np
import logging
import os

logging: object = logging.getLogger("src.utilities.prepare")

def sliding_window(audio: np.array, sr: int, window_duration: float = 5.0, hop_duration: float = 1.0) -> list:
    # Convert duration to samples
    window_size: int = int(sr * window_duration)
    hop_size: int = int(sr * hop_duration)
    
    # Calculate the number of windows
    num_windows: int = (len(audio) - window_size) // hop_size + 1
    
    windows: list = []
    for i in range(num_windows):
        start: int = i * hop_size
        end: int = start + window_size
        window: np.array = audio[start:end]
        windows.append(window)
    
    return windows

def generate_segmented_audio(filepath: str) -> list:
    # Load your audio file
    logging.info("Generating audio file")
    audio, sr = librosa.load(filepath, sr=None)
    filename: str = filepath.split("/")[-1].split(".")[0]
    folderpath: str = os.path.join(filepath.split("/")[:-1])
    logging.debug(f"Folder Path: {folderpath}")
    
    # Apply sliding window
    windows: list = sliding_window(audio, sr, window_duration=5.0, hop_duration=1.0)
    
    # Save or process each window as neede
    file_list: str = []
    for i, window in enumerate(windows):
        output: str = os.path.join(folderpath, f'{filepath}-{i}.wav')
        librosa.output.write_wav(output, window, sr)
        file_list.append(output)
        logging.debug(f"Generate the first segment: {output}")
        
    os.remove(filepath)
    logging.info("Finished segmenting")
