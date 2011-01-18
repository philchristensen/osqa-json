from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _
import views as app

urlpatterns = patterns('',
    # url(r'^%s%s%s$' % (_('account/'), _('local/'),  _('register/')), app.register, name='auth_local_register'),
    url(r'^%s%s%s$' % (_('account/'), _('local/'),  _('instantiate/')), app.instantiate, name='auth_local_instantiate'),
    url(r'^%s%s%s$' % (_('account/'), _('local/'),  _('authenticate/')), app.authenticate, name='auth_local_authenticate'),
    url(r'^%s%s%s$' % (_('account/'), _('local/'),  _('authenticate-test/')), app.authenticate_test, name='auth_local_authenticate_test'),
)