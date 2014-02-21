from flaskbb.core.exceptions import FlaskBBError

class RegistryError(FlaskBBError):
    pass

# Registry class

class Registry:
    
    def __init__(self):
        self.pool = {}
        
    def register(self, name, cls):
        self.pool[name] = cls
        
    def unregister(self, name):
        del self.pool[name]
        
    def exists(self, name):
        return (name in self.pool)
        
    def get(self, name):
        if name not in self.pool:
            return None
        return self.pool[name]
    
    
# Basic metaclass for use with registries

class BaseMeta(type):
    
    reg = None
    what = 'class'
    
    def __new__(cls, name, bases, d):
        if '_name' not in d and '_inherit' not in d:
            raise RegistryError('_name not defined in class %s' % name)
        _name = d['_name'] if '_name' in d else d['_inherit']
        _inherit = d['_inherit'] if '_inherit' in d else None
        if cls.reg.exists(_name):
            if not _inherit:
                raise RegistryError('%s named %s already exists and is not being inherited by class %s!' % (cls.what.capitalize(), _name, name))
            newcls = cls.reg.get(_name) # TODO - implement inheritance
        else:
            newcls = super().__new__(cls, name, bases, d)
            cls.reg.register(_name, newcls)      
        return newcls
    