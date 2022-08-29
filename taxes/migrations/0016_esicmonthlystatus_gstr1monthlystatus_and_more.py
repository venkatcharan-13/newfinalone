# Generated by Django 4.0.5 on 2022-08-29 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_rename_client_id_client_client_and_more'),
        ('taxes', '0015_incometaxmonthlystatus_incometaxquarterlystatus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ESICMonthlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.CreateModel(
            name='GSTR1MonthlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.CreateModel(
            name='GSTR3BMonthlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.CreateModel(
            name='GSTR8MonthlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeTaxAdvanceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter', models.CharField(choices=[('Q1', 'Apr-Jun'), ('Q2', 'Jul-Sep'), ('Q3', 'Oct-Dec'), ('Q4', 'Jan-Mar')], default='Apr-Jun', max_length=20)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProvidentFundMonthlyStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4)),
                ('year', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2022)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.RemoveField(
            model_name='gstquarterlystatus',
            name='client',
        ),
        migrations.RemoveField(
            model_name='othertaxesmonthlystatus',
            name='client',
        ),
        migrations.RemoveField(
            model_name='othertaxesquarterlystatus',
            name='client',
        ),
        migrations.AlterField(
            model_name='incometaxmonthlystatus',
            name='month_name',
            field=models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], default=4),
        ),
        migrations.AlterField(
            model_name='incometaxmonthlystatus',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30),
        ),
        migrations.AlterField(
            model_name='incometaxquarterlystatus',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('action_required', 'Client Action Required'), ('not_applicable', 'Not Applicable'), ('done', 'Done')], default='not_applicable', max_length=30),
        ),
        migrations.AlterField(
            model_name='taxalert',
            name='tax_type',
            field=models.CharField(choices=[('income_tax', 'Income Tax'), ('gst', 'GST'), ('other_compliances', 'Other Compliances')], default='income_tax', max_length=20),
        ),
        migrations.DeleteModel(
            name='GSTMonthlyStatus',
        ),
        migrations.DeleteModel(
            name='GSTQuarterlyStatus',
        ),
        migrations.DeleteModel(
            name='OtherTaxesMonthlyStatus',
        ),
        migrations.DeleteModel(
            name='OtherTaxesQuarterlyStatus',
        ),
    ]
