# Generated by Django 4.2 on 2023-04-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_card_app', '0005_remove_entry_company_entry_designation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='photo',
            field=models.ImageField(upload_to='mages/'),
        ),
    ]
