#!/usr/bin/env python3
"""
Convenience script to run federated learning with server and clients.
This script starts the server and clients in separate processes.
"""

import subprocess
import sys
import time
import os

def main():
    print("=" * 60)
    print("Federated Learning with Privacy Preservation")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Start the Flower server")
    print("2. Start multiple clients for federated training")
    print("\nNote: Press Ctrl+C to stop all processes\n")
    
    # Check if files exist
    if not os.path.exists("server.py"):
        print("Error: server.py not found!")
        sys.exit(1)
    if not os.path.exists("client_sim.py"):
        print("Error: client_sim.py not found!")
        sys.exit(1)
    
    try:
        # Start server in background
        print("Starting server...")
        server_process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is still running
        if server_process.poll() is not None:
            print("Error: Server failed to start!")
            stdout, stderr = server_process.communicate()
            print("Server output:", stdout.decode())
            print("Server errors:", stderr.decode())
            sys.exit(1)
        
        print("Server started successfully!")
        print("Starting clients...\n")
        
        # Start clients (this will block until training completes)
        client_process = subprocess.Popen(
            [sys.executable, "client_sim.py"],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        # Wait for clients to finish
        client_process.wait()
        
        print("\n" + "=" * 60)
        print("Federated Learning Training Complete!")
        print("=" * 60)
        print("\nCheck the generated plots:")
        print("- client_accuracy.png")
        print("- server_accuracy.png")
        
    except KeyboardInterrupt:
        print("\n\nStopping all processes...")
        if 'server_process' in locals():
            server_process.terminate()
        if 'client_process' in locals():
            client_process.terminate()
        print("All processes stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        if 'server_process' in locals():
            server_process.terminate()
        if 'client_process' in locals():
            client_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()


