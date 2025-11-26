# Quick Start Guide - Manual Execution

## Step-by-Step Instructions

### Prerequisites
Make sure you have installed all dependencies:
```bash
pip install -r requirements.txt
```

### Method 1: Using Two Terminal Windows (Recommended)

#### Terminal 1 - Start the Server:
```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
python server.py
```

**Expected Output:**
```
============================================================
Federated Learning Server Starting...
Server address: localhost:8081
Number of rounds: 5
Waiting for clients to connect...
============================================================
```

#### Terminal 2 - Start the Clients:
```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
python client_sim.py
```

**Expected Output:**
```
=== Starting 2 clients for Federated Learning ===
Make sure the server is running on localhost:8081
Waiting a moment for server to be ready...

[Client 0] Training loss: 0.5234
[Client 1] Training loss: 0.5123
...
```

### What Happens:
1. Server starts and waits for clients
2. Clients connect and download initial model
3. Each client trains locally for 3 epochs
4. Clients send updated weights back to server
5. Server aggregates weights using FedAvg
6. Process repeats for 5 rounds
7. Final metrics and plots are generated

### Generated Files:
- `server_accuracy.png` - Server aggregated accuracy plot
- `client_accuracy.png` - Individual client accuracy plots

### Expected Final Results:
```
=== FEDERATED LEARNING TRAINING RESULTS ===
Total Rounds Completed: 5
Final Aggregated Accuracy: 0.86-0.91 (86-91%)
```

---

## Troubleshooting

### Error: "Module not found"
```bash
pip install flwr tensorflow numpy pandas scikit-learn matplotlib
```

### Error: "Connection refused"
- Make sure server is running first
- Check that port 8081 is not in use
- Wait a few seconds after starting server before starting clients

### Error: "No module named 'tensorflow_privacy'"
- This is OK - the code will use standard Adam optimizer
- To enable DP: `pip install tensorflow-privacy`

### Plot not showing?
- Check that `client_accuracy.png` and `server_accuracy.png` are saved in the folder
- The plots are saved even if display is not available

---

## Notes
- The server must be started BEFORE the clients
- The training will take 2-5 minutes
- All results are saved to image files automatically


