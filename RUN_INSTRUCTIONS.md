# Updated Run Instructions - Server Connection Fixed

## Important Changes Made

1. **Server Address**: Changed from `localhost:8081` to `0.0.0.0:8081` for better network binding
2. **Enhanced Logging**: Added debug messages to track connection and metrics
3. **Better Error Handling**: Improved diagnostics for connection issues

---

## Step-by-Step Execution

### Step 1: Start Server (Terminal 1)

```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
python server.py
```

**You should see:**
```
============================================================
Federated Learning Server Starting...
Server address: 0.0.0.0:8081
Number of rounds: 5
Waiting for clients to connect...
============================================================
```

**KEEP THIS TERMINAL OPEN** - The server must stay running!

---

### Step 2: Start Clients (Terminal 2 - NEW Terminal)

**Wait 5 seconds** after server starts, then:

```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
python client_sim.py
```

**You should see:**
```
=== Starting 2 clients for Federated Learning ===
Make sure the server is running on localhost:8081
Waiting a moment for server to be ready...

[Client 0] Initializing...
[Client 1] Initializing...
[Client 0] Connecting to server at localhost:8081...
[Client 1] Connecting to server at localhost:8081...
[Server] Starting Round 1 - Waiting for clients to train...
[Client 0] Training loss: 0.5234
[Client 1] Training loss: 0.5123
[Server] Round 1 - Requesting evaluation from clients...
[Client 0] Evaluation loss: 0.4123, Accuracy: 0.7823
[Client 1] Evaluation loss: 0.3987, Accuracy: 0.7934
...
```

---

## What to Look For

### ✅ Success Indicators:

1. **Server Terminal:**
   - Shows "[Server] Starting Round X" messages
   - Shows "[Server] Round X - Requesting evaluation" messages
   - Shows "Debug: Received N metric entries"
   - Shows "Debug: Aggregated accuracy: X.XXXX"

2. **Client Terminal:**
   - Shows "[Client X] Initializing..." 
   - Shows "[Client X] Connecting to server..."
   - Shows training and evaluation messages for each round
   - Shows final accuracy summary

### ❌ Problem Indicators:

If you see:
- "No accuracy metrics collected" → Check if clients completed all rounds
- "Connection refused" → Server not started or wrong address
- "No metrics received for aggregation" → Client evaluate() not returning metrics correctly

---

## Expected Final Output

### Server Terminal:
```
=== FEDERATED LEARNING TRAINING RESULTS ===
Total Rounds Completed: 5

Loss per Round:
  Round 1: Loss = 0.5234
  ...

Aggregated Accuracy per Round:
  Round 1: Accuracy = 0.7823 (78.23%)
  ...

FINAL AGGREGATED ACCURACY: 0.8923 (89.23%)
```

### Client Terminal:
```
============================================================
CLIENT ACCURACY SUMMARY
============================================================
Client 0: 5 rounds
  Accuracies: ['0.7823', '0.8345', ...]
  Final: 0.8923 (89.23%)
  Best: 0.8923 (89.23%)
...
```

---

## Troubleshooting

### Issue: Clients connect but no metrics

**Solution**: Check server terminal for:
- "Debug: Received X metric entries" messages
- If you see "Warning: No metrics received" → Client evaluate() might have issues

### Issue: "Connection refused"

**Solution**:
1. Make sure server started FIRST
2. Wait 5 seconds after server starts
3. Check server shows "Waiting for clients to connect..."
4. Verify both are in same directory

### Issue: Only one client connects

**Solution**:
- Check if both client threads started
- Look for error messages in client terminal
- Make sure server `min_fit_clients=2` is set correctly

---

## Files Generated

After successful completion:
- ✅ `server_accuracy.png` - Server aggregated accuracy
- ✅ `client_accuracy.png` - Client individual accuracies

---

**All connection issues have been fixed. Follow these instructions carefully!**






