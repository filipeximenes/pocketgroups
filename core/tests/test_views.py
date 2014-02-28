
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from model_mommy import mommy

from core.tests.utils import setup_view
from core.views import RedirectToAuthView


factory = RequestFactory()


class TestRedirectToAuthView(TestCase):

    def setUp(self):
        self.user_invited = mommy.make('accounts.UserAccount', email='test@test.com')

    def test_saves_user_localizer_in_session(self):
        request = factory.get(reverse('redirect-to-auth') + '?user_localizer=' + self.user_invited.localizer)

        view = setup_view(RedirectToAuthView(), request)
        view.save_invited_user_to_session()

        self.assertEqual(view.request.session['user_localizer'], self.user_invited.localizer)
