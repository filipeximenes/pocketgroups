
from django.utils import dateformat
import datetime
from django.conf import settings
from django.utils.timezone import now

from pocket_groups import celery_app
from groups.models import PocketGroup
from articles.models import Article

from celery.utils.log import get_task_logger

from pocket import Pocket


logger = get_task_logger(__name__)


@celery_app.task
def fetch_groups():
    groups = PocketGroup.objects.order_by('last_synced_article__time_updated')

    for group in groups:
        share_group_urls.delay(group.id)


@celery_app.task
def share_group_urls(group_id):
    group = PocketGroup.objects.get(id=group_id)
    members = group.members.all()

    for member in members:
        if member.pocket_access_token:
            last_article = group.feed.order_by('time_updated').filter(shared_by=member).last()

            if last_article:
                last_update = last_article.time_updated
            else:
                last_update = int(dateformat.format(now() - datetime.timedelta(days=1), 'U'))
            last_update += 1

            pocket_cli = Pocket(settings.POCKET_CONSUMER_KEY, member.pocket_access_token)
            response, headers = pocket_cli.get(
                    state='all',
                    tag=group.tag,
                    detailType='complete',
                    sort='oldest',
                    since=last_update
                )

            process_and_add_to_feed(group, member, response)

    feed = group.feed.order_by('time_updated')
    if group.last_synced_article:
        feed = feed.filter(id__gt=group.last_synced_article.id)
    feed = feed.all()

    for member in members:
        if member.pocket_access_token:
            pocket_cli = Pocket(settings.POCKET_CONSUMER_KEY, member.pocket_access_token)

            for article in feed:
                if article.shared_by != member:
                    logger.info('Sharing: %s - %s' % (member.pocket_username, article.link))
                    pocket_cli.add(
                        url=article.link,
                        tags='pocketgroups,' + group.tag + ',' + article.shared_by.pocket_username
                    )

    group.last_synced_article = group.feed.order_by('id').last()
    group.save()

    logger.info('Remaining API calls (for the current hour): %s' % headers['x-limit-key-remaining'])


def process_and_add_to_feed(group, user, response):
    items = response['list']

    if items:
        for item_id, data in items.iteritems():
            if data['status'] != '2':
                print data
                time_updated = int(data['time_updated'])
                tags = [tag for tag, _ in data['tags'].iteritems()]
                url = data['given_url']
                pocket_id = data['item_id']
                resolved_id = data['resolved_id']

                if not 'pocketgroups' in tags:
                    Article.objects.get_or_create(
                        group=group,
                        resolved_id=resolved_id,
                        defaults={
                            'shared_by': user,
                            'time_updated': time_updated,
                            'link': url,
                            'pocket_id': pocket_id
                        }
                    )
