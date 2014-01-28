
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin, UserPassesTestMixin, FormMessagesMixin

from .models import PocketGroup


class GroupListView(LoginRequiredMixin, generic.ListView):
    template_name = 'groups/list.html'
    context_object_name = 'pocket_groups'
    model = PocketGroup

    def get_queryset(self):
        return self.request.user.pocket_groups


class GroupFormMixin(LoginRequiredMixin, FormMessagesMixin):
    model = PocketGroup
    fields = ('name', 'tag')
    form_invalid_message = 'Invalid submited data'

    def get_success_url(self):
        return reverse('groups:list')


class GroupCreateView(GroupFormMixin, generic.CreateView):
    template_name = 'groups/create.html'
    form_valid_message = 'New group created'

    def form_valid(self, form):
        current_user = self.request.user
        group = form.save(commit=False)
        group.owner = current_user
        group.save()
        group.members.add(current_user)
        return HttpResponseRedirect(self.get_success_url())


class GroupUpdateView(UserPassesTestMixin, GroupFormMixin, generic.UpdateView):
    template_name = 'groups/update.html'
    form_valid_message = 'Group successifully updated.'

    def test_func(self, user):
        return user == self.get_object().owner
