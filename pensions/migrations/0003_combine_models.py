# Generated by Django 2.2.2 on 2019-07-09 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pensions', '0002_revise_fund'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefit',
            name='final_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='benefit',
            name='first_name',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benefit',
            name='last_name',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='benefit',
            name='years_of_service',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Beneficiary',
        ),
    ]
