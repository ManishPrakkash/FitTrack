"""
Script to reset migrations and create a fresh database.
"""
import os
import shutil
import subprocess

def run_command(command):
    """Run a command and print the output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def main():
    """Main function to reset migrations."""
    # Delete the database
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("Deleted db.sqlite3")

    # Delete migration files
    apps = ['authentication', 'challenges', 'activities']
    for app in apps:
        migrations_dir = os.path.join(app, 'migrations')
        if os.path.exists(migrations_dir):
            # Keep __init__.py
            init_file = os.path.join(migrations_dir, '__init__.py')
            has_init = os.path.exists(init_file)
            
            # Remove all files in the directory
            for filename in os.listdir(migrations_dir):
                if filename != '__init__.py':
                    file_path = os.path.join(migrations_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
            
            # Create __init__.py if it doesn't exist
            if not has_init:
                with open(init_file, 'w') as f:
                    pass
                print(f"Created {init_file}")

    # Create new migrations
    for app in apps:
        if not run_command(f"python manage.py makemigrations {app}"):
            print(f"Failed to create migrations for {app}")
            return

    # Apply migrations
    if not run_command("python manage.py migrate"):
        print("Failed to apply migrations")
        return

    print("Migrations reset successfully!")

if __name__ == "__main__":
    main()
