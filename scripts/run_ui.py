"""
MemoryGuard Launch Script
Standard production entry: Starts the FastAPI API server on port 8000.
The React production frontend runs on http://localhost:5173 (via 'cd frontend && npm run dev').
"""

import subprocess
import sys
from pathlib import Path

script_dir = Path(__file__).parent
root_dir = script_dir.parent

if __name__ == "__main__":
    print("=" * 65)
    print("🧠 MEMORYGUARD — VERIFIED MEMORY FOR DEAL INTELLIGENCE AGENTS")
    print("=" * 65)
    print("Starting FastAPI Backend Server on http://localhost:8000...")
    print("To launch the React Production Frontend in another terminal:")
    print("  cd frontend")
    print("  npm run dev")
    print("  Open http://localhost:5173")
    print("=" * 65)
    
    import uvicorn
    sys.path.insert(0, str(root_dir))
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)