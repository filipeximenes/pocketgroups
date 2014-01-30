
from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    group = models.ForeignKey('groups.PocketGroup', related_name='feed')
    shared_by = models.ForeignKey(get_user_model())
    pocket_id = models.CharField(max_length=255)
    time_added = models.IntegerField()
    link = models.TextField()

    def __unicode__(self):
        return self.link



