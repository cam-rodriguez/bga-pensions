# Generated by Django 2.2.2 on 2019-07-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pensions', '0003_combine_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='pensionfund',
            name='fund_type',
            field=models.CharField(choices=[
                ('STATE', 'State'),
                ('COUNTY', 'County'),
                ('CHICAGO', 'Chicago Municipal'),
                ('DOWNSTATE', 'Downstate')
            ], default='STATE', max_length=256),
            preserve_default=False,
        ),
    ]
