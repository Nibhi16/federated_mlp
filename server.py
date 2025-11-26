import flwr as fl
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

NUM_ROUNDS = 5

# Collect aggregated metrics
aggregated_losses = []
aggregated_accuracies = []

def fit_config(server_round: int):
    """Return training configuration dict for each round."""
    print(f"\n[Server] Starting Round {server_round} - Waiting for clients to train...")
    config = {
        "server_round": server_round,
    }
    return config

def evaluate_config(server_round: int):
    """Return evaluation configuration dict for each round."""
    print(f"[Server] Round {server_round} - Requesting evaluation from clients...")
    config = {
        "server_round": server_round,
    }
    return config

# Custom strategy to collect aggregated metrics
def aggregate_metrics(metrics):
    """Aggregate client metrics."""
    if not metrics:
        print("Warning: No metrics received for aggregation")
        return {}
    
    try:
        # Metrics format: list of (num_examples, metrics_dict)
        print(f"Debug: Received {len(metrics)} metric entries")
        accuracies = []
        weights = []
        
        for num_examples, metrics_dict in metrics:
            if isinstance(metrics_dict, dict) and "accuracy" in metrics_dict:
                accuracies.append(metrics_dict["accuracy"])
                weights.append(num_examples)
            else:
                print(f"Warning: Unexpected metrics format: {metrics_dict}")
        
        if len(accuracies) > 0 and sum(weights) > 0:
            aggregated_accuracy = sum(acc * w for acc, w in zip(accuracies, weights)) / sum(weights)
            print(f"Debug: Aggregated accuracy: {aggregated_accuracy:.4f}")
            return {"accuracy": aggregated_accuracy}
        else:
            print("Warning: Could not calculate aggregated accuracy")
            return {}
    except Exception as e:
        print(f"Error in aggregate_metrics: {e}")
        import traceback
        traceback.print_exc()
        return {}

# Strategy with callbacks to track progress
strategy = fl.server.strategy.FedAvg(
    fraction_fit=1.0,  # all clients participate
    fraction_evaluate=1.0,  # all clients participate in evaluation
    min_fit_clients=2,
    min_evaluate_clients=2,  # Changed from min_eval_clients
    min_available_clients=2,
    on_fit_config_fn=fit_config,
    on_evaluate_config_fn=evaluate_config,
    evaluate_metrics_aggregation_fn=aggregate_metrics,
)

print("Strategy configured:")
print(f"  - Min fit clients: {strategy.min_fit_clients}")
print(f"  - Min evaluate clients: {strategy.min_evaluate_clients}")
print(f"  - Fraction fit: {strategy.fraction_fit}")
print(f"  - Fraction evaluate: {strategy.fraction_evaluate}\n")

# Start server
print("=" * 60)
print("Federated Learning Server Starting...")
print(f"Server address: 0.0.0.0:8081")
print(f"Number of rounds: {NUM_ROUNDS}")
print("Waiting for clients to connect...")
print("=" * 60 + "\n")

try:
    history = fl.server.start_server(
        server_address="0.0.0.0:8081",
        config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
        strategy=strategy
    )
except Exception as e:
    print(f"\nERROR: Server failed to start: {e}")
    import traceback
    traceback.print_exc()
    history = None

# Extract metrics from history
if history:
    # Extract loss and accuracy from history
    losses_distributed = history.losses_distributed
    metrics_distributed = history.metrics_distributed
    
    print("\n" + "=" * 60)
    print("=== FEDERATED LEARNING TRAINING RESULTS ===")
    print("=" * 60)
    print(f"Total Rounds Completed: {len(losses_distributed)}")
    print(f"\nLoss per Round:")
    print("-" * 60)
    
    for round_num, loss_data in enumerate(losses_distributed, 1):
        try:
            if isinstance(loss_data, tuple):
                loss = loss_data[0]
            else:
                loss = loss_data
            print(f"  Round {round_num}: Loss = {loss:.4f}")
        except Exception as e:
            print(f"  Round {round_num}: Loss = {loss_data} (parsing error: {e})")
    
    # Extract accuracy if available
    accuracies = []
    if metrics_distributed and "accuracy" in metrics_distributed:
        try:
            # Handle different possible structures of metrics
            accuracy_metrics = metrics_distributed["accuracy"]
            for metric_tuple in accuracy_metrics:
                if isinstance(metric_tuple, tuple):
                    if len(metric_tuple) == 2:
                        # Format: (round, (value, num_examples))
                        _, (acc_val, _) = metric_tuple
                        accuracies.append(acc_val)
                    else:
                        # Format might be different
                        acc = metric_tuple[1] if len(metric_tuple) > 1 else metric_tuple[0]
                        accuracies.append(acc)
                else:
                    accuracies.append(metric_tuple)
        except Exception as e:
            print(f"Warning: Could not parse accuracy metrics: {e}")
            print(f"Metrics structure: {metrics_distributed.get('accuracy', 'N/A')}")
            accuracies = []
    
    if accuracies:
        print(f"\nAggregated Accuracy per Round:")
        print("-" * 60)
        for round_num, acc in enumerate(accuracies, 1):
            print(f"  Round {round_num}: Accuracy = {acc:.4f} ({acc*100:.2f}%)")
        
        print(f"\n{'=' * 60}")
        print(f"FINAL AGGREGATED ACCURACY: {accuracies[-1]:.4f} ({accuracies[-1]*100:.2f}%)")
        print(f"BEST ACCURACY: {max(accuracies):.4f} ({max(accuracies)*100:.2f}%)")
        if len(accuracies) > 1:
            print(f"ACCURACY IMPROVEMENT: {accuracies[-1] - accuracies[0]:.4f} ({((accuracies[-1] - accuracies[0])*100):.2f}%)")
        print("=" * 60)
        
        # Plot server metrics
        rounds = list(range(1, len(accuracies) + 1))
        
        plt.figure(figsize=(10, 6))
        plt.plot(rounds, accuracies, marker='o', label='Server Global Accuracy', linewidth=2, markersize=8)
        plt.title("Federated Learning: Server Aggregated Accuracy per Round", fontsize=14, fontweight='bold')
        plt.xlabel("Federated Round", fontsize=12)
        plt.ylabel("Accuracy", fontsize=12)
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig("server_accuracy.png", dpi=300, bbox_inches='tight')
        print("\n✓ Accuracy plot saved as 'server_accuracy.png'")
        plt.close()  # Close figure to free memory
    else:
        print("\n⚠ Note: Accuracy metrics not available.")
        print("Debug information:")
        print(f"  - Metrics distributed exists: {metrics_distributed is not None}")
        if metrics_distributed:
            print(f"  - Available metrics keys: {list(metrics_distributed.keys())}")
        print("\nThis may happen if:")
        print("  1. Clients didn't return accuracy metrics in evaluate()")
        print("  2. Metrics aggregation function had issues")
        print("  3. Clients didn't complete evaluation phase")
        
        # Try to get any available metrics
        if metrics_distributed:
            print("\nAvailable metrics:")
            for key, value in metrics_distributed.items():
                print(f"  - {key}: {value}")
else:
    print("\nNo training history available.")
    print("The server may have exited before collecting metrics.")
