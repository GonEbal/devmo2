# Generated by Django 3.0.8 on 2020-08-31 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devmo', '0002_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='additional_content',
            field=models.CharField(blank=True, max_length=6400),
        ),
    ]