"""
    This utility manages project paths that are seemingly group
    together and called. This is convinient for calling big project
    paths that removes duplicated code

    By Dimaunahan, Isiah Jordan (NoobAtem)
"""

import os
import src.utilities.system as system
import logging

logging: object = logging.getLogger("src.utilities.view")

class AudioDataSource:
    """
        This is to handle monitoring changes
        occuring in the data folder that only
        includes raw, interim, and preprocessed
    """
    def __init__(self) -> None:
        
        self.rdoor: list = [] # raw door audio
        self.rglass: list = [] # raw glass audio
        
        # Get paths
        self.generatePath()
        
        # Make sure it's currently in its latest files
        self.updateContent()

    def updateContent(self) -> None:
        logging.info("Initializing Audio Monitoring Class")
        rdoor: list = os.listdir(self.rdoor_p)
        rglass: list = os.listdir(self.rglass_p)

        # Get only audio files
        for aud in rdoor:
            if aud.endswith(".wav"):
                logging.info(f"Adding {aud}")
                self.rdoor.append(os.path.join(self.rdoor_p, aud))

        for aud in rglass:
            if aud.endswith(".wav"):
                logging.info(f"Adding {aud}")
                self.rglass.append(os.path.join(self.rglass_p, aud))
        
        self.rdoor_i: int = len(self.rdoor)
        self.rglass_i: int = len(self.rglass)

    def generatePath(self) -> None:
        logging.info("Generating Paths")
        self.rdoor_p: str = os.path.join("data", "raw", "door")
        self.rglass_p: str = os.path.join("data", "raw", "glass")
        self.interim_p: str = os.path.join("data", "interim")
        self.preprocessed_p: str = os.path.join("data", "preprocessed")
        logging.debug(f"Path name: {self.rdoor_p}")
        logging.debug(f"Path name: {self.rglass_p}")
        logging.debug(f"Path name: {self.interim_p}")
        logging.debug(f"Path name: {self.preprocessed_p}")

    def getRawDoorAudio(self) -> list:
        logging.info("Raw door audio have been requested")
        return self.rdoor
        
    def getRawGlassAudio(self) -> list:
        logging.info("Raw glass audio have been requested")
        return self.rglass

    def getRawAudio(self) -> list:
        return self.getRawDoorAudio() + self.getRawGlassAudio()

    def getInterimPath(self) -> str:
        return self.interim_p

    def getPreprocessPath(self) -> str:
        return self.preprocessed_p


    