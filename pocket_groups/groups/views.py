
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
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

    def get_context_data(self, **kwargs):
        remaining = [1,2,3,4]
        kwargs['remaining_emails'] = remaining
        if self.object:
            kwargs['remaining_emails'] = remaining[self.object.members.count()-1:]

        return kwargs

    def form_valid(self, form):
        invited_users = []
        for i in range(5):
            email = form.data.get('invite-email'+str(i), None)
            if email:
                print email
                user, created = get_user_model().objects.get_or_create(
                    email=email, defaults={'pocket_username': email})
                invited_users.append(user)

        if invited_users:
            self.object.members.add(*invited_users)
            pass
            # send_invitation_email(self.request.user, invited_users)

        return super(GroupFormMixin, self).form_valid(form)


class GroupCreateView(GroupFormMixin, generic.CreateView):
    template_name = 'groups/create.html'
    form_valid_message = 'New group created'

    def form_valid(self, form):
        current_user = self.request.user
        self.object = form.save(commit=False)
        self.object.owner = current_user
        self.object.save()
        self.object.members.add(current_user)
        
        return super(GroupCreateView, self).form_valid(form)


class GroupUpdateView(UserPassesTestMixin, GroupFormMixin, generic.UpdateView):
    template_name = 'groups/update.html'
    form_valid_message = 'Group successifully updated.'

    def test_func(self, user):
        return user == self.get_object().owner
