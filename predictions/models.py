from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook_username = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True, null=True)
    
    def has_twitter_authentication(self):
        return bool(self.twitter_access_token and self.twitter_access_token_secret)
    
    
    def __str__(self):
        return self.user.username
class Team(models.Model):
    name = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='pics', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='pics', blank=True, null=True)
    teams = models.ManyToManyField(Team)  # Add this field
    
    def __str__(self):
        return self.name

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team_home = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE, blank=True, null=True)
    team_away = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE, blank=True, null=True)
    match_date = models.DateTimeField()

    def __str__(self):
        return f"{self.team_home} vs {self.team_away}"

    def clean(self):
        if self.tournament.name not in ["UEFA", "Europa"]:
            if self.team_home and self.team_away:
                team_home_tournament = self.team_home.tournament_set.first()
                team_away_tournament = self.team_away.tournament_set.first()

                if team_home_tournament != team_away_tournament:
                    raise ValidationError("Both teams must belong to the same tournament.")
        else:
            # For "UEFA" or "Europa," teams can be from different tournaments
            return

        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Prediction(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_goals = models.PositiveIntegerField()
    away_goals = models.PositiveIntegerField()
    shared = models.BooleanField(default=False)
    sharer_name = models.CharField(max_length=100, blank=True, null=True)  # Add this field
    
    def __str__(self):
        return f"{self.match}: {self.home_goals} - {self.away_goals}"
