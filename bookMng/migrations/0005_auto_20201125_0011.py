# Generated by Django 3.1.3 on 2020-11-25 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]