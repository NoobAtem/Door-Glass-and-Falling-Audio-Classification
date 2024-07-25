"""
    Fetching and requesting a download of datasets from
    the Gdrive given the format

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""

import opendatasets as od
import subprocess
import shutil
import yaml
import gdown
import os
import src.utilities.system as system
import logging

logging: object = logging.getLogger("src.scraping.drive")


def fetch_drive() -> None:
    """
        This handles downloading the zip file from
        my gdrive, you can change the config by
        modifying dataset_config.yaml. Config is the
        path to that file
    """
    logging.info("Fetching dataset from drive")
    monitor_dir: list = os.listdir()
    _paths: dict = system.get_relevant_paths()
    

    # Generate missing dataset files
    _missing: dict = system.check_dataset_health()
    _external: dict = _missing["external"]
    _raw: dict = _missing["raw"]

    # Download all missing files
    folderpath: str = _paths["external"]
    for key, val in _external.items():
        logging.info(f"Downloading dataset")
        od.download(val)
        
        # By pass the download warning from gdrive by
        # first getting the current download file
        new_file: str = system.list_diff(os.listdir(), monitor_dir)[0]
        logging.debug(new_file)
        
        # Getting the zip file
        subprocess.run(["gdown", new_file])
        
        # Cleanup
        system.delete_entity(new_file)
        
        # Getting the zip file
        monitor_dir = os.listdir()
        new_file = list(filter(lambda p: p.endswith(".zip"), monitor_dir))[0]
        logging.debug(f"Download results: {new_file}")
        
        # Unzipping
        destination: str = os.path.join(folderpath, key)
        system.unzip(new_file, destination)
        system.delete_entity(new_file)
        logging.info(f"Dataset have been move to external")
        monitor_dir = os.listdir()

    folderpath = _paths["raw"]
    for key, val in _raw.items():
        logging.info(f"Downloading dataset")
        od.download(val)
        
        # By pass the download warning from gdrive by
        # first getting the current download file
        new_file: str = system.list_diff(os.listdir(), monitor_dir)[0]
        logging.debug(new_file)
        
        # Getting the zip file
        subprocess.run(["gdown", new_file])
        
        # Cleanup
        system.delete_entity(new_file)
        
        # Getting the zip file
        monitor_dir = os.listdir()
        new_file = list(filter(lambda p: p.endswith(".zip"), monitor_dir))[0]
        logging.debug(f"Download results: {new_file}")
        
        # Unzipping
        destination: str = os.path.join(folderpath, key)
        system.unzip(new_file, destination)
        system.delete_entity(new_file)
        logging.info(f"Dataset have been move to internal")
        monitor_dir = os.listdir()

def entry() -> None:
    logging.info("==== Drive ====")
    fetch_drive()
    logging.info("==== End of Drive ====")