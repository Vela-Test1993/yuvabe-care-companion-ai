import os
import pandas as pd
import string
from utils import logger

logger = logger.get_logger()

DATASET_PATH = "src/backend/data/dataset.csv"
PARAQUET_DATASET_PATH = "hf://datasets/lavita/ChatDoctor-HealthCareMagic-100k/data/train-00000-of-00001-5e7cb295b9cff0bf.parquet"

def get_data_set():

    try:
        if not os.path.exists(DATASET_PATH):
            logger.info(f"{DATASET_PATH} not found. Reading from Parquet file.")
            df = pd.read_parquet(PARAQUET_DATASET_PATH)
            df.drop_duplicates(subset=["input", "output"], inplace=True)
            df.dropna(subset=["input", "output"], inplace=True) # Remove NaNs first
        
        # This line is to remove the empty column or column with only spaces
            df = df[(df["input"].str.strip() != "") & (df["output"].str.strip() != "")] # Remove empty strings/spaces

        # This line is to remove puncuation and emjois
            translator = str.maketrans('', '', string.punctuation)
            df["input"] = df["input"].str.lower().str.translate(translator)
            df["output"] = df["output"].str.lower().str.translate(translator)
            df.to_csv(DATASET_PATH, index=False)
            logger.info(f"CSV file created and cleaned at: {DATASET_PATH}")
        else:
            logger.info(f"Loading existing dataset from: {DATASET_PATH}")
            df = pd.read_csv(DATASET_PATH)
            logger.info("Dataset loaded successfully.")
        return df

    except Exception as e:
        logger.error(f"Error while loading dataset: {e}", exc_info=True)
        return None