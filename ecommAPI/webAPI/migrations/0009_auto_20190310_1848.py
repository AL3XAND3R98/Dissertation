# Generated by Django 2.1.2 on 2019-03-10 18:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webAPI', '0008_basket_baskettotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='basketID',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.RemoveField(
            model_name='basket',
            name='basketItem',
        ),
        migrations.AddField(
            model_name='basket',
            name='basketItem',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, to='webAPI.Product'),
            preserve_default=False,
        ),
    ]
