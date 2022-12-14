# Generated by Django 4.0.5 on 2022-07-15 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0002_incometaxmonthlystatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ITQuarterlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(max_length=20)),
                ('paymentStatus', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('quaity_check', 'Quality Check'), ('done', 'Completed')], default='Pending', max_length=30)),
            ],
        ),
        migrations.RenameModel(
            old_name='TaxAlert',
            new_name='IncomeTaxAlert',
        ),
        migrations.RenameModel(
            old_name='IncomeTaxMonthlyStatus',
            new_name='ITMonthlyStatus',
        ),
    ]
