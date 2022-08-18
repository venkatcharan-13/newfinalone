# Generated by Django 4.0.5 on 2022-08-18 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_client_zoho_client_id_client_zoho_client_secret_and_more'),
        ('accounts', '0035_alter_zohoaccount_account_for_coding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratio',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client'),
        ),
        migrations.AlterField(
            model_name='zohoaccount',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client'),
        ),
    ]
