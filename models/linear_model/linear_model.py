import numpy as np
import pandas as pd
import pickle
from config import settings


def get_input_matrix(df):
    return np.column_stack(
        (df.abs_diff_longitude, df.abs_diff_latitude, np.ones(len(df)))
    )


def train_linear_model() -> None:
    train_df = pd.read_csv(
        f'./data/{settings.get("dataset.nyc_fare_train_dataset", "train.csv.zip")}',
        nrows=10_000_000,
    )
    train_df = train_df.dropna(how="any", axis="rows")

    train_df = train_df.drop(
        train_df.loc[
            (train_df["pickup_longitude"] < -80) | (train_df["pickup_longitude"] > 50)
        ].index
    )
    train_df = train_df.drop(
        train_df.loc[
            (train_df["dropoff_longitude"] < -80) | (train_df["dropoff_latitude"] > 50)
        ].index
    )
    # add_travel_vector_features(train_df)
    train_df["abs_diff_longitude"] = (
        train_df.dropoff_longitude - train_df.pickup_longitude
    ).abs()
    train_df["abs_diff_latitude"] = (
        train_df.dropoff_latitude - train_df.pickup_latitude
    ).abs()

    train_df = train_df[
        (train_df.abs_diff_longitude < 5.0) & (train_df.abs_diff_latitude < 5.0)
    ]

    train_X = get_input_matrix(train_df)
    train_y = np.array(train_df["fare_amount"])

    (w, _, _, _) = np.linalg.lstsq(train_X, train_y, rcond=None)
    with open("./artifacts/weights.pkl", "wb") as f:
        pickle.dump(w, f)
