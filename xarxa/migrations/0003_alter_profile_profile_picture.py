# Generated by Django 5.2 on 2025-06-04 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xarxa', '0002_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/profiles/default.jpg', null=True, upload_to='media/'),
        ),
    ]
