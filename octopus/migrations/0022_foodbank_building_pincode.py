# Generated by Django 3.2.5 on 2021-10-24 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('octopus', '0021_remove_foodbank_building_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodbank',
            name='building_pincode',
            field=models.CharField(default='93743', max_length=10),
            preserve_default=False,
        ),
    ]
