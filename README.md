# Federated Learning with Privacy Preservation for Medical Data

This project implements a Federated Learning system using the Flower framework with Differential Privacy (DP) for medical data classification. The system uses a Multi-Layer Perceptron (MLP) neural network to classify heart disease data while preserving patient privacy through differential privacy techniques.

## Features

- **Federated Learning**: Distributed training across multiple clients using Flower framework
- **Differential Privacy**: Privacy-preserving training with tensorflow-privacy
- **MLP Model**: Multi-layer perceptron for binary classification
- **Medical Data**: Uses UCI Heart Disease dataset
- **Client Simulation**: Supports both single client and multi-client simulation

## Project Structure

```
federated_mlp/
├── server.py          # Flower server implementation
├── client.py          # Single client implementation
├── client_sim.py      # Multi-client simulation with DP
├── dataset.py         # Data loading and preprocessing
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Note**: If you encounter issues with `tensorflow-privacy`, you can install it separately:
   ```bash
   pip install tensorflow-privacy
   ```

## Usage

### Option 1: Multi-Client Simulation (Recommended)

This option simulates multiple clients in a single process with differential privacy enabled:

```bash
python client_sim.py
```

**Note**: Make sure to start the server first (see below).

### Option 2: Single Client Mode

1. **Start the server** (in one terminal):
   ```bash
   python server.py
   ```

2. **Start clients** (in separate terminals):
   ```bash
   python client.py
   ```
   You can modify `CLIENT_ID` in `client.py` for each client instance.

## How It Works

### 1. Data Distribution
- The UCI Heart Disease dataset is automatically downloaded and preprocessed
- Data is split among clients for federated training
- Each client has its own train/test split

### 2. Model Architecture
The MLP model consists of:
- Input layer: 13 features (normalized)
- Hidden layer 1: 16 neurons with ReLU activation
- Hidden layer 2: 8 neurons with ReLU activation
- Output layer: 1 neuron with sigmoid activation (binary classification)

### 3. Differential Privacy
- Uses `DPKerasAdamOptimizer` from tensorflow-privacy
- Privacy parameters:
  - L2 norm clip: 1.0
  - Noise multiplier: 0.5
  - Number of microbatches: 32

### 4. Federated Training
- Server aggregates model weights from all clients using FedAvg
- Clients train locally for 3 epochs per round
- Total of 5 federated rounds

## Configuration

You can modify these parameters in the respective files:

**In `client_sim.py` and `client.py`:**
- `NUM_CLIENTS`: Number of clients (default: 2)
- `CLIENT_EPOCHS`: Local training epochs per round (default: 3)
- Model architecture (hidden layers, neurons)

**In `server.py`:**
- `NUM_ROUNDS`: Number of federated learning rounds (default: 5)
- `min_fit_clients`: Minimum clients required for training
- `min_eval_clients`: Minimum clients required for evaluation

**DP Parameters (in `client_sim.py`):**
- `L2_NORM_CLIP`: Gradient clipping threshold (default: 1.0)
- `NOISE_MULTIPLIER`: DP noise scale (default: 0.5)
- `NUM_MICROBATCHES`: Microbatch size for DP (default: 32)
- `LEARNING_RATE`: Learning rate (default: 0.001)

## Results

After training, the system generates:
- Console output with training progress and metrics
- Plot showing client accuracies per round (from `client_sim.py`)
- Plot showing server aggregated accuracy per round (from `server.py`)
- Saved accuracy plot as `server_accuracy.png`

## Research Applications

This implementation is suitable for research on:
- Federated Learning in healthcare
- Privacy-preserving machine learning
- Differential Privacy mechanisms
- Distributed training with medical data

## Privacy Considerations

- **Differential Privacy**: Adds calibrated noise to gradients to protect individual data points
- **No Data Sharing**: Raw medical data never leaves client devices
- **Secure Aggregation**: Only model parameters are shared with the server
- **Privacy Budget**: The noise multiplier controls the privacy-utility trade-off

## Troubleshooting

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Connection refused**: Ensure the server is running before starting clients

3. **DP optimizer not found**: The code falls back to standard Adam optimizer if tensorflow-privacy is not available

4. **Port conflicts**: Change the port in `server.py` and `client*.py` if 8081 is in use

## License

This project is for research purposes. The UCI Heart Disease dataset is used under UCI Machine Learning Repository terms.

## References

- Flower Framework: https://flower.dev
- TensorFlow Privacy: https://github.com/tensorflow/privacy
- UCI Heart Disease Dataset: https://archive.ics.uci.edu/ml/datasets/heart+disease


