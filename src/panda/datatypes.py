__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__contact__   = 'alefnula@gmail.com'
__date__      = '21 October 2010'
__copyright__ = 'Copyright (c) 2010 Viktor Kerkez'

class Environment(object):
    def __init__(self, parent=None, mapping=None):
        self.parent = parent
        self.mapping = {} if mapping is None else mapping
    
    def set(self, key, value):
        self.mapping[key] = value
    
    def deepset(self, key, value):
        if key in self.mapping:
            self.mapping[key] = value
        else:
            self.parent.deepset(key, value)

    def get(self, key):
        if key in self.mapping:
            return self.mapping[key]
        if self.parent:
            return self.parent.get(key)
        return None
    
    def __repr__(self):
        return str(self.mapping)
    __str__ = __repr__


PRIMITIVES = {
    'True'  : True,
    'False' : False,
}

class Primitive(object):
    def __init__(self, name, function):
        self.name = name
        self.function = function
        global PRIMITIVES
        PRIMITIVES[name] = self
    
    def __call__(self, *args):
        return self.function(*args)
    
    def __repr__(self):
        return '[primitive: %s]' % self.name
    __str__  = __repr__



class SpecialForm(object):
    def __init__(self, name, function):
        self.name = name
        self.function = function
        global PRIMITIVES
        PRIMITIVES[name] = self
        
    def __call__(self, *args):
        return self.function(*args)
    
    def __repr__(self):
        return '[primitive: %s]' % self.name
    __str__  = __repr__



class Block(object):
    def __init__(self, parent=None, blocks=None):
        self.parent = parent
        if parent is not None:
            self.parent.add(self)
        self.blocks = [] if blocks is None else blocks
    
    def add(self, block):
        self.blocks.append(block)
    
    def at(self, index):
        return self.blocks[index]

    def __repr__(self):
        return '(%s)' % ' '.join(map(str, self.blocks))
    __str__ = __repr__

    def __iter__(self):
        for item in self.blocks:
            yield item

    def eval(self, environ):
        operator = self.blocks[0].eval(environ)
        if isinstance(operator, SpecialForm):
            return apply(operator, [environ] + self.blocks[1:])
        else:
            return apply(operator, map(lambda arg: arg.eval(environ), self.blocks[1:]))



class List(object):
    def __init__(self, parent=None, items=None):
        self.parent = parent
        if parent is not None:
            self.parent.add(self)
        self.items = [] if items is None else items
    
    def add(self, item):
        self.items.append(item)
    
    def at(self, index):
        return self.items[index]

    def __repr__(self):
        return '[%s]' % ' '.join(map(str, self.items))
    __str__ = __repr__

    def __iter__(self):
        for item in self.items:
            yield item

    def eval(self, environ):
        return map(lambda item: item.eval(environ), self.items)



class Variable(object):
    def __init__(self, data):
        self.data = data
    
    def name(self):
        return self.data

    def eval(self, environ):
        return environ.get(self.data)

    def __repr__(self):
        return 'Var(%s)' % self.data
    __str__ = __repr__



class Lambda(object):
    def __init__(self, environ, name, arglist, *code_blocks):
        self.environ = environ
        self.name = name
        if len(arglist) >= 2 and arglist[-2] == '.':
            self.arglist = arglist[:-2]
            self.cumulative = arglist[-1]
        else:
            self.arglist = arglist
            self.cumulative = None
        self.code_blocks = code_blocks
    
    def __repr__(self):
        return '#[lambda %s arglist=(%s)]' % (self.name, ' '.join(self.arglist))
    
    def __call__(self, *args):
        env = Environment(parent=self.environ)
        for i, arg in enumerate(self.arglist):
            env.set(arg, args[i])
        if self.cumulative is not None:
            env.set(self.cumulative, args[len(self.arglist):])
        result = None
        for code_block in self.code_blocks:
            result = code_block.eval(env)
        return result



class Number(object):
    def __init__(self, data):
        try:
            self.data = int(data)
        except ValueError:
            self.data = float(data)

    def eval(self, environ):
        return self.data

    def __repr__(self):
        return str(self.data)
    __str__ = __repr__



class String(object):
    def __init__(self, data):
        self.data = data

    def eval(self, environ):
        return self.data

    def __repr__(self):
        return repr(self.data)
    __str__ = __repr__
