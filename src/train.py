import os
import yaml
import numpy as np
import pandas as pd
import tensorflow as tf

def main():
    with open("params.yaml", "r") as file:
        params = yaml.safe_load(file)

    train_params = params["train"]

    dense_units = train_params["dense_units"]
    dropout_rate = train_params["dropout_rate"]
    learning_rate = train_params["learning_rate"]
    epochs = train_params["epochs"]
    batch_size = train_params["batch_size"]

    x_train = np.load("data/processed/x_train.npy")
    y_train = np.load("data/processed/y_train.npy")
    x_val = np.load("data/processed/x_val.npy")
    y_val = np.load("data/processed/y_val.npy")

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(dense_units, activation="relu"),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=learning_rate
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=epochs,
        batch_size=batch_size
    )

    os.makedirs("models", exist_ok=True)

    model.save("models/model.h5")

    pd.DataFrame(history.history).to_csv(
        "models/history.csv",
        index=False
    )

    print("Training completed successfully.")
    print("Model saved to models/model.h5")
    print("History saved to models/history.csv")

if __name__ == "__main__":
    main()