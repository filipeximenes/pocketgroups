
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .models import PocketGroup


class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/list.html'
    context_object_name = 'pocket_groups'
    model = PocketGroup

    def get_queryset(self):
        return self.request.user.pocket_groups


class GroupFormMixin(UserPassesTestMixin):
    model = PocketGroup
    fields = ('name', 'tag')

    def get_success_url(self):
        return reverse('groups:list')

    def test_func(self, user):
        return user == self.get_object().owner


class GroupCreateView(GroupFormMixin, generic.CreateView):
    template_name = 'groups/create.html'

    def form_valid(self, form):
        current_user = self.request.user
        group = form.save(commit=False)
        group.owner = current_user
        group.save()
        group.members.add(current_user)
        return HttpResponseRedirect(self.get_success_url())


class GroupUpdateView(GroupFormMixin, generic.UpdateView):
    template_name = 'groups/update.html'



