from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from Classes.models import test
from Classes.views import *

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ExpertSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/$',  test),
    url(r'^$',  situations),
    url(r'^scenarios/$',  situations),
    url(r'^scenarios/([0-9]+)/$',  questions),
    url(r'^questions/([0-9]+)/$',  next_question),
    url(r'^expert/$', expert_entrance),
    url(r'^expert_logindata/$', expert_auth),
    url(r'^expert/situations/$', expert_situations),
    url(r'^expert/new_scenario/$', add_situation),
    url(r'^expert/new_question/$', add_question),
    url(r'^expert/new_recommendation/$', add_recommendation),
    url(r'^expert/situations/([0-9]+)/$', redact_situation),
    url(r'^expert/situations/([0-9]+)/delete/$', delete_situation),
    url(r'^expert/answers/([0-9]+)/delete/$', delete_answer),
    url(r'^expert/answers/add/$', add_answer),
    url(r'^expert/questions/([0-9]+)/delete/$', delete_question),
    url(r'^expert/questions/([0-9]+)/setter/$', question_setter),
    url(r'^expert/questions/([0-9]+)/$', redact_question),
    url(r'^expert/recommendations/([0-9]+)/delete/$', del_recommendation),
    url(r'^expert/recommendations/([0-9]+)/$', redact_recommendation),

    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
urlpatterns += staticfiles_urlpatterns()