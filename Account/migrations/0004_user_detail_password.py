# Generated by Django 4.1 on 2022-09-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_remove_user_detail_is_email_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_detail',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
