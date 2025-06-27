from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import getpass
import re

class Command(BaseCommand):
    help = 'Create a secure admin user for the Content Automation Platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Admin username',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password (will prompt if not provided)',
        )

    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character")
        
        return True

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Creating secure admin user for Content Automation Platform')
        )
        
        # Get username
        username = options['username']
        if not username:
            username = input('Enter admin username: ').strip()
        
        if not username:
            self.stdout.write(
                self.style.ERROR('Username is required')
            )
            return
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User "{username}" already exists')
            )
            return
        
        # Get email
        email = options['email']
        if not email:
            email = input('Enter admin email: ').strip()
        
        if email:
            try:
                validate_email(email)
            except ValidationError:
                self.stdout.write(
                    self.style.ERROR('Invalid email format')
                )
                return
        else:
            self.stdout.write(
                self.style.WARNING('No email provided - admin user will be created without email')
            )
        
        # Get password
        password = options['password']
        if not password:
            while True:
                password = getpass.getpass('Enter admin password: ')
                password_confirm = getpass.getpass('Confirm admin password: ')
                
                if password != password_confirm:
                    self.stdout.write(
                        self.style.ERROR('Passwords do not match')
                    )
                    continue
                
                try:
                    self.validate_password(password)
                    break
                except ValidationError as e:
                    self.stdout.write(
                        self.style.ERROR(str(e))
                    )
                    continue
        
        # Create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{username}"')
            )
            self.stdout.write(
                self.style.SUCCESS('You can now log in to the admin interface')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            ) 