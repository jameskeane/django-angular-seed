from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import base64

# Enable the admin site
from django.contrib import admin
admin.autodiscover()

# Import the API
from app import api

# define the catch all
def index(request):
    user_json = {}
    if request.user.is_authenticated():
      ur = api.UserResource()
      ur_bundle = ur.build_bundle(obj=request.user, request=request)
      user_json = ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')

    return render_to_response('index.html', {
      'user': request.user, 
      'user_json': user_json
    })

def auth(request):
  if 'HTTP_AUTHORIZATION' in request.META:
    uname, passwd = request.META['HTTP_AUTHORIZATION'].split(':')
    user = authenticate(username=uname, password=passwd)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.user = user

  # They did not provide basic authentication
  response = HttpResponse()
  response.status_code = 200 if request.user.is_authenticated() else 401
  return response

def vlogout(request):
  logout(request)
  return redirect('/')

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^api/', include(api.router.urls)),

    url(r'^auth/?', auth, name='auth'),
    url(r'^logout/?', vlogout, name='logout'),
    # Catch all, for history API routing
    url(r'^.*', index, name='index')
)
