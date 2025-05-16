"""
Script to examine the djongo base.py file structure.
"""
import os
import sys
import inspect

def examine_djongo_base():
    """Examine the djongo base.py file structure."""
    try:
        # Try to import djongo
        import djongo.base
        # Get the file path
        file_path = inspect.getfile(djongo.base)
        print(f"Found djongo base.py at: {file_path}")
        
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for the _close method
        if "def _close(self):" in content:
            print("Found _close method in djongo base.py")
            
            # Extract the _close method
            start_idx = content.find("def _close(self):")
            end_idx = content.find("def ", start_idx + 1)
            if end_idx == -1:
                end_idx = len(content)
            
            close_method = content[start_idx:end_idx].strip()
            print("\nCurrent _close method:")
            print(close_method)
            
            # Check if the method contains the problematic code
            if "if self.connection:" in close_method:
                print("\nFound problematic code: 'if self.connection:'")
            else:
                print("\nDid not find 'if self.connection:' in _close method")
                
            # Print the entire method for manual inspection
            print("\nPlease use this information to update the patch_djongo.py script.")
            
            return True
        else:
            print("Error: Could not find _close method in djongo base.py")
            return False
            
    except ImportError:
        print("Error: djongo package not found. Make sure it's installed.")
        return False
    except Exception as e:
        print(f"Error examining djongo base.py: {e}")
        return False

if __name__ == "__main__":
    examine_djongo_base()
