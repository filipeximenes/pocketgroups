from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static

from core.views import LandingPageView, RedirectToAuthView, RootRedirectView
from accounts.views import LoginCallbackView

urlpatterns = patterns('',
    # url(r'^$', RootRedirectView.as_view(), name='root'),
    url(r'^$', LandingPageView.as_view(), name='index'),
    url(r'^redirect_to_pocket_auth/$', RedirectToAuthView.as_view(), name='redirect-to-auth'),
    url(r'^login_callback_view/$', LoginCallbackView.as_view(), name='pocket-login-callback'),

    url(r'^groups/', include('groups.urls', namespace='groups')),

    url(r'^admin/', include(admin.site.urls)),
) 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
