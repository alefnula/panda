__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__contact__   = 'alefnula@gmail.com'
__date__      = '21 October 2010'
__copyright__ = 'Copyright (c) 2010 Viktor Kerkez'

import re
import sys
import optparse
import traceback
try:
    import readline
except ImportError:
    pass

import primitives #@UnusedImport
from datatypes import *



class InvalidSyntax(Exception):
    pass

    
class UnknownSymbol(Exception):
    pass

class Tokenizer(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.current      = Block()
        self.current_item = ''
        self.in_string    = False
        self.in_dict      = False
    
    def match_number(self, item):
        return re.match('^[\+\-]?\d+\.?\d*$', item) is not None
    
    def match_variable(self, item):
        return True
    
    def is_dict(self, current, rest):
        return False

    def feed(self, data):
        for line in data.splitlines():
            self.feed_line(line)

    def feed_line(self, line):
        in_something = False
        i, size = 0, len(line)
        while i < size:
            c = line[i]
            if self.in_string:
                if c == '\\' and line[i+1] == '\'':
                    self.current_item += '"'
                    i += 1
                elif c == '\'':
                    self.current.add(String(self.current_item))
                    self.in_string = False
                    self.current_item = ''
                else:
                    self.current_item += c
            elif in_something:
                if re.match('\s', c):
                    self.add_something()
                    in_something = False
                elif c in (')', ']'):
                    self.add_something()
                    in_something = False
                    self.current = self.current.parent
                elif c == ';':
                    break
                else:
                    self.current_item += c
            elif self.in_dict:
                pass
            else:
                if re.match('\s', c): pass
                elif c == '(':
                    self.current = Block(self.current)
                elif c == '[':
                    self.current = List(self.current)
                elif c in (')', ']'):
                    self.current = self.current.parent
                elif c == '\'':
                    self.in_string = True
                elif c == ';':
                    break
                elif self.is_dict(c, line[i+1:]):
                    self.in_dict = True
                else:
                    in_something = True
                    self.current_item = c
            i += 1
        if in_something:
            self.add_something()
        if self.in_string:
            self.current_item += '\n'

    def add_something(self):
        if self.match_number(self.current_item):
            self.current.add(Number(self.current_item))
        elif self.match_variable(self.current_item):
            self.current.add(Variable(self.current_item))
        else:
            print 'ERROR!!!! %s' % self.current_item
        self.current_item = ''


    def can_evaluate(self):
        return (self.current.parent is None) and \
               (not self.in_string)          and \
               (not self.in_dict)

    def eval(self, environ):
        results = map(lambda item: item.eval(environ), self.current)
        self.reset()
        return results



def get_exception():
    trace = ''
    exception = ''
    exc_list = traceback.format_exception_only(sys.exc_type, sys.exc_value) #@UndefinedVariable
    for entry in exc_list:
        exception += entry
    tb_list = traceback.format_tb(sys.exc_info()[2])
    for entry in tb_list:
        trace += entry    
    return '\n\n%s\n%s' % (exception, trace)


def repl(debug=False):
    tokenizer = Tokenizer()
    environment = Environment(mapping=PRIMITIVES)
    while True:
        try:
            data = raw_input('panda> ')
            tokenizer.feed(data)
            while not tokenizer.can_evaluate():
                tokenizer.feed(raw_input(': '))
            for result in tokenizer.eval(environment):
                print result
        except InvalidSyntax, e:
            print 'Invalid syntax'
        except UnknownSymbol, e:
            print 'Unknown symbol: %s' % e
        except (KeyboardInterrupt, EOFError):
            print
            return 0
        except Exception, e:
            print get_exception()
            tokenizer.reset()


def script(script_path, debug=False):
    tokenizer = Tokenizer()
    environment = Environment(mapping=PRIMITIVES)
    data = open(script_path, 'rb').read()
    try:
        tokenizer.feed(data)
        if tokenizer.can_evaluate():
            tokenizer.eval(environment)
        else:
            print 'Error in script'
    except:
        return 0


def main(argv):
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', dest='debug', action='store_true', default=False,
                      help='Show debug informations')
    options, args = parser.parse_args()
    if len(args) > 1:
        print 'Usage: panda.py [script.pnd]'
    elif len(args) == 1:
        script(args[0], options.debug)
    else:
        repl(options.debug)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
