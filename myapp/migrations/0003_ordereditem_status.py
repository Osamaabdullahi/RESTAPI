# Generated by Django 5.0.6 on 2024-06-25 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditem',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('InTransit', 'InTransit'), ('Processing', 'Processing')], default='Processing', max_length=50),
        ),
    ]
