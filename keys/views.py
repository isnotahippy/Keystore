from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from keys.models import KeyPair
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.forms import ModelForm, model_to_dict
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import sys
import json
from django.core import serializers
from django.conf import settings

class KeypairForm(ModelForm):
    class Meta:
        model = KeyPair
        fields = ['key_name', 'key_value']

@ensure_csrf_cookie
@login_required
def keypair_list(request):
    if request.user.is_authenticated():

        KeyPairs = KeyPair.objects.filter(user=request.user, deleted=False).order_by('pk')

        return render_to_response('list.html', { 'name': request.user.username, 'keypairs': KeyPairs}, context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def keypair_api_general(request):

    if request.user.is_authenticated():

        # Post/create new key pair
        if request.method == "POST":
            if request.POST.get('kpid', False):
                try:
                    keypair = KeyPair.objects.get(pk=request.POST['kpid'])
                except 'DoesNotExist':
                    keypair = KeyPair()
                    keypair.user = request.user

            else:
                keypair = KeyPair()
                keypair.user = request.user

            keypair.key_name = request.POST.get('key_name', None)
            keypair.key_value = request.POST.get('key_value', None)

            keypair.save()

            return HttpResponse(json.dumps({'kpid': keypair.pk, 'key_name': keypair.key_name, 'key_value': keypair.key_value }), mimetype="application/json")

        # Get list
        elif request.method == "GET":
            KeyPairs = KeyPair.objects.filter(user=request.user, deleted=False).order_by('pk')
            return HttpResponse(serializers.serialize('json',KeyPairs), mimetype="application/json")

@ensure_csrf_cookie
@login_required
def keypair_api_specific(request, id):
    if request.user.is_authenticated():
        try:
            keypair = KeyPair.objects.get(pk=id)

            if(keypair.user==request.user):

                if request.method=="DELETE":
                    response = json.dumps({"model": model_to_dict(keypair)})
                    keypair.delete()
                    return HttpResponse(response, mimetype="application/json")
                else:
                    return HttpResponse(json.dumps({"model": model_to_dict(keypair)}), mimetype="application/json")
            else:
                return HttpResponseForbidden(json.dumps({ "error": settings.MESSAGES['api']['keypair_forbidden'] }), mimetype="application/json")
        except KeyPair.DoesNotExist:
            return HttpResponseNotFound(json.dumps({ "error": settings.MESSAGES['api']['keypair_notfound'] }), mimetype="application/json")

