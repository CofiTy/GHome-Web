import socket
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.template import RequestContext, loader
from django.utils import simplejson
import client
import models

s = client.Server('localhost', 8080)
m = models.Model(init=s.initialise())

# Test Code
# m = models.Model()
# m.sensors["Temperature"] = models.Sensor("Temperature", 1)
# m.sensors["Humidity"] = models.Sensor("Humidity", 2)
# m.commands += ["shutdown", "Cool"]


def sensors(request):
    return render_to_response('test303/sensors.html', {'sensors' : m.sensors})

def sensor(request, type_name, name):
    return render_to_response('test303/sensor.html', {'sensor' : m.sensors[type_name][name]})

def json_sensor(request, type_name, name):
    try:
        sensor_id = m.sensors[type_name][name].ident

        #fetch data from server
        ans = s.update([sensor_id])

        #update model
        m.update_sensor_by_id(type_name, sensor_id, ans[0]['value'])

        #create json
        d = {"value": ans[0]['value']}
        js = simplejson.dumps(d)
        print js
        res = HttpResponse(js)
    except Exception as e:
        print e
    return res

def commands(request):
    return render_to_response('test303/commands.html', {'commands' : m.commands})

def command(request, name):
    response_dict = {}
    response_dict['message'] = "Just sent "+name+" command !"
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

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
