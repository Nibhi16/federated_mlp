# client.py
import flwr as fl
import tensorflow as tf
from dataset import load_data

# Set this for each client (0, 1, ...)
CLIENT_ID = 1

# Create MLP model
def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation="relu", input_shape=(13,)),  # 13 features in dataset
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

# Load data for this client
X_train, y_train, X_test, y_test = load_data(client_id=CLIENT_ID, num_clients=2)
model = create_model()

# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config=None):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(X_train, y_train, epochs=3, batch_size=32, verbose=0)
        return model.get_weights(), len(X_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        return loss, len(X_test), {"accuracy": accuracy}

# Start client
if __name__ == "__main__":
    fl.client.start_numpy_client(server_address="localhost:8081", client=FlowerClient())
