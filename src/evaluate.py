import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def main():
    x_test = np.load("data/processed/x_test.npy")
    y_test = np.load("data/processed/y_test.npy")

    model = tf.keras.models.load_model("models/model.h5")

    test_loss, test_accuracy = model.evaluate(
        x_test,
        y_test,
        verbose=1
    )

    predictions = model.predict(x_test, verbose=1)
    predicted_labels = np.argmax(predictions, axis=1)

    cm = confusion_matrix(y_test, predicted_labels)

    display = ConfusionMatrixDisplay(confusion_matrix=cm)
    display.plot()
    plt.title("Fashion-MNIST Confusion Matrix")
    plt.savefig("confusion_matrix.png", bbox_inches="tight")
    plt.close()

    metrics = {
        "test_loss": float(test_loss),
        "test_accuracy": float(test_accuracy)
    }

    with open("metrics.json", "w") as file:
        json.dump(metrics, file, indent=4)

    print("Evaluation completed successfully.")
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print("Confusion matrix saved to confusion_matrix.png")
    print("Metrics saved to metrics.json")

if __name__ == "__main__":
    main()