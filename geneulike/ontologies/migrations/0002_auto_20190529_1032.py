# Generated by Django 2.0.13 on 2019-05-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontologies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biological',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='biological',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_biological_as_ancestor_+', to='ontologies.Biological'),
        ),
        migrations.RemoveField(
            model_name='biological',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='biological',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_biological_as_parent_+', to='ontologies.Biological'),
        ),
        migrations.RemoveField(
            model_name='cell',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='cell',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_cell_as_ancestor_+', to='ontologies.Cell'),
        ),
        migrations.RemoveField(
            model_name='cell',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='cell',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_cell_as_parent_+', to='ontologies.Cell'),
        ),
        migrations.RemoveField(
            model_name='cellline',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='cellline',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_cellline_as_ancestor_+', to='ontologies.CellLine'),
        ),
        migrations.RemoveField(
            model_name='cellline',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='cellline',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_cellline_as_parent_+', to='ontologies.CellLine'),
        ),
        migrations.RemoveField(
            model_name='chemical',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='chemical',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_chemical_as_ancestor_+', to='ontologies.Chemical'),
        ),
        migrations.RemoveField(
            model_name='chemical',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='chemical',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_chemical_as_parent_+', to='ontologies.Chemical'),
        ),
        migrations.RemoveField(
            model_name='disease',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='disease',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_disease_as_ancestor_+', to='ontologies.Disease'),
        ),
        migrations.RemoveField(
            model_name='disease',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='disease',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_disease_as_parent_+', to='ontologies.Disease'),
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='experiment',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_experiment_as_ancestor_+', to='ontologies.Experiment'),
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='experiment',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_experiment_as_parent_+', to='ontologies.Experiment'),
        ),
        migrations.RemoveField(
            model_name='species',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='species',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_species_as_ancestor_+', to='ontologies.Species'),
        ),
        migrations.RemoveField(
            model_name='species',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='species',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_species_as_parent_+', to='ontologies.Species'),
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='as_ancestor',
        ),
        migrations.AddField(
            model_name='tissue',
            name='as_ancestor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_tissue_as_ancestor_+', to='ontologies.Tissue'),
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='as_parent',
        ),
        migrations.AddField(
            model_name='tissue',
            name='as_parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_tissue_as_parent_+', to='ontologies.Tissue'),
        ),
    ]
