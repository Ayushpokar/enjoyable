# train_app/forms.py
from django import forms
from .models import *

class searchtrainform(forms.Form):
    source=forms.CharField()
    destination = forms.CharField()
    depart_date = forms.DateField() 
    



# for add station 
# forms.py








'''from .forms import *
import os, json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators  import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your views here.
@login_required(login_url='/accounts/signup')
def uploadfile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file to MEDIA_ROOT/uploaded_folder using a unique name
            fs = FileSystemStorage(settings.MEDIA_ROOT + '/uploaded_folder',
                                    base_url=settings.MEDIA_URL + 'uploaded_folder')
            filename = fs.save('%s-%s' % (form.cleaned_data['name'],
                                         form.cleaned_data['document']),
                               form.cleaned_data['document'])
            
            # Make sure the uploaded file is an image and get its URL
            try:
                with open(fs.path(filename)) as fp:
                    document = Image.open(fp)
                    
                    # Resize the image to fit within the required dimensions
                    width, height = document.size
                    max_dimension = max(width, height)
                    new_width = int((960 / float(max_dimension)) * width)
                    new_height = int((540 / float(max_dimension)) * height)
                    document = document.resize((new_width, new_height), Image.ANTIALIAS)
                    
                    # Save the th umbnail in THUMBNAILS_FOLDER
                    thumb_fs = FileSystemStorage(settings.THUMBNAILS_FOLDER)
                    thumb_filename = thumb_fs.save("thumb_" + filename,
                                                   ContentFile(document.convert('RGB').tostring()))
                    # Add the URL of the thumbnail to the saved data
                    doc_dict = {'name': form.cleaned_data['name'],
                                'docfile': '%s/%s' % (fs.base_url.strip('/'), filename),
                                'thumbfile': '%s/%s' % (thumb_fs.base_url.strip('/'), thumb_filename)}
                    docs = json.loads(request.session.get('docs', '[]'))
                    docs.append(doc_dict)
                    request.session['docs'] = json.dumps(docs)
            except IOError:
                pass  # Not an image; just save the file as-is
            
            return HttpResponseRedirect('.')
    else:
        form = UploadFileForm()
    
    return render_to_response('uploader/index.html', {
        'form': form,
        'docs': docs}, context_instance=RequestContext(request))</s> 
'''

# json_data = open('static/railways/stations.json','r')
# stations = json.loads(json_data.read())
# for d in stations["features"]:
#     data = d["properties"]
#     station = Station()
#     station.state = data["state"]
#     station.code = data["code"]
#     station.name = data["name"]
#     station.zone = data["zone"]
#     station.address = data["address"]
#     station.save()

# json_data = open('static/railways/trains.json', 'r')
# trains = json.loads(json_data.read())
# for d in trains["features"]:
#     data = d["properties"]
#     train = Train()
#     train.arrival = data["arrival"]
#     train.source = Station.objects.get(pk=data["from_station_code"])
#     train.name = data["name"]
#     train.number = data["number"]
#     train.departure = data["departure"]
#     train.return_train = data["return_train"]
#     train.dest = Station.objects.get(pk=data["to_station_code"])
#     train.duration_m = data["duration_m"]
#     train.duration_h = data["duration_h"]
#     train.type = data["type"]
#     train.distance = data["distance"]
#     print(train)
#     train.save()
#
# json_data = open('static/railways/schedules.json', 'r')
# schedules = json.loads(json_data.read())
# for data in schedules:
#     schedule = Schedule()
#     schedule.arrival = data["arrival"]
#     schedule.day = data["day"]
#     schedule.station = Station.objects.get(pk=data["station_code"])
#     schedule.train = Train.objects.get(pk=data["train_number"])
#     schedule.departure = data["departure"]
#     schedule.id = data["id"]
#     print(schedule.id)
#     schedule.save()


