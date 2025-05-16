"""
Direct fix for djongo connection handling.
This script directly modifies the Database class in pymongo to fix the bool issue.
"""
import sys

def fix_pymongo_database():
    """Fix the pymongo Database class to handle bool operations."""
    try:
        import pymongo.database
        
        # Check if already patched
        if hasattr(pymongo.database.Database, '__bool__'):
            original_bool = pymongo.database.Database.__bool__
            if 'return True  # Patched for FitTrack' in original_bool.__code__.co_consts:
                print("pymongo.database.Database already patched.")
                return True
        
        # Define a new __bool__ method
        def patched_bool(self):
            return True  # Patched for FitTrack
        
        # Apply the patch
        pymongo.database.Database.__bool__ = patched_bool
        
        print("Successfully patched pymongo.database.Database.__bool__")
        return True
    except Exception as e:
        print(f"Error patching pymongo.database.Database: {e}")
        return False

if __name__ == "__main__":
    success = fix_pymongo_database()
    if not success:
        sys.exit(1)
    sys.exit(0)
