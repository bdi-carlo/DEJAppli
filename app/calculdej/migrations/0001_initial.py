# Generated by Django 2.1.5 on 2019-01-20 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coef', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('titre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('typeCat', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='activite',
            name='categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculdej.Categorie'),
        ),
    ]