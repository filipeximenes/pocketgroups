
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings
from django.contrib.auth import get_user_model, login

from pocket import Pocket

from accounts.models import UserAccount


class LoginCallbackView(generic.RedirectView):
    http_method_names = ['get']
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        request_token = self.request.GET.get('request_token', None)

        if request_token:
            credentials = Pocket.get_credentials(
                consumer_key=settings.POCKET_CONSUMER_KEY, 
                code=request_token
                )

            email = None
            localized = None

            user = get_user_model().objects.filter(pocket_username=credentials['username']).first()

            localizer = self.request.session.get('user_localizer', None)
            if localizer:
                localized = get_user_model().objects.filter(localizer=localizer).first()

            if localized:
                email = localized.email
                if user:
                    groups = localized.pocket_groups.values_list('id', flat=True)
                    user.pocket_groups.add(*groups)
                    if not localized.is_active:
                        localized.delete()
                else:
                    user = localized

            if not user:
                user = UserAccount()

            user.is_active = True
            user.email = email or user.email
            user.pocket_username = credentials['username']
            user.pocket_access_token = credentials['access_token']
            user.save()

            user.backend='django.contrib.auth.backends.ModelBackend' 

            login(self.request, user)

            return reverse('groups:list')
        
        return '/'

