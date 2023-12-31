# Generated by Django 4.2.3 on 2023-08-18 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0004_alter_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team_away',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='predictions.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_home',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='predictions.team'),
        ),
    ]
