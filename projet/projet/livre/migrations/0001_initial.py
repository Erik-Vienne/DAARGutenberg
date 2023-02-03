# Generated by Django 4.1.5 on 2023-02-03 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('idLivre', models.IntegerField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=300)),
                ('auteur', models.CharField(max_length=300)),
                ('lien', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Mot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mot', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbOccurrence', models.IntegerField()),
                ('idLivre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='livre.livre')),
                ('idMot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='livre.mot')),
            ],
        ),
        migrations.AddConstraint(
            model_name='index',
            constraint=models.UniqueConstraint(fields=('idLivre', 'idMot'), name='unique_migration_host_combination'),
        ),
    ]