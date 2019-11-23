from django.db import models

class Gametemp(models.Model):
    game_temp_name = models.CharField(max_length=250)
    '''owner = models.ForeignKey(User, on_delete=models.CASCADE)'''
    def __str__(self):
       return self.game_temp_name

class Room(models.Model):
    gametemp = models.ForeignKey(Gametemp, on_delete=models.CASCADE)
    status = models.IntegerField
    password = models.CharField(max_length=10)
    '''time = models.TimeField( auto_now_add=True, blank=True)'''

class Tempuser(models.Model):
    nickname = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class Location(models.Model):
    gametemp = models.ForeignKey(Gametemp, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=250)

    def __str__(self):
        return self.location_name + ' - ' + str(self.gametemp)
