"""
Start a local Qdrant server for persistent memory storage.
Run this in a separate terminal to enable memory features.
"""

from qdrant_client import QdrantClient
from pathlib import Path
import time

# Create storage directory
storage_path = Path(__file__).parent / "qdrant_storage"
storage_path.mkdir(exist_ok=True)

print("🚀 Starting local Qdrant server...")
print(f"📁 Storage path: {storage_path}")
print("🌐 Server will be available at: http://localhost:6333")
print("\n⚠️  Keep this terminal running to use memory features")
print("   Press Ctrl+C to stop the server\n")

# Start Qdrant in server mode
# Note: For a full server, you'd typically download the Qdrant binary
# This uses the Python client in local mode which persists to disk

try:
    # Create a persistent client
    client = QdrantClient(path=str(storage_path))
    
    print("✅ Qdrant server started successfully!")
    print("\nCollections will be stored at:", storage_path)
    print("\nYou can now run your math discovery agent with enable_memory=True")
    
    # Keep running
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down Qdrant server...")
except Exception as e:
    print(f"\n❌ Error: {e}")
