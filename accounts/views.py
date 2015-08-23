# from django.views.generic import View
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
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            player.set_password(form.cleaned_data['password'])
            player.save()
            return HttpResponseRedirect(reverse('accounts:home'))
    else:
        form = PlayerForm()  # An unbound form

    return render(request, 'accounts/register.html', {
        'form': form,
    })
