# Generated by Django 3.1.4 on 2020-12-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201213_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.Category'),
        ),
    ]