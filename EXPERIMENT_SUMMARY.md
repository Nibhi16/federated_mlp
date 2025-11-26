# Experiment Summary - Quick Reference

## Quick Run Commands

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run experiment (2 terminals)
# Terminal 1:
python server.py

# Terminal 2:
python client_sim.py

# Or use automated runner:
python run_and_report.py
```

## Expected Output

After running, you should see:

1. **Console Output**:
   - Server startup messages
   - Client training progress per round
   - Final aggregated accuracy
   - Round-by-round metrics

2. **Generated Files**:
   - `server_accuracy.png` - Server aggregated accuracy plot
   - `client_accuracy.png` - Individual client accuracy plots
   - `experiment_report.txt` - Detailed text report (if using runner)
   - `experiment_metrics.json` - Structured metrics (if using runner)

## Typical Results

| Metric | Value Range |
|--------|-------------|
| Final Accuracy | 86-91% |
| Training Time | 2-5 minutes |
| Federated Rounds | 5 |
| Privacy (ε) | ~1-2 |

## Troubleshooting

- **Import errors**: Run `pip install -r requirements.txt`
- **Connection refused**: Make sure server starts before clients
- **DP not available**: Code falls back to standard Adam optimizer
- **Port conflicts**: Change port 8081 in server.py and client files

## Key Files

- `server.py` - FL server
- `client_sim.py` - Client simulation with DP
- `dataset.py` - Data loading
- `requirements.txt` - Dependencies


