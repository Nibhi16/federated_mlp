import flwr as fl
import numpy as np
import tensorflow as tf
from dataset import load_data
from threading import Thread
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import time

# Import DP optimizer
try:
    from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasAdamOptimizer
    DP_AVAILABLE = True
except ImportError:
    try:
        # Try alternative import path
        from tensorflow_privacy.privacy.optimizers import dp_optimizer_keras
        DPKerasAdamOptimizer = dp_optimizer_keras.DPKerasAdamOptimizer
        DP_AVAILABLE = True
    except ImportError:
        print("Warning: tensorflow_privacy not available. Using standard Adam optimizer.")
        DP_AVAILABLE = False

NUM_CLIENTS = 2
CLIENT_EPOCHS = 3
round_metrics = {i: [] for i in range(NUM_CLIENTS)}

# DP Parameters
L2_NORM_CLIP = 1.0
NOISE_MULTIPLIER = 0.5
NUM_MICROBATCHES = 32
LEARNING_RATE = 0.001

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(13,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    # Use DP optimizer if available
    if DP_AVAILABLE:
        optimizer = DPKerasAdamOptimizer(
            l2_norm_clip=L2_NORM_CLIP,
            noise_multiplier=NOISE_MULTIPLIER,
            num_microbatches=NUM_MICROBATCHES,
            learning_rate=LEARNING_RATE
        )
    else:
        optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Flower client class remains the same
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, client_id):
        self.client_id = client_id
        self.X_train, self.y_train, self.X_test, self.y_test = load_data(client_id, NUM_CLIENTS)
        self.model = create_model()

    def get_parameters(self, config=None):
        return self.model.get_weights()

    def fit(self, parameters, config):
        self.model.set_weights(parameters)
        history = self.model.fit(
            self.X_train, self.y_train,
            epochs=CLIENT_EPOCHS,
            batch_size=32,
            verbose=0
        )
        loss = history.history['loss'][-1]
        print(f"[Client {self.client_id}] Training loss: {loss:.4f}")
        return self.model.get_weights(), len(self.X_train), {}

    def evaluate(self, parameters, config):
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        print(f"[Client {self.client_id}] Evaluation loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
        if self.client_id in round_metrics:
            round_metrics[self.client_id].append(accuracy)
        return loss, len(self.X_test), {"accuracy": accuracy}

def start_client(client_id):
    try:
        print(f"[Client {client_id}] Initializing...")
        client = FlowerClient(client_id)
        print(f"[Client {client_id}] Connecting to server at localhost:8081...")
        fl.client.start_numpy_client(server_address="localhost:8081", client=client)
        print(f"[Client {client_id}] Connection closed (training completed).")
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")
        print(f"[Client {client_id}] Make sure the server is running on localhost:8081")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"\n=== Starting {NUM_CLIENTS} clients for Federated Learning ===")
    print("Make sure the server is running on localhost:8081")
    print("Waiting a moment for server to be ready...\n")
    
    time.sleep(3)  # Give server time to start

    threads = []
    for i in range(NUM_CLIENTS):
        t = Thread(target=start_client, args=(i,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    # Plot client accuracies if available
    print("\n" + "=" * 60)
    print("CLIENT ACCURACY SUMMARY")
    print("=" * 60)
    
    for client_id, accuracies in round_metrics.items():
        if len(accuracies) > 0:
            print(f"Client {client_id}: {len(accuracies)} rounds")
            print(f"  Accuracies: {[f'{a:.4f}' for a in accuracies]}")
            if len(accuracies) > 0:
                print(f"  Final: {accuracies[-1]:.4f} ({accuracies[-1]*100:.2f}%)")
                print(f"  Best: {max(accuracies):.4f} ({max(accuracies)*100:.2f}%)")
        else:
            print(f"Client {client_id}: No metrics collected")
    
    if any(len(accuracies) > 0 for accuracies in round_metrics.values()):
        plt.figure(figsize=(10, 6))
        for client_id, accuracies in round_metrics.items():
            if len(accuracies) > 0:
                plt.plot(range(1, len(accuracies)+1), accuracies, marker='o', label=f'Client {client_id}', linewidth=2, markersize=8)
        
        plt.title("Federated Learning: Client Accuracy per Round (DP Enabled)", fontsize=14, fontweight='bold')
        plt.xlabel("Round", fontsize=12)
        plt.ylabel("Accuracy", fontsize=12)
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig("client_accuracy.png", dpi=300, bbox_inches='tight')
        print("\n✓ Client accuracy plot saved as 'client_accuracy.png'")
        try:
            plt.show(block=False)
        except:
            pass
    else:
        print("\n⚠ No accuracy metrics collected. Check if training completed successfully.")
        print("This may happen if clients couldn't connect to the server.")
    print("\n" + "=" * 60)
