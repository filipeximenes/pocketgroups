
from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    group = models.ForeignKey('groups.PocketGroup', db_index=True, related_name='feed')
    shared_by = models.ForeignKey(get_user_model())
    pocket_id = models.CharField(max_length=255)
    resolved_id = models.CharField(max_length=255, db_index=True)
    time_updated = models.IntegerField(default=0)
    link = models.TextField()

    def __unicode__(self):
        return self.link



