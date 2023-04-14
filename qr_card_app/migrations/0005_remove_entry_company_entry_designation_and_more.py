# Generated by Django 4.2 on 2023-04-13 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_card_app', '0004_alter_entry_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='company',
        ),
        migrations.AddField(
            model_name='entry',
            name='designation',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='linkedin',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='photo',
            field=models.ImageField(default=0, upload_to='media/images/'),
            preserve_default=False,
        ),
    ]