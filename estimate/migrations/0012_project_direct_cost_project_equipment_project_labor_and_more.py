# Generated by Django 4.1.7 on 2023-02-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0011_divisioncost_direct_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='direct_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='equipment',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='labor',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='material',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
