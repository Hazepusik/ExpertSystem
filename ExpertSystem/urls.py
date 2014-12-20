from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from Classes.models import test
from Classes.views import main, situations, questions, solution

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ExpertSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test/$',  test),
    url(r'^$',  main),
    url(r'^scenarios/$',  situations),
    url(r'^scenarios/([0-9]+)/$',  questions),
    url(r'^solution/$',  solution),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
