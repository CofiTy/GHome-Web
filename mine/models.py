# Create your models here.

class Sensor(object):
    """
    """
    
    def __init__(self, name, ident):
        """
        
        Arguments:
        - `identifier`:
        - `name`:
        - `value`:
        """
        self.ident = ident
        self.name = name
        self.value = 0
        

class Model(object):
    """
    """
    
    def __init__(self, sensors={}, commands=[], init=None):
        """
        
        Arguments:
        - `sensors`:
        - `commands`:
        """
        self.sensors = sensors
        self.commands = commands

        self.cross = {}

        if init != None:
            self._from_init(init)
            self.commands = init['commands']

    def _from_init(self, init):
        """
        
        Arguments:
        - `self`:
        - `init`:
        """
        for sensor in init['sensors']:
            sens = Sensor(sensor['name'], sensor['id'])
            self.cross[sensor['id']] = sensor['name']
            try:
                self.sensors[sensor['type']][sensor['name']] = sens
            except KeyError:
                self.sensors[sensor['type']] = {sensor['name']: sens}

    def update_sensor_by_id(self, sensor_type, sensor_id, value):
        self.sensors[sensor_type][self.cross[sensor_id]].value = value

    def get_name_for_id(self, sensor_id):
        return self.cross[sensor_id]
