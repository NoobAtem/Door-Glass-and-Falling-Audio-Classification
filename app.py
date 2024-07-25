"""
    The goal of this file is to initialize the following
    process:
    - Check for any missing folders
    - Initialize Logs
    - Instigating modules
    
    by Dimaunahan, Isiah Jordan (NoobAtem)
"""


import yaml
try:
    from yaml import CLoader as Loader
except:
    from yaml import Loader
import os
import logging
import logging.config
import sys
from queue import Queue

# Modules
import src.scraping.drive as drive
import src.preprocessing.audio as audio

def read_config(filepath: str) -> dict:
    with open(filepath, "r") as yml:
        return yaml.safe_load(yml)

def print_help() -> None:
    text: str = """
        This designed to setup or instigate particular options
        that can logs, missing files, or etc.
        
        The following are available arguments to be passed:
        -h    -- List all available task and purpose of module
        -s [module_name].py    -- Run entry point in the module
        -ch    -- Run a health check for potential missing components
    """
    print(text)

def run_module(filename: str) -> None:
    """
        Handle running each module scripts
    """
    print(f"Running Module {filename}")
    if not filename.endswith(".py"):
        logging.error("Module does not exsist")
        return
    if filename.endswith("drive.py"):
        logging.info("Module drive has been called")
        drive.entry()
    if filename.endswith("audio.py"):
        logging.info("Module audio has been called")
        audio.entry()
    else:
        logging.error("Module does not exist")


def log_config() -> None:
    """
        Setup the appropriate logging configuraton by reading the
        config for logs
    """
    logging.config.dictConfig(read_config(os.path.join("configs", "log_config.yaml")))
    logging.info("Logs have been initialize")

def proj_health() -> None:
    """
        Using a list of required folders and files,
        the project takes notes for any missing prerequisites
    """
    logging.info("---> Starting")
    tree: dict = read_config(os.path.join("configs", "config.yaml"))["tree"]
    q: object = Queue(maxsize=100)
    q.put([]) # Start with root
    while not q.empty():
        # Pop the bottom item
        logging.debug(f"Queue: {list(q.queue)}")
        path: list = q.get()
        # Track tree
        _dir: dict = tree
        # Track path
        _p: str = ""
        for i in path:
            _dir = _dir[i]
            _p += i + "/" 

        logging.info(f"Tree Dictionary: {_p}")
        # Verify path
        for key, val in enumerate(_dir):
            if not val == "description":
                logging.info(f"Verifying Path: {val}")
                temp_p: str = os.path.join(_p, val)
                if not os.path.exists(temp_p):
                    logging.error(f"Missing path: {temp_p}")
                    return
                elif os.path.isdir(temp_p):
                    logging.info(f"Adding folder: {_p}")
                    q.put(temp_p.split("/"))
                    
    logging.info("---> No missing modules found")

# Check particular user flags
def switch_flags() -> None:
    if len(sys.argv) == 1:
        logging.error("No tasks specified")

    logging.info("Verifying flags")
    curr_pointer_arg: int = 1
    while curr_pointer_arg < len(sys.argv):
        if sys.argv[curr_pointer_arg] == "-h":
            logging.info("Help function called")
            print_help()
        elif sys.argv[curr_pointer_arg] == "-s":
            if curr_pointer_arg + 1 < len(sys.argv) and sys.argv[curr_pointer_arg + 1].endswith(".py"):
                curr_pointer_arg += 1
                logging.info(f"Running module {sys.argv[curr_pointer_arg]}")
                run_module(sys.argv[curr_pointer_arg])
        elif sys.argv[curr_pointer_arg] == "-ch":
            logging.info(f"Checking project health")
            proj_health()
        else:
            logging.warning("This is not a valid flag")            

        curr_pointer_arg += 1
            

if __name__ == "__main__":
    log_config()
    logging.info("===== Module Start =====")
    switch_flags()
    logging.info("=====  Module End  =====")