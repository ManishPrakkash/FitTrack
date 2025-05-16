import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result.returncode == 0

def main():
    """Main setup function"""
    print("Setting up FitTrack Django Backend...")
    
    # Create virtual environment
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run_command("python -m venv venv")
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        pip_cmd = ".\\venv\\Scripts\\pip"
        django_admin_cmd = ".\\venv\\Scripts\\django-admin"
    else:
        pip_cmd = "./venv/bin/pip"
        django_admin_cmd = "./venv/bin/django-admin"
    
    # Install requirements
    print("Installing dependencies...")
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    # Create Django project if it doesn't exist
    if not os.path.exists("fittrack_backend"):
        print("Creating Django project...")
        run_command(f"{django_admin_cmd} startproject fittrack_backend .")
    
    # Create apps if they don't exist
    if not os.path.exists("users"):
        print("Creating users app...")
        run_command(f"{django_admin_cmd} startapp users")
    
    if not os.path.exists("authentication"):
        print("Creating authentication app...")
        run_command(f"{django_admin_cmd} startapp authentication")
    
    print("Setup completed successfully!")
    print("\nTo start the development server:")
    if sys.platform == "win32":
        print("  .\\venv\\Scripts\\python manage.py runserver")
    else:
        print("  ./venv/bin/python manage.py runserver")

if __name__ == "__main__":
    main()
