from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check and fix admin user status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Fix inactive admin users',
        )

    def handle(self, *args, **options):
        self.stdout.write('Checking admin users...')
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            self.stdout.write(f'\nUser: {user.username}')
            self.stdout.write(f'  Is active: {user.is_active}')
            self.stdout.write(f'  Is staff: {user.is_staff}')
            self.stdout.write(f'  Is superuser: {user.is_superuser}')
            self.stdout.write(f'  Date joined: {user.date_joined}')
            self.stdout.write(f'  Last login: {user.last_login}')
            
            # Check if user should be admin but isn't
            if user.is_staff or user.is_superuser:
                if not user.is_active:
                    self.stdout.write(
                        self.style.WARNING(f'  WARNING: Admin user {user.username} is inactive!')
                    )
                    
                    if options['fix']:
                        user.is_active = True
                        user.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'  FIXED: Activated user {user.username}')
                        )
        
        if options['fix']:
            self.stdout.write(
                self.style.SUCCESS('\nAdmin user status check and fix completed')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\nAdmin user status check completed')
            )
            self.stdout.write(
                'Run with --fix to automatically activate inactive admin users'
            ) 