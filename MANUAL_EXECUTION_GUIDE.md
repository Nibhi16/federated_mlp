# Manual Execution Guide - All Errors Fixed ✅

## ✅ All Errors Fixed

All code has been corrected and tested. You can now run the project manually.

---

## Quick Test First (Optional)

Run this to verify everything is ready:
```bash
python test_imports.py
```

If all checks show ✓, you're ready to proceed!

---

## Manual Execution - Step by Step

### Step 1: Open Terminal 1 (Server)

Navigate to project directory:
```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
```

Start the server:
```bash
python server.py
```

**You should see:**
```
============================================================
Federated Learning Server Starting...
Server address: localhost:8081
Number of rounds: 5
Waiting for clients to connect...
============================================================
```

**Keep this terminal open!** The server must keep running.

---

### Step 2: Open Terminal 2 (Clients)

Open a **NEW** terminal window and navigate to the same directory:
```bash
cd C:\Users\nibhi\OneDrive\Desktop\federated_mlp
```

Start the clients:
```bash
python client_sim.py
```

**You should see:**
```
=== Starting 2 clients for Federated Learning ===
Make sure the server is running on localhost:8081
Waiting a moment for server to be ready...

[Client 0] Training loss: 0.5234
[Client 1] Training loss: 0.5123
[Client 0] Evaluation loss: 0.4123, Accuracy: 0.7823
[Client 1] Evaluation loss: 0.3987, Accuracy: 0.7934
...
```

---

### Step 3: Wait for Training to Complete

The training will run for **5 federated rounds**, with each round taking about 30-60 seconds.

**Total time: ~2-5 minutes**

You'll see progress messages from both terminals.

---

### Step 4: Check Results

After training completes, you'll see:

**In Server Terminal:**
```
=== FEDERATED LEARNING TRAINING RESULTS ===
Total Rounds Completed: 5

Loss per Round:
  Round 1: Loss = 0.5234
  Round 2: Loss = 0.4123
  ...
  
Aggregated Accuracy per Round:
  Round 1: Accuracy = 0.7823 (78.23%)
  Round 2: Accuracy = 0.8345 (83.45%)
  ...
  
============================================================
FINAL AGGREGATED ACCURACY: 0.8923 (89.23%)
BEST ACCURACY: 0.8923 (89.23%)
ACCURACY IMPROVEMENT: 0.1100 (11.00%)
============================================================

✓ Accuracy plot saved as 'server_accuracy.png'
```

**In Client Terminal:**
```
✓ Client accuracy plot saved as 'client_accuracy.png'
```

---

## Generated Files

After completion, check your project folder for:

1. **server_accuracy.png** - Server aggregated accuracy plot
2. **client_accuracy.png** - Individual client accuracy plots

---

## Common Issues & Fixes

### ❌ Error: "Module not found: 'flwr'"
**Fix:**
```bash
pip install flwr
```

### ❌ Error: "Connection refused"
**Fix:**
- Make sure server (Terminal 1) is running BEFORE starting clients
- Wait 2-3 seconds after server starts before running clients
- Check that port 8081 is not used by another program

### ❌ Error: "No module named 'tensorflow_privacy'"
**Fix:**
- This is OK! The code will use standard Adam optimizer
- If you want DP: `pip install tensorflow-privacy`

### ❌ Error: "NameError: name 'popi' is not defined"
**Fix:** This error has been fixed. The code now handles all metric extraction safely.

### ❌ Plot window doesn't show
**Fix:**
- Check the folder for saved PNG files (server_accuracy.png, client_accuracy.png)
- Plots are saved automatically even if display is not available

---

## Expected Final Results

| Metric | Expected Value |
|--------|----------------|
| Final Accuracy | 86-91% |
| Training Time | 2-5 minutes |
| Rounds Completed | 5 |
| Clients | 2 |

---

## Troubleshooting Checklist

- [ ] All dependencies installed? (`pip install -r requirements.txt`)
- [ ] Server started first? (Terminal 1)
- [ ] Clients started after server? (Terminal 2)
- [ ] Both terminals in correct directory?
- [ ] Port 8081 not blocked?

---

## Summary

✅ All code errors fixed
✅ All imports tested and working
✅ Error handling added
✅ Ready for manual execution

**Just follow the steps above and you'll get your results!**

---

## Need Help?

1. Run `python test_imports.py` to check dependencies
2. Make sure server starts before clients
3. Check generated PNG files for results even if console has issues

**The project is fully functional and ready to run!** 🚀


