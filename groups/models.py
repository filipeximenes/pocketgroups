
from django.db import models
from django.contrib.auth import get_user_model


class PocketGroup(models.Model):
    owner = models.ForeignKey(get_user_model())
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    members = models.ManyToManyField(get_user_model(), related_name='pocket_groups')
    last_synced_article = models.ForeignKey('articles.Article', null=True)

    def __unicode__(self):
        return self.name
