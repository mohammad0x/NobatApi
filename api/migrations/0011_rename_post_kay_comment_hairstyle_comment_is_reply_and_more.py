# Generated by Django 4.2.2 on 2023-06-10 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_comment_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_kay',
            new_name='HairStyle',
        ),
        migrations.AddField(
            model_name='comment',
            name='is_reply',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentid', to='api.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]