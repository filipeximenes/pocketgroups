
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings
from django.contrib.auth import get_user_model, login

from pocket import Pocket


class LoginCallbackView(generic.RedirectView):
    http_method_names = ['get']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        request_token = self.request.GET.get('request_token', None)
        username = self.request.GET.get('username', None)

        if request_token:
            credentials = Pocket.get_credentials(
                consumer_key=settings.POCKET_CONSUMER_KEY, 
                code=request_token
                )

            user, created = get_user_model().objects.get_or_create(pocket_username=credentials['username'])
            user.pocket_access_token = credentials['access_token']
            user.save()

            user.backend='django.contrib.auth.backends.ModelBackend' 

            login(self.request, user)

            return reverse('groups:list')
        
        return '/'

