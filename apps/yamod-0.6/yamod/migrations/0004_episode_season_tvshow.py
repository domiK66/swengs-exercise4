# Generated by Django 3.2.8 on 2021-11-10 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0003_alter_person_year_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='TvShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('released', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('cast', models.ManyToManyField(to='yamod.Person')),
                ('tv_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.tvshow')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('runtime', models.IntegerField(default=90, help_text='in minutes')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.season')),
                ('tv_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.tvshow')),
            ],
        ),
    ]
