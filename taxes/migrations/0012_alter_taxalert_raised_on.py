# Generated by Django 4.0.5 on 2022-08-10 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0011_alter_gstmonthlystatus_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxalert',
            name='raised_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
