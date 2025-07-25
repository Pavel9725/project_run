from django.contrib.auth.models import User
from django.db import models


class Run(models.Model):
    STATUS_CHOICES = [
        ('init', 'Initialization'),
        ('in_progress', 'In_progress'),
        ('finished', 'Finished')
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='init')
    distance = models.FloatField(blank=True, null=True)
    run_time_seconds = models.IntegerField(null=True, blank=True)
    speed = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'athlete_id: {self.athlete.id} id:{self.id} {self.status}'


class AthleteInfo(models.Model):
    goals = models.TextField(blank=True, default='')
    weight = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_info')

    def __str__(self):
        return f'{self.user} user.id: {self.user.id} athlete.id: {self.id}'


class Challenge(models.Model):
    full_name = models.CharField(max_length=255)
    athlete = models.ForeignKey(AthleteInfo, on_delete=models.CASCADE, related_name='challenges')

    def __str__(self):
        return f'{self.full_name} athlete: {self.athlete}'


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='positions')
    latitude = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    date_time = models.DateTimeField()
    speed = models.FloatField(default=0)
    distance = models.FloatField(default=0)


class CollectibleItem(models.Model):
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=255, unique=True)
    value = models.IntegerField()
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    picture = models.URLField()
    collected_by = models.ManyToManyField(User, related_name='collectible_items', blank=True)


class Subscribe(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe_coach')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe_athlete')

    class Meta:
        unique_together = ('coach', 'athlete')
