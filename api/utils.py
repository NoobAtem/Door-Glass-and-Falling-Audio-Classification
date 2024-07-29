import yaml
import os
import librosa
import numpy as np

def read_yaml(filepath: str) -> dict:
    with open(filepath, "r") as yml:
        return yaml.safe_load(yml)
    return None
