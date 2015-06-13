"""
Regression tests for the resolve_url function.
"""

from django.db import models


class UnimportantThing(models.Model):
    importance = models.IntegerField()

    def get_absolute_url(self):
        return '/importance/%d/' % (self.importance,)


# House/Room/RoomManager are written old style - get_query_set

class House(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RoomManager(models.Manager):

    def get_query_set(self):
        return super(RoomManager, self).get_query_set().select_related('house')

    def downstairs(self):
        return self.get_query_set().filter(downstairs=True)


class Room(models.Model):
    name = models.CharField(max_length=50)
    downstairs = models.BooleanField()
    house = models.ForeignKey(House, related_name='rooms')

    objects = RoomManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# NewHouse/NewRoom/NewRoomManager are written new style - get_queryset

class NewHouse(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class NewRoomManager(models.Manager):

    def get_queryset(self):
        return super(NewRoomManager, self).get_queryset().select_related('house')

    def downstairs(self):
        return self.get_queryset().filter(downstairs=True)


class NewRoom(models.Model):
    name = models.CharField(max_length=50)
    downstairs = models.BooleanField()
    house = models.ForeignKey(NewHouse, related_name='rooms')

    objects = NewRoomManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
