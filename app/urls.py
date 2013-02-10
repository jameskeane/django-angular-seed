from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response

# Enable the admin site
from django.contrib import admin
admin.autodiscover()

# Import the API
from app import api

# define the catch all
def index(request):
    return render_to_response('index.html')

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.router.urls)),

    # Catch all, for history API routing
    url(r'^.*', index, name='index')
)
