# Generated by Django 4.2.1 on 2023-06-04 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_like_image_remove_like_like_image_dislike_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_key',
            new_name='HairStyle',
        ),
    ]
