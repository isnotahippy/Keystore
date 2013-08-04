from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):

    if request.user.is_authenticated():
        return render_to_response('interface/authenticated.html', {'name': request.user.username}, context_instance=RequestContext(request))
    else:
        return render_to_response('interface/index.html', context_instance=RequestContext(request))