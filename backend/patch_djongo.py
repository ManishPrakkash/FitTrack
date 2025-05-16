"""
Patch script for djongo to fix connection handling issues.
"""
import os
import sys
import inspect
import importlib.util
from pathlib import Path

def find_djongo_base_path():
    """Find the path to the djongo base.py file."""
    try:
        # Try to import djongo
        import djongo.base
        # Get the file path
        file_path = inspect.getfile(djongo.base)
        return file_path
    except ImportError:
        print("Error: djongo package not found. Make sure it's installed.")
        return None
    except Exception as e:
        print(f"Error finding djongo base.py: {e}")
        return None

def patch_djongo_base():
    """Patch the djongo base.py file to fix connection handling."""
    base_path = find_djongo_base_path()
    if not base_path:
        return False
    
    print(f"Found djongo base.py at: {base_path}")
    
    # Read the file
    with open(base_path, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if "# PATCHED FOR FITTRACK" in content:
        print("djongo base.py already patched.")
        return True
    
    # Find the _close method
    if "def _close(self):" not in content:
        print("Error: Could not find _close method in djongo base.py")
        return False
    
    # Replace the problematic code
    old_code = """    def _close(self):
        if self.connection:
            self.connection.close()"""
    
    new_code = """    def _close(self):
        # PATCHED FOR FITTRACK
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()"""
    
    if old_code not in content:
        print("Error: Could not find the exact code to patch in djongo base.py")
        return False
    
    # Apply the patch
    patched_content = content.replace(old_code, new_code)
    
    # Write the patched file
    with open(base_path, 'w') as f:
        f.write(patched_content)
    
    print("Successfully patched djongo base.py")
    return True

if __name__ == "__main__":
    success = patch_djongo_base()
    if not success:
        sys.exit(1)
    sys.exit(0)
