from django.shortcuts import render_to_response, get_object_or_404
from keys.models import KeyPair
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
import sys

class KeypairForm(ModelForm):
    class Meta:
        model = KeyPair
        fields = ['key_name', 'key_value']

def keypair_list(request):
    return render_to_response('list.html', { 'keypairs': KeyPair.objects.all() })

def keypair_edit(request, keyid=None):

    if id:
        keypair = get_object_or_404(KeyPair, pk=keyid)
    else:
        keypair = KeyPair()

    if request.POST:
        form = KeypairForm(request.POST, instance=keypair)

        try:
            form.save()
            return HttpResponseRedirect(reverse('list'))
        except 'ValueErrror':
            print >>sys.stderr, 'form errors'
    else:
        form = KeypairForm(instance=keypair)

    return render_to_response('add.html', { 'KeypairForm': form }, RequestContext(request))

