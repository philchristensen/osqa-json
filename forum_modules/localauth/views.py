import time

from forum.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth import login
from django import http

from forms import ClassicRegisterForm
from forum.forms import SimpleEmailSubscribeForm
from forum.views.auth import login_and_forward
from forum.actions import UserJoinsAction

ALLOWED_IPS = [
    '127.0.0.1',
    '192.168.1.99',
]

KODINGEN_COOKIE_NAME = 'kodingen'

def authenticate(request):
    if KODINGEN_COOKIE_NAME not in request.COOKIES:
        return http.HttpResponseBadRequest('Kodingen cookie not found')
    
    auth_token = request.COOKIES[KODINGEN_COOKIE_NAME]
    u = User.objects.filter(auth_token=auth_token)
    
    if not(u):
        return http.HttpResponseForbidden('User with provided auth token not found')
    
    u = u[0]
    u.auth_token = ''
    u.save()
    u.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, u)
    
    if 'url' in request.GET:
        return http.HttpResponseRedirect(request.GET['url'])
    
    return http.HttpResponse('Logged-in user #%d, %s <%s>' % (u.id, u.username, u.email))

def authenticate_test(request):
    kodingen_cookie = '###########%s###########' % time.time()
    
    u = User.objects.filter(username=request.GET['username'])
    if not(u):
        return http.HttpResponseBadRequest('Invalid user specified')
    
    u = u[0]
    u.auth_token = kodingen_cookie
    u.save()
    
    r = http.HttpResponse('Setup test kodingen cookie for #%d, %s <%s>' % (u.id, u.username, u.email))
    r.set_cookie(KODINGEN_COOKIE_NAME, kodingen_cookie)
    return r

def instantiate(request):
    # if request.META['REMOTE_ADDR'] not in ALLOWED_IPS:
    #     return http.HttpResponseForbidden('Invalid REMOTE_ADDR')
    if request.method != 'GET':
        return http.HttpResponseBadRequest('Invalid request method')
    
    try:
        username = request.GET['username']
        email = request.GET['email']
    except http.MultiValueDictKeyError, e:
        return http.HttpResponseBadRequest(str(e))
    
    if(User.objects.filter(username=username)):
        return http.HttpResponseBadRequest('Username already in use')
    
    u = User(username=username, email=email)
    u.save()
    
    return http.HttpResponse('Created user #%d, %s <%s>' % (u.id, username, email))

def register(request):
    # disable registration
    return http.HttpResponseForbidden()
    
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
        