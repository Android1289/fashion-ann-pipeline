
import gzip
import os
import urllib.request
import numpy as np

BASE_URL = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
FILES = {
    "train_images": "train-images-idx3-ubyte.gz",
    "train_labels": "train-labels-idx1-ubyte.gz",
    "test_images": "t10k-images-idx3-ubyte.gz",
    "test_labels": "t10k-labels-idx1-ubyte.gz"
}

def download_file(filename):
    os.makedirs("data/raw", exist_ok=True)
    path = os.path.join("data/raw", filename)

    if not os.path.exists(path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(BASE_URL + filename, path)

    return path

def read_images(path):
    with gzip.open(path, "rb") as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=16)

    return data.reshape(-1, 28, 28)

def read_labels(path):
    with gzip.open(path, "rb") as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=8)

    return data

def main():
    train_images = read_images(download_file(FILES["train_images"]))
    train_labels = read_labels(download_file(FILES["train_labels"]))
    test_images = read_images(download_file(FILES["test_images"]))
    test_labels = read_labels(download_file(FILES["test_labels"]))

    np.save("data/raw/x_train.npy", train_images)
    np.save("data/raw/y_train.npy", train_labels)
    np.save("data/raw/x_test.npy", test_images)
    np.save("data/raw/y_test.npy", test_labels)

    print("Fashion-MNIST dataset prepared successfully.")
    print(f"Training images: {train_images.shape}")
    print(f"Training labels: {train_labels.shape}")
    print(f"Test images: {test_images.shape}")
    print(f"Test labels: {test_labels.shape}")

if __name__ == "__main__":
    main()

