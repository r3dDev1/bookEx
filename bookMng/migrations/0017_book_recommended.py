# Generated by Django 3.1.2 on 2020-12-04 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0016_recommendedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='recommended',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
