
from django.conf.urls import patterns, include, url


from . import views


urlpatterns = patterns('',
    url(r'^$', views.GroupListView.as_view(), name='list'),
    url(r'^new/$', views.GroupCreateView.as_view(), name='create'),
    url(r'^edit/(?P<pk>\d+)/$', views.GroupUpdateView.as_view(), name='update'),
)
