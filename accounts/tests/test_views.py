
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from model_mommy import mommy

from core.tests.utils import setup_view
from accounts.views import LoginCallbackView


factory = RequestFactory()


class TestUserLogin(TestCase):

    def setUp(self):
        self.user = mommy.make('accounts.UserAccount', pocket_username='testusername')
        self.user_invited = mommy.make('accounts.UserAccount', email='test@test.com')

        self.group = mommy.make('groups.PocketGroup')
        self.group.members.add(self.user_invited)

    def test_inviting_existing_user_to_new_group(self):
        request = factory.get(reverse('pocket-login-callback'))
        request.session = {}
        request.session['user_localizer'] = self.user_invited.localizer

        view = setup_view(LoginCallbackView(), request)

        user, email = view.process_logged_user_info(self.user.pocket_username)

        self.assertEqual(user.pocket_username, self.user.pocket_username)
        self.assertEqual(email, self.user_invited.email)

        user_invited = get_user_model().objects.filter(id=self.user_invited.id).first()
        self.assertIsNone(user_invited)

    def test_invited_existing_users_inherits_groups(self):
        request = factory.get(reverse('pocket-login-callback'))
        request.session = {}
        request.session['user_localizer'] = self.user_invited.localizer

        view = setup_view(LoginCallbackView(), request)

        user, email = view.process_logged_user_info(self.user.pocket_username)

        self.assertIn(user, self.group.members.all())
        self.assertIn(self.group, user.pocket_groups.all())




