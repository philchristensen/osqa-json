from forum.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from django import http

from forms import ClassicRegisterForm
from forum.forms import SimpleEmailSubscribeForm
from forum.views.auth import login_and_forward
from forum.actions import UserJoinsAction

ALLOWED_IPS = [
    '127.0.0.1',
]

def instantiate(request):
    if request.method != 'POST':
        return http.HttpResponseBadRequest()
    elif request.META['REMOTE_ADDR'] not in ALLOWED_IPS:
        return http.HttpResponseForbidden()
    
    username = request.POST['username']
    email = request.POST['email']
    
    u = User(username=username, email=email)
    u.save()
    
    return http.HttpResponse('Created user #%d, %s <%s>' % (u.id(), username, email))

def register(request):
    # disable registration
    # return http.HttpResponseForbidden()
    
    if request.method == 'POST':
        form = ClassicRegisterForm(request.POST)
        email_feeds_form = SimpleEmailSubscribeForm(request.POST)

        if form.is_valid() and email_feeds_form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            user_ = User(username=username, email=email)
            user_.set_password(password)

            if User.objects.all().count() == 0:
                user_.is_superuser = True
                user_.is_staff = True

            user_.save()
            UserJoinsAction(user=user_, ip=request.META['REMOTE_ADDR']).save()

            if email_feeds_form.cleaned_data['subscribe'] == 'n':
                user_.subscription_settings.enable_notifications = False
                user_.subscription_settings.save()

            return login_and_forward(request, user_, None, _("A welcome email has been sent to your email address. "))
    else:
        form = ClassicRegisterForm(initial={'next':'/'})
        email_feeds_form = SimpleEmailSubscribeForm()

    return render_to_response('auth/complete.html', {
        'form1': form,
        'email_feeds_form': email_feeds_form
        }, context_instance=RequestContext(request))
        