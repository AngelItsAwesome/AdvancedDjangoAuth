# Generated by Django 5.0.6 on 2024-06-20 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='celphone',
            field=models.CharField(default='', max_length=15),
        ),
    ]