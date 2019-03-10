# Generated by Django 2.1.2 on 2019-03-10 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=200)),
                ('productDesc', models.TextField()),
                ('productStock', models.PositiveIntegerField()),
            ],
        ),
    ]
