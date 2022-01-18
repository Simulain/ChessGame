from hashlib import blake2b
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey

CREATED = 1
IN_PROGRESS = 2
COMPLETED = 3
GAME_STATUS = ((CREATED, 'Game created'), (IN_PROGRESS, 'Game in progress'), (COMPLETED, 'Game completed'))

WHITE_WON = 1
BLACK_WON = 2
DRAW = 3
RESULT = ((WHITE_WON, 'Winner: white'), (BLACK_WON, 'Winner: black'), (DRAW, 'Draw'))

class Game(models.Model):
    host = ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    opponent = ForeignKey(User, on_delete=models.CASCADE, related_name='opponent', null=True)
    host_white = models.BooleanField(default=True)
    fen = models.CharField(max_length=100, null=True, blank=True)
    pgn = models.TextField(null=True, blank=True)
    result = models.IntegerField(default=None, choices=RESULT, blank=True, null=True)
    winner = ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)
    status = models.IntegerField(default=CREATED, choices=GAME_STATUS)

    def __str__(self):
        return f'{self.host.username} Game number {self.pk}'
