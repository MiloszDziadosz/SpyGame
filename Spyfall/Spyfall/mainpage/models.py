from django.db import models


class Gametemp(models.Model):
    game_temp_name = models.CharField(max_length=250)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.game_temp_name


class Room(models.Model):
    gametemp = models.ForeignKey(Gametemp, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=20, null=True)
    status = models.IntegerField(default=0)
    password = models.CharField(max_length=10)
    current_location = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.room_name


class Tempuser(models.Model):
    nickname = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    role = models.IntegerField(default=0)
    ready = models.IntegerField(default=0)
    voted = models.IntegerField(default=0)
    voted_for = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname + ' - ' + self.room.room_name + str(self.id) + '    ' + str(self.role)


class Location(models.Model):
    gametemp = models.ForeignKey(Gametemp, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=250)

    def __str__(self):
        return self.location_name + ' - ' + str(self.gametemp)
