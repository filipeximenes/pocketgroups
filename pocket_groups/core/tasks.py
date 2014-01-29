
# import time
from django.utils import dateformat
import datetime
from django.conf import settings
from django.utils.timezone import now

from pocket_groups import celery_app
from groups.models import PocketGroup

from celery.utils.log import get_task_logger

from pocket import Pocket


logger = get_task_logger(__name__)


@celery_app.task
def fetch_groups():
    groups = PocketGroup.objects.order_by('last_addition')

    for group in groups:
        share_group_urls.delay(group.id)


@celery_app.task
def share_group_urls(group_id):
    group = PocketGroup.objects.get(id=group_id)

    members = group.members.all()

    last_addition = group.last_addition
    if not last_addition:
        last_addition = int(dateformat.format(now() - datetime.timedelta(days=1), 'U'))

    last_addition += 1

    newest_item = 0

    members_data = {}

    for member in members:
        if member.pocket_access_token:
            pocket_cli = Pocket(settings.POCKET_CONSUMER_KEY, member.pocket_access_token)
            response, headers = pocket_cli.get(
                    state='all',
                    tag=group.tag,
                    detailType='complete',
                    sort='oldest',
                    since=last_addition
                )

            members_data[member.id] = process_response(member, response)

    for member in members:
        if member.pocket_access_token:
            pocket_cli = Pocket(settings.POCKET_CONSUMER_KEY, member.pocket_access_token)
            
            for member_id, data in members_data.iteritems():
                if member_id is not member.id:
                    sharing_user = data['user']
                    shared_items = data['items']

                    for item in shared_items:
                        if not 'pocketgroups' in item['tags'] and \
                            item['time_added'] > last_addition:
                            pocket_cli.add(
                                url=item['url'],
                                tags='pocketgroups,' + group.tag + ',' + sharing_user.pocket_username
                                )

                    if newest_item < data['lastest_date']:
                        newest_item = data['lastest_date']
    
    if newest_item > 0:
        group.last_addition = newest_item
        group.save()

    logger.info('Remaining API calls (for the current hour): %s' % headers['x-limit-key-remaining'])


def process_response(user, response):
    items = response['list']

    response_dict = {
        'user': user,
        'items': [],
        'lastest_date': None,
    }

    if items:
        for item_id, data in items.iteritems():
            item_dict = {}
            if int(data['status']) != 2:
                item_dict['time_added'] = int(data['time_added'])
                item_dict['tags'] = [tag for tag, _ in data['tags'].iteritems()]
                item_dict['url'] = data['resolved_url']

                response_dict['items'].append(item_dict)

                if not response_dict['lastest_date']:
                    response_dict['lastest_date'] = item_dict['time_added']

                if item_dict['time_added'] < response_dict['lastest_date']:
                    response_dict['lastest_date'] = item_dict['time_added']

    return response_dict
