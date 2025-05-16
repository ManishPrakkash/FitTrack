"""
Script to run the Django server with all necessary fixes.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_server():
    """Run the Django server with all necessary fixes."""
    try:
        # Get the current directory
        current_dir = Path(__file__).parent.absolute()

        # Apply pymongo fix
        print("Applying pymongo fix...")
        fix_script = os.path.join(current_dir, "fix_djongo.py")
        subprocess.run([sys.executable, fix_script], check=True)

        # Initialize database
        print("Initializing database...")
        init_script = os.path.join(current_dir, "init_db.py")
        subprocess.run([sys.executable, init_script], check=True)

        # Start the server
        print("Starting Django development server...")
        manage_script = os.path.join(current_dir, "manage.py")
        subprocess.run([sys.executable, manage_script, "runserver", "0.0.0.0:8000"], check=True)

        return True
    except Exception as e:
        print(f"Error running server: {e}")
        return False

if __name__ == "__main__":
    run_server()
