# Generated by Django 2.1.1 on 2019-01-19 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20190119_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departure',
            old_name='busdriver_id',
            new_name='busdriver',
        ),
        migrations.RenameField(
            model_name='departure',
            old_name='shuttle_id',
            new_name='shuttle',
        ),
    ]
