"""
    Fetching the input audio to
    the configured model to receive
    that data and output the label

    By Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import logging
from api.utils import read_yaml
import src.model.model as model
import src.model.yamnet as yamnet

logging.basicConfig(level=logging.INFO)
logging: object = logging.getLogger("api.model_api")

# Use to predict given an input audio
def fetch_model_api(filepath: str) -> str:
    try:
        # Load the configuration
        config: dict = read_yaml(os.path.join("configs", "network_config.yaml"))
        model_name: str = config["model"][0]
        weights_p: str = os.path.join("src", "weights", model_name)
        
        logging.info(f"Loading model from {weights_p}")
        
        # Load the mode;
        load_model: object = yamnet.YamnetClassifier.load(weights_p)
        
        # Create a model handler and assign the loaded model
        model_handler: object = yamnet.ModelHandler()
        model_handler.model = load_model
        
        logging.info(f"Model loaded successfully, processing file {filepath}")
        
        # Predict using the model handler
        prediction: str = model_handler.predict(filepath)
        
        logging.info(f"Prediction for {filepath}: {prediction}")
        return prediction
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return "Error: Model file not found"
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "Error: An error occurred while processing the model"
        