"""
Management Command to Populate Sample Data

This command creates sample users and financial records for testing.

Usage:
    python manage.py populate_sample_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from users.models import User
from records.models import FinancialRecord


class Command(BaseCommand):
    """
    Management command to populate database with sample data.
    
    Creates:
    - 3 test users (admin, analyst, viewer)
    - 50 sample financial records
    - Mix of income and expense transactions
    
    Usage:
        python manage.py populate_sample_data
    """
    
    help = 'Populate database with sample users and financial records for testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        FinancialRecord.objects.all().delete()
        User.objects.filter(username__in=['admin', 'analyst_user', 'viewer_user']).delete()
        
        # Create sample users
        self.stdout.write('Creating sample users...')
        
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        analyst_user = User.objects.create_user(
            username='analyst_user',
            email='analyst@example.com',
            password='analyst123',
            first_name='Analyst',
            last_name='User',
            role='analyst'
        )
        
        viewer_user = User.objects.create_user(
            username='viewer_user',
            email='viewer@example.com',
            password='viewer123',
            first_name='Viewer',
            last_name='User',
            role='viewer'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Created 3 test users'))
        self.print_users(admin_user, analyst_user, viewer_user)
        
        # Create sample financial records
        self.stdout.write('\nCreating sample financial records...')
        
        # Income categories
        income_categories = [
            ('salary', 'Salary'),
            ('freelance', 'Freelance'),
            ('investment', 'Investment Returns'),
            ('business', 'Business Income'),
            ('other_income', 'Other Income'),
        ]
        
        # Expense categories
        expense_categories = [
            ('food', 'Food & Dining'),
            ('transport', 'Transportation'),
            ('utilities', 'Utilities'),
            ('rent', 'Rent/Mortgage'),
            ('healthcare', 'Healthcare'),
            ('entertainment', 'Entertainment'),
            ('shopping', 'Shopping'),
            ('education', 'Education'),
            ('travel', 'Travel'),
            ('insurance', 'Insurance'),
        ]
        
        # Create income records
        income_amounts = [5000, 3500, 2000, 1500, 800, 600, 450, 300]
        for i, amount in enumerate(income_amounts):
            category_key, category_name = income_categories[i % len(income_categories)]
            date = timezone.now().date() - timedelta(days=i * 7)
            
            FinancialRecord.objects.create(
                amount=Decimal(str(amount)),
                record_type='income',
                category=category_key,
                date=date,
                description=f'{category_name} payment',
                notes=f'Sample income record #{i+1}',
                created_by=admin_user if i % 2 == 0 else analyst_user
            )
        
        # Create expense records
        expense_amounts = [1200, 800, 650, 500, 450, 380, 320, 280, 250, 200, 180, 150, 120, 100, 80]
        for i, amount in enumerate(expense_amounts):
            category_key, category_name = expense_categories[i % len(expense_categories)]
            date = timezone.now().date() - timedelta(days=i * 5)
            
            FinancialRecord.objects.create(
                amount=Decimal(str(amount)),
                record_type='expense',
                category=category_key,
                date=date,
                description=f'{category_name} expense',
                notes=f'Sample expense record #{i+1}',
                created_by=admin_user if i % 3 == 0 else analyst_user
            )
        
        # Create some records for viewer
        for i in range(5):
            FinancialRecord.objects.create(
                amount=Decimal(str(500 + i * 100)),
                record_type='expense',
                category='shopping',
                date=timezone.now().date() - timedelta(days=i * 3),
                description=f'Personal shopping {i+1}',
                notes=f'Viewer personal expense',
                created_by=viewer_user
            )
        
        total_records = FinancialRecord.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {total_records} financial records'))
        
        # Print summary
        self.print_summary()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data population completed!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Login Credentials:'))
        self.stdout.write(self.style.WARNING('  Admin:    username=admin, password=admin123'))
        self.stdout.write(self.style.WARNING('  Analyst:  username=analyst_user, password=analyst123'))
        self.stdout.write(self.style.WARNING('  Viewer:   username=viewer_user, password=viewer123'))
    
    def print_users(self, admin, analyst, viewer):
        """Print created user details."""
        self.stdout.write('\n📋 Users Created:')
        self.stdout.write(f'  👑 Admin:   {admin.username} ({admin.email})')
        self.stdout.write(f'  📊 Analyst: {analyst.username} ({analyst.email})')
        self.stdout.write(f'  👁️  Viewer:  {viewer.username} ({viewer.email})')
    
    def print_summary(self):
        """Print data summary."""
        from django.db.models import Sum
        
        total_income = FinancialRecord.objects.filter(record_type='income').count()
        total_expense = FinancialRecord.objects.filter(record_type='expense').count()
        total_amount_income = FinancialRecord.objects.filter(record_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_amount_expense = FinancialRecord.objects.filter(record_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  Total Records: {FinancialRecord.objects.count()}')
        self.stdout.write(f'  Income Records: {total_income} (${total_amount_income:,.2f})')
        self.stdout.write(f'  Expense Records: {total_expense} (${total_amount_expense:,.2f})')
        self.stdout.write(f'  Net Balance: ${total_amount_income - total_amount_expense:,.2f}')
