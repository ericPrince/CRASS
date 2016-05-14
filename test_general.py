from __future__ import print_function

import ply.lex as lev
lev.lev = lev.lex
import ply.yacc as yacc

import sys

if sys.version_info[0] >= 3:
    raw_input = input

#--------------------------------------
# TOKENS
#--------------------------------------

tokens = (
    # general
    'ID',

    # constants
    'INT', 'FLOAT', 'STRINGA', 'STRINGB',

    # keywords
    'DO', 'TO',

    # assignment
    'DICK',

    # symbols
    'COMMA', 'LPAREN', 'RPAREN',

    # operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

)

# build this automatically
t_ID = r'(?!do|to)[A-Za-z_][A-Za-z0-9_]*'

#--------------------------------------

# constants

def t_INT(t):
    r'(\d(?!\.))+(?![\d=])'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.(\d*)?(e\d+)?'
    t.value = float(t.value)
    return t

t_STRINGA = r'\"([^\\\n]|(\\.))*?\"'
t_STRINGB = r'\'([^\\\n]|(\\.))*?\''

#--------------------------------------

# keywords

t_DO = r'do'
t_TO = r'to'

#--------------------------------------

# assignment

t_DICK = r'8=+(>|\))-*'

#--------------------------------------

# symbols

t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'

#--------------------------------------

# operators

t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'

#--------------------------------------

# non-token

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1

t_ignore = ' \t'

def t_error(t):
    print('unrecognized token')

#--------------------------------------

lever = lev.lev()

#--------------------------------------
# SYNTAX
#--------------------------------------

# precedence

precedence = (
    ('left', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

#--------------------------------------

# statements

def p_statements(p):
    '''statements : statements statement
                  | statement'''

def p_statement(p):
    '''statement : task
                 | assign'''

#--------------------------------------

# expressions

def p_expr_id(p):
    '''expr : ID'''

def p_expr_const(p):
    '''expr : constant'''

def p_expr_func_call(p):
    '''expr : func_name LPAREN optargs RPAREN'''

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''

#--------------------------------------

# expressions - binops

def p_expr_add(p):
    '''expr : expr PLUS expr'''

def p_expr_sub(p):
    '''expr : expr MINUS expr'''

def p_expr_mul(p):
    '''expr : expr TIMES expr'''

def p_expr_div(p):
    '''expr : expr DIVIDE expr'''

#--------------------------------------

# expressions - unops

def p_expr_negate(p):
    '''expr : MINUS expr %prec UMINUS'''

#--------------------------------------

# task

def p_task(p):
    '''task : offender DO func_name TO args'''

def p_offender(p):
    '''offender : ID'''

def p_func_name(p):
    '''func_name : ID'''

#--------------------------------------

# args

def p_args(p):
    '''args : arg
            | arg COMMA args'''

def p_arg(p):
    '''arg : expr'''

def p_optargs(p):
    '''optargs : args
               | empty'''

#--------------------------------------

# assign

def p_assign(p):
    '''assign : lval DICK rval'''

# note: lval and rval could be
#  formalized to replace expression

def p_lval(p):
    '''lval : ID'''

def p_rval(p):
    '''rval : expr'''

#--------------------------------------

# constants

def p_constant(p):
    '''constant : INT
                | FLOAT
                | STRINGA
                | STRINGB'''

#--------------------------------------

# general

def p_empty(p):
    '''empty : '''

def p_error(p):
    #print('p_error')
    if p:
        print("Syntax error at line %d: '%s'" % (p.lineno, p.value))
        #print(p)
    else:
        print("ended in bad state")

#--------------------------------------

parser = yacc.yacc(start='statements')

#--------------------------------------
# RUN
#--------------------------------------

while True:
    try:
        s = raw_input('input : ')
    except EOFError:
        break

    r = parser.parse(s, lexer=lever)

    if r is not None:
        print(r)