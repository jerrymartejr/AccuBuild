# Generated by Django 4.1.7 on 2023-02-27 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0015_remove_divisioncost_direct_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ocm',
            field=models.DecimalField(blank=True, decimal_places=2, default=10, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='profit',
            field=models.DecimalField(blank=True, decimal_places=2, default=12, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='vat',
            field=models.DecimalField(blank=True, decimal_places=2, default=12, max_digits=20, null=True),
        ),
    ]
