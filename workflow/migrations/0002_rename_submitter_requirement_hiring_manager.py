# Generated by Django 3.2 on 2021-04-09 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requirement',
            old_name='submitter',
            new_name='hiring_manager',
        ),
    ]
