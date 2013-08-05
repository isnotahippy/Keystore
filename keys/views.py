from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from keys.models import KeyPair
from django.http import HttpResponseRedirect, HttpResponseNotModified, HttpResponse
from django.forms import ModelForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import sys
import json

class KeypairForm(ModelForm):
    class Meta:
        model = KeyPair
        fields = ['key_name', 'key_value']

@ensure_csrf_cookie
@login_required
def keypair_list(request):
    if request.user.is_authenticated():

        KeyPairs = KeyPair.objects.filter(user=request.user).order_by('pk')

        return render_to_response('list.html', {'keypairs': KeyPairs}, context_instance=RequestContext(request))

def keypair_api_post(request):

    if request.user.is_authenticated():

        if request.is_ajax():

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


@login_required
def keypair_edit(request, keyid=None):

    if keyid:
        keypair = get_object_or_404(KeyPair, pk=keyid)
    else:
        keypair = KeyPair()

    if request.POST:
        form = KeypairForm(request.POST, instance=keypair)

        try:
            new_keypair = form.save(commit=False)
            new_keypair.user = request.user
            new_keypair.save()

            return HttpResponseRedirect(reverse('list'))
        except 'ValueErrror':
            print >>sys.stderr, 'form errors'
    else:
        form = KeypairForm(instance=keypair)

    return render_to_response('add.html', { 'KeypairForm': form }, context_instance=RequestContext(request))

