import os
import yaml
import numpy as np
from sklearn.model_selection import train_test_split

def main():
    with open("params.yaml", "r") as file:
        params = yaml.safe_load(file)

    test_size = params["preprocess"]["test_size"]
    seed = params["preprocess"]["seed"]

    x_train = np.load("data/raw/x_train.npy")
    y_train = np.load("data/raw/y_train.npy")
    x_test = np.load("data/raw/x_test.npy")
    y_test = np.load("data/raw/y_test.npy")

    # Reconciled normalization: Standardized [0, 1] float32 scaling for ANN stability
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train, x_val, y_train, y_val = train_test_split(
        x_train,
        y_train,
        test_size=test_size,
        random_state=seed,
        stratify=y_train
    )

    os.makedirs("data/processed", exist_ok=True)

    np.save("data/processed/x_train.npy", x_train)
    np.save("data/processed/y_train.npy", y_train)
    np.save("data/processed/x_val.npy", x_val)
    np.save("data/processed/y_val.npy", y_val)
    np.save("data/processed/x_test.npy", x_test)
    np.save("data/processed/y_test.npy", y_test)

    print("Preprocessing completed successfully.")
    print(f"Training: {x_train.shape}")
    print(f"Validation: {x_val.shape}")
    print(f"Test: {x_test.shape}")
    print(f"Pixel range: {x_train.min()} - {x_train.max()}")

if __name__ == "__main__":
    main()