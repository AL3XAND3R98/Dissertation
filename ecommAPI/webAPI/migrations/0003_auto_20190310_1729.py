# Generated by Django 2.1.2 on 2019-03-10 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webAPI', '0002_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productName',
            field=models.CharField(max_length=100),
        ),
    ]
