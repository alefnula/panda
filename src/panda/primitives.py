__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__contact__   = 'alefnula@gmail.com'
__date__      = '21 October 2010'
__copyright__ = 'Copyright (c) 2010 Viktor Kerkez'

import operator
import functools

from datatypes import *


def primitive(name):
    return functools.partial(Primitive, name)


def special_form(name):
    return functools.partial(SpecialForm, name)

Primitive('str', str)

@primitive('+')
def add(*items):
    result = items[0]
    for item in items[1:]:
        result += item
    return result


@primitive('-')
def sub(item, *items):
    return item - sum(items)


@primitive('*')
def mul(*items):
    result = items[0]
    for item in items[1:]:
        result *= item
    return result


@primitive('/')
def div(item, *items):
    for i in items:
        item /= i
    return item


Primitive('%',  operator.mod)
Primitive('=',  operator.eq)
Primitive('!=', operator.ne)
Primitive('<',  operator.lt)
Primitive('<=', operator.le)
Primitive('>',  operator.gt)
Primitive('>=', operator.ge)

@primitive('cons')
def cons(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    elif isinstance(a, list):
        return a + [b]
    elif isinstance(b, list):
        return [a] + b
    else:
        return [a, b]


@primitive('car')
def car(list):
    return list[0]


@primitive('cdr')
def cdr(list):
    return list[1:]


@primitive('print')
def print_function(*items):
    print ''.join(map(str, items))


Primitive('map', map)
Primitive('filter', filter)


@special_form('define')
def define_form(environ, variable_block, *value_blocks):
    if isinstance(variable_block, Block):
        name = variable_block.blocks[0].name()
        value = lambda_form(environ, Block(blocks=variable_block.blocks[1:]), *value_blocks)
        value.name = name
        environ.set(name, value)
        return name
    else:
        name = variable_block.name()
        value = value_blocks[0].eval(environ)
        if isinstance(value, Lambda):
            value.name = name
        environ.set(name, value)
        return name


@special_form('if')
def if_form(environ, condition_block, true_block, false_block):
    if condition_block.eval(environ):
        return true_block.eval(environ)
    else:
        return false_block.eval(environ)


@special_form('cond')
def cond_form(environ, *blocks):
    else_block = None
    if len(blocks) > 0:
        for block in blocks:
            condition = block.at(0)
            result = block.at(1)
            if isinstance(condition, Variable) and condition.name() == 'else':
                else_block = result
            else:
                if condition.eval(environ):
                    return result.eval(environ)
        if else_block is not None:
            return else_block.eval(environ)
    return None


@special_form('let')
def let_form(environ, mapping_blocks, code_block):
    env = Environment(parent=environ)
    for block in mapping_blocks:
        env.set(block.at(0).name(), block.at(1).eval(environ))
    return code_block.eval(env)


@special_form('set!')
def setbang_form(environ, variable, value):
    environ.deepset(variable.name(), value.eval(environ))


@special_form('lambda')
def lambda_form(environ, args_block, *code_blocks):
    args = map(lambda variable: variable.name(), args_block.blocks)
    return Lambda(environ, 'lambda', args, *code_blocks)
