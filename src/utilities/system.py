"""
    Handles all type of project creating, modifying, 
    reading, and moving

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""

import yaml
import shutil
import os
import logging
import numpy as np
from zipfile import ZipFile

logging: object = logging.getLogger("src.utilities.system")

def is_not_a_path(filepath: str) -> bool:
    return not os.path.exists(filepath)

def get_relevant_paths() -> dict:
    """
        This makes for convinience in getting
        usual important folders or file without
        the need to join path
    """
    paths: dict = {
        "dataset_config": os.path.join("configs", "dataset_config.yaml"),
        "raw": os.path.join("data", "raw"),
        "external": os.path.join("data", "external"),
        "interim": os.path.join("data", "interim"),
        "processed": os.path.join("data", "processed")
    }
    return paths

def check_zip_root_dir(filepath: str) -> bool:
    logging.info(f"Cheking if zip file has a root dir: {filepath}")
    with ZipFile(filepath, "r") as zip_ref:
        content: list = zip_ref.namelist()
        root_directory: str = os.path.commonprefix(content)
        if root_directory.endswith("/"):
            return True
        else:
            return False

def get_zip_root_dir(filepath: str) -> str:
    logging.info(f"Getting the root dir of zip: {filepath}")
    with ZipFile(filepath, "r") as zip_ref:
        content: list = zip_ref.namelist()
        root_directory: str = os.path.commonprefix(content)
        if root_directory.endswith('/'):
            root_directory = root_directory[:-1]
        return root_directory
        
def unzip(source: str, destination: str) -> None:
    logging.info(f"Unzipping {source}")
    if is_not_a_path(source):
        logging.info(f"Filepath does not exist {source}")
        return

    with ZipFile(source, "r") as zip_ref:
        if not check_zip_root_dir:
            if is_not_a_path(destination):
                os.mkdir(destination)
                logging.debug(f"Created a directory: {destination}")
            logging.debug(f"Extracting with no root")
            zip_ref.extractall(destination)
        else:
            logging.debug(f"Extracting with rename root")
            key: str = destination.split("/")[-1]
            destination = "/".join(destination.split("/")[:-1])
            logging.info(f"Path to data: {destination}")
            zip_ref.extractall(destination)
            os.rename(os.path.join(destination, get_zip_root_dir(source)), os.path.join(destination, key))
            
        logging.info("Succesful extraction")

def read_yaml(filepath: str) -> dict:
    logging.info(f"Reading yaml: {filepath}")
    
    if is_not_a_path(filepath):
        logging.error(f"Filepath does not exist: {filepath}")
        return None
    if not filepath.endswith(".yaml"):
        logging.error(f"Not valid format: {filepath}")
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

# Delete file or folder
def delete_entity(path: str) -> None:
    if is_not_a_path(path):
        logging.error(f"Path does not exist: {path}")
        return
    if os.path.isdir(path):
        logging.debug(f"Deleting Dir: {path}")
        shutil.rmtree(path)
    elif os.path.isfile(path):
        logging.debug(f"Deleting File: {path}")
        os.remove(path)

# Delete a collection of file or folder or both
def delete_entities(path: list) -> None:
    logging.info("Deleting a collection of entities")
    
    for _p in path:
        delete_entity(_p)

# Move file or folder
def move_entity(source: str, destination: str) -> None:
    logging.info("Moving entity")
    is_source_exist: bool = is_not_a_path(source)
    is_dest_exist: bool = is_not_a_path(destination)
    if not is_source_exist:
        logging.error(f"Source does not exist: {source}")
        return
    elif not is_dest_exist:
        logging.error(f"Destination does not exist: {destination}")
        return
        
    if os.path.isdir(source):
        logging.debug(f"Moving Dir: {source}")
    elif os.path.isfile(path):
        logging.debug(f"Deleting File: {source}")
    shutil.move(source, destination)


def move_entities(sources: list, destination: str) -> None:
    logging.info("Moving a collection of entities")
    
    for _p in sources:
        move_entity(_p, destination)

def list_diff(minuend: list, subtrahend: list) -> list:
    logging.info("Get two list difference in element")
    _minuend: np.array = np.array(minuend)
    _subtrahend: np.array = np.array(subtrahend)
    return np.setdiff1d(_minuend, _subtrahend)

def check_dataset_health() -> dict:
    """
        Verify if the current datasets has
        matched the requirement else return
        missing datasets
    """
    logging.info("Verify dataset health")
    _paths: dict = get_relevant_paths()
    _conf: dict = read_yaml(_paths["dataset_config"])
    _missing: dict = {
        "external": {},
        "raw": {}
    }

    # Checking all of raw
    for key, val in enumerate(_conf["internal"]):
        # Fetch dataset name
        if not val == "description":
            if is_not_a_path(os.path.join(_paths["internal"], val)):
                logging.debug(f"Missing internal entity: {val}")    
                _missing["internal"][val] = _conf["external"][val]["url"]

    # Checking all of external
    for key, val in enumerate(_conf["external"]):
        # Fetch dataset name
        if not val == "description":
            if is_not_a_path(os.path.join(_paths["external"], val)):
                logging.debug(f"Missing external entity: {val}")
                _missing["external"][val] = _conf["external"][val]["url"]
    return _missing