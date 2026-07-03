from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from products.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Creating new data...')

        # Create admin user
        User.objects.create_superuser(
            email='admin@pierinelli.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User'
        )
        self.stdout.write(self.style.SUCCESS('Admin user created.'))

        # Create worker user
        User.objects.create_user(
            email='worker@pierinelli.com',
            password='workerpassword',
            first_name='Worker',
            last_name='User',
            role='worker'
        )
        self.stdout.write(self.style.SUCCESS('Worker user created.'))

        # Create products
        Product.objects.create(
            name='Plancha de Acero 1',
            description='Plancha de acero de 1mm de espesor',
            height=1.2,
            width=2.4,
            price=150.00,
            stock=10
        )
        Product.objects.create(
            name='Plancha de Acero 2',
            description='Plancha de acero de 2mm de espesor',
            height=1.2,
            width=2.4,
            price=250.00,
            stock=5
        )
        self.stdout.write(self.style.SUCCESS('Products created.'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
