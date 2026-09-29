"""
Launch MemoryGuard FastAPI Backend Server.
"""

import uvicorn
import sys
from pathlib import Path

# Add workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    print("=" * 60)
    print("Starting MemoryGuard Backend API Server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
