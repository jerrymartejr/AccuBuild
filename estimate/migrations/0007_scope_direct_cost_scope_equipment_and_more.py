# Generated by Django 4.1.7 on 2023-02-23 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0006_rename_profite_other_cost_scopecost_profit_other_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='scope',
            name='direct_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='equipment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='indirect_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='labor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='material',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='ocm_prcnt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='profit_other_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='profit_prcnt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='qty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='total_cost_no_vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='total_cost_w_vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='total_prcnt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='unit',
            field=models.CharField(default='lot', max_length=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='unit_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='scope',
            name='vat_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.RemoveField(
            model_name='scope',
            name='project',
        ),
        migrations.DeleteModel(
            name='ScopeCost',
        ),
        migrations.AddField(
            model_name='scope',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scopes', to='estimate.project'),
        ),
    ]
