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
            try:
                self.sensors[sensor['type']][sensor['name']] = Sensor(sensor['name'], sensor['id'])
            except KeyError:
                self.sensors[sensor['type']] = {sensor['name']:Sensor(sensor['name'], sensor['id'])}

