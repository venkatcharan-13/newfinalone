# Generated by Django 4.0.5 on 2022-08-03 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0007_alter_gstmonthlystatus_monthname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gstmonthlystatus',
            old_name='monthName',
            new_name='month_name',
        ),
        migrations.RenameField(
            model_name='gstmonthlystatus',
            old_name='paymentStatus',
            new_name='payment_status',
        ),
        migrations.RenameField(
            model_name='gstquarterlystatus',
            old_name='paymentStatus',
            new_name='payment_status',
        ),
        migrations.RenameField(
            model_name='itmonthlystatus',
            old_name='monthName',
            new_name='month_name',
        ),
        migrations.RenameField(
            model_name='itmonthlystatus',
            old_name='paymentStatus',
            new_name='payment_status',
        ),
        migrations.RenameField(
            model_name='itquarterlystatus',
            old_name='paymentStatus',
            new_name='payment_status',
        ),
        migrations.RenameField(
            model_name='taxalert',
            old_name='dueDate',
            new_name='due_date',
        ),
        migrations.RenameField(
            model_name='taxalert',
            old_name='raisedOn',
            new_name='raised_on',
        ),
        migrations.RenameField(
            model_name='taxalert',
            old_name='taxType',
            new_name='tax_type',
        ),
    ]
