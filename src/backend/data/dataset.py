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
        else:
            logger.info(f"Loading existing dataset from: {DATASET_PATH}")
            df = pd.read_csv(DATASET_PATH).fillna("")

        # Cleaning logic for both Parquet and CSV data
        df.drop_duplicates(subset=["input", "output"], inplace=True)

        # Remove NaN values or empty strings
        df = df[df["input"].str.strip().notna() & df["output"].str.strip().notna()]
        df = df[(df["input"].str.strip() != "") & (df["output"].str.strip() != "")]

        # Clean punctuation and emojis
        translator = str.maketrans('', '', string.punctuation)
        df["input"] = df["input"].fillna("").str.lower().str.translate(translator)
        df["output"] = df["output"].fillna("").str.lower().str.translate(translator)

        # Save only if data is present
        if not os.path.exists(DATASET_PATH):
            df.to_csv(DATASET_PATH, index=False)
            logger.info(f"CSV file created and cleaned at: {DATASET_PATH}")

        return df

    except Exception as e:
        logger.error(f"Error while loading dataset: {e}", exc_info=True)
        return None
