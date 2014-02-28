
from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings

from pocket import Pocket


class RootRedirectView(generic.RedirectView):
    http_method_names = ['get']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return reverse('groups:list')

        return reverse('index')


class LandingPageView(generic.TemplateView):
    template_name = 'core/index.html'


class RedirectToAuthView(generic.RedirectView):
    http_method_names = ['get']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        request_token = Pocket.get_request_token(consumer_key=settings.POCKET_CONSUMER_KEY, 
            redirect_uri=self.request.get_full_path())

        redirect_url = self.request.build_absolute_uri(reverse('pocket-login-callback') + 
            '?request_token=' + request_token)

        self.save_invited_user_to_session()

        auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_url)

        return auth_url

    def save_invited_user_to_session(self):
        invited = self.request.GET.get('user_localizer', None)
        if invited:
            self.request.session['user_localizer'] = invited
