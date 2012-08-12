from django.db.models import Q, Max
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
import django.utils.simplejson as json

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import AlbumForm, PickAlbumForm
from utils import resize

@login_required
def new_album(request):
    if request.method == "POST": #submission of new album
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            try:
                album.validate_unique()
                album.save()
                return HttpResponse("<div title=\"%s\"><input type=\"hidden\" id=\"status\" value=\"%s\"/></div>" % (album.title, album.id))
            except ValidationError:
                error = "You have used this album title before. Make sure you pick an unique title."
    else: #request for rendered form
        form = AlbumForm()
        error = None
    return render_to_response(request, 'albums/ajax/new_album.html', {'form': form, 'error': error})

@login_required
def uploadify(request):
    # Processing of each uploaded image
    albumform = PickAlbumForm(request.user, request.POST)
    
    if albumform.is_valid():
        album = albumform.cleaned_data['album']
        max_order = Photo.objects.filter(album=album).aggregate(Max('order'))['order__max'] or 0
        img = request.FILES['Filedata']
        path = 'albums/%s/%s/' % (request.user.id, album.id) #/media/albums/<userid>/<albumid>/<img>.jpg
        # get the resizing dimensions from the preferences #TODO this might move to utils in the future
        preferences = Preferences.get_or_create(request.user)
        resize_dimensions = preferences.get_default_img_size()
        img_data = resize(img, upload_to=path, sizes_data=[resize_dimensions])
        
        for data in img_data:
            photo = Photo(user=request.user, album=album, width=data[1], height=data[2])
            photo.image = data[0]
            photo.order = max_order + 1
            photo.save()
            p_id = photo.id
        return HttpResponse('%s' % p_id, mimetype="text/plain") #return the photo id
    else:
        return HttpResponse()

### search function
def search(request):
    inputresults = request.GET.__getitem__('term').split(' ')
    query = []
    for value in inputresults:
        q = Q(title__icontains=value) | Q(description__icontains=value) | Q(user__username__icontains=value)
        query.append(q)
    if len(query) > 0 and len(query) < 10:
        albums = Album.objects.filter(trash=False, public=True, *query).order_by('title')
    else:
        return HttpResponse()
    output = []
    for album in albums:
        label = mark_safe(u"%s \u2022 %s" % (album.__unicode__(), album.user.get_profile().forum_nickname))
        output.append({
            "id": album.id,
            "label": label,
            "value": album.__unicode__(),
            "url": album.get_absolute_url()
        })
    return HttpResponse(json.dumps(output))