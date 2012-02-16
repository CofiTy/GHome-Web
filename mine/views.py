import socket
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.template import RequestContext, loader
from django.utils import simplejson
import client
import models

s = client.Server('localhost', 5003)
m = models.Model(init=s.initialise())

cross = {'rules':1, 'actions':2, 'activators':3, 'sensors':4}

def sensors(request):
    #fetch data from server
    ans = s.update(m.get_id_list())

    for sensor in ans:
        m.update_sensor_by_id(sensor['type'], sensor['id'], sensor['value'])
    
    return render_to_response('test303/sensors.html', {'sensors' : m.sensors})

def binary_sensors(request):    
    return render_to_response('test303/binary_sensors.html', {'sensors' : m.sensors['Presence']})

def sensor(request, type_name, name):
    return render_to_response('test303/sensor.html', {'sensor' : m.sensors[type_name][name], 'type': type_name})

def json_sensor(request, type_name, name):
    try:
        sensor_id = m.sensors[type_name][name].ident

        #fetch data from server
        ans = s.update([sensor_id])

        #update model 
        for sensor in ans:
            m.update_sensor_by_id(sensor['type'], sensor['id'], sensor['value'])

        #create json
        d = {"value": m.sensors[sensor['type']][name].value}
        js = simplejson.dumps(d)
        print js
        res = HttpResponse(js)
    except Exception as e:
        print e
    return res

def json_sensor_init(request, type_name, name):
    sensor_id = m.sensors[type_name][name].ident
    values = s.history(sensor_id, 20)
    js = simplejson.dumps(values)
    
    return HttpResponse(js)

def commands(request):
    return render_to_response('test303/commands.html', {'commands' : m.commands})

def command(request, name):
    s.command(name)
    response_dict = {}
    response_dict['message'] = "Just sent "+name+" command !"
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

def editor(request, name="default"):
    data = s.edits(cross[name])

    return render_to_response('test303/editor.html', {"type": name, "text": data['file']})

def json_editor(request, name="default"):
    ans = {}
    if request.method == 'POST':
        mess  = request.POST.copy()
        mess = mess['data']
        s.edata(cross[name], mess)

    return HttpResponse(simplejson.dumps(ans), mimetype='application/javascript')

def editors(request):
    return render_to_response('test303/editors.html')

def home(request):
    return render_to_response('test303/home.html')
    


############################################################################caca

class TestForm(forms.Form):
    name = forms.CharField(max_length=100)
    msg = forms.CharField(max_length=500)

def form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = TestForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            pass

    form = TestForm() # An unbound form
    t = loader.get_template('test303/form.html')
    c = RequestContext(request, {'form': form })

    return HttpResponse(t.render(c))


def thanks(request, name):
    """
    
    Arguments:
    - `request`:
    """
    return render_to_response('test303/thanks.html', {'name': name})
            


def lol(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 8080))
    s.listen(5)

    (clientsock, a) = s.accept()
    
    msg = clientsock.recv(4)

    return HttpResponse("lol" + msg)

def ajax(request):
    return render_to_response('test303/ajax.html')

def json(request):
    response_dict = {}
    response_dict['info'] = 42
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')


tabs_data = {"home": "some data for home",
             "profile": "Data for profile"}


def tabs_ajax(request, tab):
    d = {}
    try:
        d['content'] = tabs_data[tab]
    except KeyError:
        d['content'] = tab

    return HttpResponse(simplejson.dumps(d))

def tabs(request):
    return render_to_response('test303/tabs.html')
