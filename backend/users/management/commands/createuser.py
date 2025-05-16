"""
Management command to create a user directly in MongoDB.
"""
from django.core.management.base import BaseCommand
from users.models import User
import getpass


class Command(BaseCommand):
    help = 'Creates a new user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='User email')
        parser.add_argument('--name', type=str, help='User name')
        parser.add_argument('--password', type=str, help='User password')
        parser.add_argument('--admin', action='store_true', help='Create admin user')

    def handle(self, *args, **options):
        email = options.get('email')
        name = options.get('name')
        password = options.get('password')
        is_admin = options.get('admin', False)

        # Interactive mode if arguments are missing
        if not email:
            email = input('Email: ')
        if not name:
            name = input('Name: ')
        if not password:
            password = getpass.getpass('Password: ')

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f'User with email {email} already exists'))
                return

            # Create user
            user_data = {
                'email': email,
                'name': name,
                'password': password,
            }
            
            if is_admin:
                user_data['is_staff'] = True
                user_data['is_superuser'] = True
                user = User.objects.create_superuser(**user_data)
                self.stdout.write(self.style.SUCCESS(f'Admin user {email} created successfully'))
            else:
                user = User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f'User {email} created successfully'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
