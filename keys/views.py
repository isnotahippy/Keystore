from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from keys.models import KeyPair
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import sys

class KeypairForm(ModelForm):
    class Meta:
        model = KeyPair
        fields = ['key_name', 'key_value']

@login_required
def keypair_list(request):
    if request.user.is_authenticated():

        KeyPairFormSet = modelformset_factory(model=KeyPair,exclude='user',extra=1)

        if request.method == 'POST':
            formset = KeyPairFormSet(request.POST, queryset=KeyPair.objects.filter(user=request.user))

            if formset.is_valid():
                models = formset.save(commit=False)

                for model in models:
                    if model.pk is None:
                        model.user = request.user
                    model.save()

            return HttpResponseRedirect(reverse('list'))

        else:
            formset = KeyPairFormSet(queryset=KeyPair.objects.filter(user=request.user))

        return render_to_response('list.html', {'formset': formset}, context_instance=RequestContext(request))

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

