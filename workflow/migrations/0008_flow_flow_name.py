# Generated by Django 3.2 on 2021-07-02 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0007_alter_flow_executed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='flow',
            name='flow_name',
            field=models.CharField(default='Legacy', max_length=255, verbose_name='Process'),
            preserve_default=False,
        ),
    ]