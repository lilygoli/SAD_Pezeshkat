# Generated by Django 3.0.5 on 2020-04-16 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200416_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(null=True),
        ),
    ]
