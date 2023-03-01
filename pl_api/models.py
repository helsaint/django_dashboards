from django.db import models

class PremierLeague(models.Model):
    id = models.IntegerField(blank=False,null=False, primary_key=True)
    player = models.TextField(blank=True,null=True)
    nation = models.TextField(blank=True, null=True)
    pos = models.TextField(blank=True, null=True)
    squad = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    born = models.IntegerField(blank=True, null=True)
    avg_90s_played = models.TextField(blank=True, null=True)
    sca = models.IntegerField(blank=True, null=True)
    sca_per_90 = models.TextField(blank=True, null=True)
    pass_live = models.IntegerField(blank=True, null=True)
    pass_dead = models.IntegerField(blank=True, null=True)
    take_ons = models.IntegerField(blank=True, null=True)
    shots = models.IntegerField(blank=True, null=True)
    fld = models.IntegerField(blank=True, null=True)
    sca_def = models.IntegerField(blank=True, null=True)
    gca = models.IntegerField(blank=True, null=True)
    gca_per_90 = models.TextField(blank=True, null=True)
    pass_live_goal = models.IntegerField(blank=True, null=True)
    pass_dead_goal = models.IntegerField(blank=True, null=True)
    to_goal = models.IntegerField(blank=True, null=True)
    sh_goal = models.IntegerField(blank=True, null=True)
    fld_goal = models.IntegerField(blank=True, null=True)
    def_goal = models.IntegerField(blank=True, null=True)
    unique_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'premier_league'


# Create your models here.
