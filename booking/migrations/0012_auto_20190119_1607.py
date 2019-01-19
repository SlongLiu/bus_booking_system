# Generated by Django 2.1.1 on 2019-01-19 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20190119_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.IntegerField()),
                ('departure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Departure')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.User')),
            ],
        ),
        migrations.AddField(
            model_name='shuttle',
            name='seat',
            field=models.IntegerField(default=40),
        ),
    ]