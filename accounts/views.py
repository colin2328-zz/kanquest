from django.views.generic import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import PlayerForm


@login_required
def home(request):
    return HttpResponseRedirect(reverse('game:player_list'))


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/register.html', {
            'form': PlayerForm(),
        })

    def post(self, request, *args, **kwargs):
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            player.set_password(form.cleaned_data['password'])
            player.is_superuser = True
            player.save()
            return HttpResponseRedirect(reverse('accounts:home'))

        return render(request, 'accounts/register.html', {
            'form': form,
        })
