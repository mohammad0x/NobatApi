# Generated by Django 4.1 on 2023-05-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_createservice',
            name='position',
            field=models.IntegerField(null=True),
        ),
    ]
