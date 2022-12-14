# Generated by Django 4.0.5 on 2022-07-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0006_gstmonthlystatus_client_gstquarterlystatus_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gstmonthlystatus',
            name='monthName',
            field=models.CharField(choices=[('january', 'Jan'), ('february', 'Feb'), ('march', 'Mar'), ('april', 'Apr'), ('may', 'May'), ('june', 'Jun'), ('july', 'Jul'), ('august', 'Aug'), ('september', 'Sep'), ('october', 'Oct'), ('november', 'Nov'), ('december', 'Dec')], default='Jan', max_length=20),
        ),
        migrations.AlterField(
            model_name='gstquarterlystatus',
            name='quarter',
            field=models.CharField(choices=[('january', 'Jan-Mar'), ('april', 'Apr-Jun'), ('july', 'Jul-Sep'), ('october', 'Oct-Dec')], default='Jan-Mar', max_length=20),
        ),
        migrations.AlterField(
            model_name='itmonthlystatus',
            name='monthName',
            field=models.CharField(choices=[('january', 'Jan'), ('february', 'Feb'), ('march', 'Mar'), ('april', 'Apr'), ('may', 'May'), ('june', 'Jun'), ('july', 'Jul'), ('august', 'Aug'), ('september', 'Sep'), ('october', 'Oct'), ('november', 'Nov'), ('december', 'Dec')], default='Jan', max_length=20),
        ),
        migrations.AlterField(
            model_name='itquarterlystatus',
            name='quarter',
            field=models.CharField(choices=[('january', 'Jan-Mar'), ('april', 'Apr-Jun'), ('july', 'Jul-Sep'), ('october', 'Oct-Dec')], default='Jan-Mar', max_length=20),
        ),
    ]
