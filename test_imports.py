#!/usr/bin/env python3
"""
Quick test script to verify all imports work correctly.
Run this before running the main federated learning code.
"""

print("Testing imports...")
print("=" * 50)

try:
    import flwr as fl
    print("✓ flwr imported successfully")
except ImportError as e:
    print(f"✗ flwr import failed: {e}")
    print("  Install with: pip install flwr")

try:
    import tensorflow as tf
    print(f"✓ tensorflow imported successfully (version: {tf.__version__})")
except ImportError as e:
    print(f"✗ tensorflow import failed: {e}")
    print("  Install with: pip install tensorflow")

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")
    print("  Install with: pip install numpy")

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ pandas import failed: {e}")
    print("  Install with: pip install pandas")

try:
    import sklearn
    print("✓ scikit-learn imported successfully")
except ImportError as e:
    print(f"✗ scikit-learn import failed: {e}")
    print("  Install with: pip install scikit-learn")

try:
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except ImportError as e:
    print(f"✗ matplotlib import failed: {e}")
    print("  Install with: pip install matplotlib")

# Test tensorflow_privacy (optional)
try:
    from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasAdamOptimizer
    print("✓ tensorflow_privacy imported successfully (DP enabled)")
except ImportError:
    try:
        from tensorflow_privacy.privacy.optimizers import dp_optimizer_keras
        print("✓ tensorflow_privacy imported successfully (alternative path, DP enabled)")
    except ImportError:
        print("⚠ tensorflow_privacy not available (DP will be disabled)")
        print("  Install with: pip install tensorflow-privacy")

# Test dataset module
try:
    from dataset import load_data
    print("✓ dataset module imported successfully")
except ImportError as e:
    print(f"✗ dataset module import failed: {e}")

print("=" * 50)
print("Import test complete!")
print("\nIf all checks passed (✓), you're ready to run:")
print("  Terminal 1: python server.py")
print("  Terminal 2: python client_sim.py")


