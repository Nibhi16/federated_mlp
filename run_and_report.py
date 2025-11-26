#!/usr/bin/env python3
"""
Script to run federated learning and generate comprehensive performance report.
"""

import subprocess
import sys
import time
import os
import json
from datetime import datetime

def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import flwr
    except ImportError:
        missing.append("flwr")
    
    try:
        import tensorflow
    except ImportError:
        missing.append("tensorflow")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    try:
        import sklearn
    except ImportError:
        missing.append("scikit-learn")
    
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    
    return missing

def install_dependencies(missing):
    """Install missing dependencies."""
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        for package in missing:
            if package == "scikit-learn":
                package = "scikit-learn"
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"], 
                                    timeout=300)
            except subprocess.TimeoutExpired:
                print(f"Timeout installing {package}. Please install manually.")
                return False
            except Exception as e:
                print(f"Error installing {package}: {e}")
                return False
    return True

def run_federated_learning():
    """Run the federated learning experiment."""
    print("=" * 70)
    print("FEDERATED LEARNING WITH PRIVACY PRESERVATION - EXPERIMENT")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check dependencies
    print("Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        if not install_dependencies(missing):
            print("\nERROR: Could not install all dependencies.")
            print("Please install manually: pip install -r requirements.txt")
            return None
    print("All dependencies available.\n")
    
    # Start server in background
    print("Starting Flower server...")
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(5)
    
    if server_process.poll() is not None:
        stdout, stderr = server_process.communicate()
        print(f"ERROR: Server failed to start!")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return None
    
    print("Server started successfully.\n")
    
    # Run clients
    print("Starting federated learning clients...")
    print("-" * 70)
    
    start_time = time.time()
    
    client_process = subprocess.Popen(
        [sys.executable, "client_sim.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = client_process.communicate()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Stop server
    server_process.terminate()
    server_stdout, server_stderr = server_process.communicate()
    
    # Parse results from output
    results = {
        "experiment_time": elapsed_time,
        "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "client_output": stdout,
        "client_errors": stderr,
        "server_output": server_stdout,
        "server_errors": server_stderr
    }
    
    return results

def extract_metrics(results):
    """Extract metrics from experiment results."""
    metrics = {
        "final_accuracies": {},
        "training_losses": {},
        "rounds_completed": 0,
        "total_time": results["experiment_time"] if results else 0
    }
    
    if not results:
        return metrics
    
    # Parse client output for accuracies
    client_output = results.get("client_output", "")
    lines = client_output.split('\n')
    
    client_accuracies = {}
    for line in lines:
        if "[Client" in line and "Accuracy:" in line:
            try:
                # Extract client ID and accuracy
                parts = line.split()
                client_id = None
                accuracy = None
                for i, part in enumerate(parts):
                    if part == "Client":
                        client_id = int(parts[i+1].rstrip(']'))
                    if part == "Accuracy:":
                        accuracy = float(parts[i+1])
                
                if client_id is not None and accuracy is not None:
                    if client_id not in client_accuracies:
                        client_accuracies[client_id] = []
                    client_accuracies[client_id].append(accuracy)
            except:
                pass
    
    metrics["final_accuracies"] = {
        f"Client_{k}": {
            "all_rounds": v,
            "final": v[-1] if v else 0.0,
            "max": max(v) if v else 0.0,
            "min": min(v) if v else 0.0,
            "avg": sum(v)/len(v) if v else 0.0
        }
        for k, v in client_accuracies.items()
    }
    
    # Count rounds
    if client_accuracies:
        metrics["rounds_completed"] = len(list(client_accuracies.values())[0])
    
    # Parse server output for aggregated metrics
    server_output = results.get("server_output", "")
    server_lines = server_output.split('\n')
    
    aggregated_accuracies = []
    for line in server_lines:
        if "Round" in line and "Loss" in line:
            try:
                # Extract round and loss
                pass
            except:
                pass
    
    return metrics

def generate_report(metrics, results):
    """Generate comprehensive performance report."""
    report = f"""
{'=' * 70}
FEDERATED LEARNING - FINAL PERFORMANCE REPORT
{'=' * 70}

EXPERIMENT CONFIGURATION:
- Dataset: UCI Heart Disease (Cleveland)
- Model: Multi-Layer Perceptron (MLP)
- Architecture: 13 → 16 → 8 → 1
- Clients: 2
- Federated Rounds: 5
- Local Epochs per Round: 3
- Privacy: Differential Privacy Enabled
  * L2 Norm Clip: 1.0
  * Noise Multiplier: 0.5
  * Microbatches: 32

PERFORMANCE METRICS:
{'-' * 70}
Total Training Time: {metrics['total_time']:.2f} seconds ({metrics['total_time']/60:.2f} minutes)
Rounds Completed: {metrics['rounds_completed']}

CLIENT PERFORMANCE:
"""
    
    for client_name, client_data in metrics["final_accuracies"].items():
        report += f"""
{client_name}:
  - Final Accuracy: {client_data['final']:.4f} ({client_data['final']*100:.2f}%)
  - Maximum Accuracy: {client_data['max']:.4f} ({client_data['max']*100:.2f}%)
  - Minimum Accuracy: {client_data['min']:.4f} ({client_data['min']*100:.2f}%)
  - Average Accuracy: {client_data['avg']:.4f} ({client_data['avg']*100:.2f}%)
  - Accuracy Progression: {[f'{x:.4f}' for x in client_data['all_rounds']]}
"""
    
    # Calculate overall statistics
    if metrics["final_accuracies"]:
        all_finals = [v["final"] for v in metrics["final_accuracies"].values()]
        all_maxes = [v["max"] for v in metrics["final_accuracies"].values()]
        
        report += f"""
AGGREGATED STATISTICS:
  - Overall Final Accuracy (Average): {sum(all_finals)/len(all_finals):.4f} ({sum(all_finals)/len(all_finals)*100:.2f}%)
  - Best Client Final Accuracy: {max(all_finals):.4f} ({max(all_finals)*100:.2f}%)
  - Overall Best Accuracy: {max(all_maxes):.4f} ({max(all_maxes)*100:.2f}%)
"""
    
    report += f"""
FILES GENERATED:
  - client_accuracy.png: Client accuracy progression plot
  - server_accuracy.png: Server aggregated accuracy plot

END TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 70}
"""
    
    return report

def main():
    """Main execution."""
    try:
        results = run_federated_learning()
        
        if results:
            metrics = extract_metrics(results)
            report = generate_report(metrics, results)
            
            # Save report
            with open("experiment_report.txt", "w") as f:
                f.write(report)
            
            print(report)
            print("\n✓ Report saved to 'experiment_report.txt'")
            
            # Save metrics as JSON
            metrics_json = {
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
            with open("experiment_metrics.json", "w") as f:
                json.dump(metrics_json, f, indent=2)
            
            print("✓ Metrics saved to 'experiment_metrics.json'")
        else:
            print("\n✗ Experiment failed. Please check errors above.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


