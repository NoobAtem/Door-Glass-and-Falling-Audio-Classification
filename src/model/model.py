"""
    Generates the necessary models to be designed and saved
    into weights, this is in reference to modeling.ipynb were
    expertiments and trial error have been conducted to identify
    decent models

    by Dimaunahan, Isiah Jordan (NoobAtem)
"""

import logging
import src.model.yamnet as yamnet

logging: object = logging.getLogger("src.model.model")

def entry() -> None:
    logging.info("==== Start of model ====")
    ymnt: object = yamnet.ModelHandler()
    ymnt.save()
    logging.info("==== End of model ====")
