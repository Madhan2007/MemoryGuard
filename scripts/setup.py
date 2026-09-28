#!/usr/bin/env python3
"""
Setup script for MemoryGuard.

Run this after cloning to set up the development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, cwd: str = None):
    """Run command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True


def main():
    """Main setup function."""
    repo_root = Path(__file__).parent.parent
    
    print("🛡️ MemoryGuard Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Create virtual environment
    venv_path = repo_root / ".venv"
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", ".venv"], cwd=repo_root):
            return False
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment exists")
    
    # Determine pip path
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip"
        python_path = venv_path / "Scripts" / "python"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    # Upgrade pip
    print("📦 Upgrading pip...")
    run_command([str(pip_path), "install", "--upgrade", "pip"], cwd=repo_root)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if not run_command([str(pip_path), "install", "-r", "requirements.txt"], cwd=repo_root):
        return False
    
    # Install in development mode
    print("📦 Installing MemoryGuard in development mode...")
    if not run_command([str(pip_path), "install", "-e", ".[dev]"], cwd=repo_root):
        return False
    
    # Install pre-commit hooks
    print("🔧 Installing pre-commit hooks...")
    run_command([str(pip_path), "install", "pre-commit"], cwd=repo_root)
    run_command([str(python_path), "-m", "pre_commit", "install"], cwd=repo_root)
    
    # Copy .env.example to .env if not exists
    env_path = repo_root / ".env"
    env_example = repo_root / ".env.example"
    if not env_path.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_path)
        print("📝 Created .env from .env.example")
        print("⚠️  Please edit .env with your API keys!")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env with your API keys:")
    print("   - GROQ_API_KEY")
    print("   - HINDSIGHT_API_KEY")
    print("   - HINDSIGHT_BASE_URL")
    print("2. Activate virtual environment:")
    if sys.platform == "win32":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("3. Run the app:")
    print("   python scripts/run_app.py")
    print("   or: streamlit run src/ui/main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)