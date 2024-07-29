"""
    From the modeling.ipynb, we now convert it into a 
    custom model.

    by Dimaunahan, Isiah Jordan
"""

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow.keras as keras
import os
from tensorflow.keras.models import load_model
import numpy as np
import joblib
import datetime
import librosa
import logging
import src.utilities.system as system
import warnings
warnings.filterwarnings("ignore")

logging: object = logging.getLogger("src.model.yamnet")

class YamnetClassifier(tf.keras.Model):
    """
        This is the model that the model
        handler will initialize and use
    """
    def __init__(self) -> None:
        super(YamnetClassifier, self).__init__()
        logging.info("Loading a YAMNet classifier")
        self.config: dict = system.read_yaml(os.path.join("configs", "model_config.yaml"))
        self.yt_model: object = hub.load("https://tfhub.dev/google/yamnet/1")
        self.cfr_model: object = load_model(self.config["yamnet"]["model"][0])
    
    def get_config(self):
        return {"config_path": self.config["yamnet"]["model"][0]}
        
    @classmethod
    def from_config(cls, config):
        instance = cls()
        instance.cfr_model = keras.models.load_model(config["config_path"])
        return instance

    def call(self, inputs: np.array) -> np.array:
        # Extract embeddings
        #inputs = tf.reshape(inputs, [-1])
        _, embeddings, _ = self.yt_model(inputs)
        # Pass embeddings to the classifier
        embeddings = np.expand_dims(embeddings, axis=0)
        outputs: np.array = self.cfr_model(embeddings)
        return outputs
    
    def save(self, filepath: str = None, **kwargs) -> None:
        if filepath is None:
            flags = self.config["flags"]
            now = datetime.datetime.now().strftime("%m-%d-%Y")
            filename = f"{now}-{str(flags['ESC50_DATA'] | flags['RAW_DOOR_1_DATA'])}-10"
            filepath = os.path.join("src", "weights", filename + '.keras')
        self.cfr_model.save(filepath, **kwargs)
        super(YamnetClassifier, self).save(os.path.join("src", "weights", 'yamnet_classifier.keras'), **kwargs)
        
    @classmethod
    def load(cls, filepath: str):
        instance = cls()
        instance.cfr_model = keras.models.load_model(filepath)
        return instance

class ModelHandler:
    """
        Purpose of this class is
        to abstract the required process
        to use the models
    """
    def __init__(self):
        logging.info("Model handler initialize")
        self.model: object = YamnetClassifier()
        self.encoder = joblib.load(os.path.join("src", "weights", "label_encoder.joblib"))
        logging.debug(f"Encoder {self.encoder.classes_}")
        
    def predict(self, path: str) -> str:
        logging.info("Predicting")
        if system.is_not_a_path(path):
            logging.error(f"Not a valid path: {path}")
            return None
        target_audio, sr = librosa.load(path, sr=16000)  # Load audio at 16 kHz
        #target_audio = librosa.util.fix_length(target_audio, size=80000)  # Fix length to 80000 samples
        #target_audio = np.asarray(target_audio, dtype=np.float32)  # Ensure it's float32 array

        predictions = self.model(target_audio)  # Expand dimensions to (1, 80000)
        logging.debug(predictions)
        predicted_class = np.argmax(predictions, axis=-1)
        return self.encoder.inverse_transform(predicted_class)[0]

    def save(self) -> None:
        logging.info("Saving model")
        self.model.save()