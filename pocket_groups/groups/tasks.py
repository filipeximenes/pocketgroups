
from pocket_groups import celery_app
from templated_email import send_templated_mail

from groups.models import PocketGroup
from accounts.models import UserAccount

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@celery_app.task
def send_invite_emails(group_id, invited_users_ids):
    group = PocketGroup.objects.get(id=group_id)
    users = UserAccount.objects.filter(id__in=invited_users_ids)

    for user in users:
        send_templated_mail(
            template_name='invite',
            from_email='no-reply@getpocketgroups.com',
            recipient_list=[user.email],
            context={
                'user': user,
                'group': group,
        },)
        logger.info('Sent email to %s', user.email)


