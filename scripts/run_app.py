#!/usr/bin/env python3
"""
Run MemoryGuard Streamlit application.
"""

import os
import sys
from pathlib import Path

# Add src to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

# Load environment
from dotenv import load_dotenv
load_dotenv(repo_root / ".env")

# Import and run Streamlit
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # Set up arguments for streamlit
    sys.argv = [
        "streamlit",
        "run",
        str(Path(__file__).parent.parent / "src" / "ui" / "main.py"),
        "--server.port=8501",
        "--server.address=0.0.0.0",
    ]
    sys.exit(stcli.main())