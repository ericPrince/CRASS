from __future__ import print_function

import ply.lex as lev
lev.lev = lev.lex
import ply.yacc as yacc

import sys

if sys.version_info[0] >= 3:
    raw_input = input

#--------------------------------------
# PROGRAM
#--------------------------------------

# TODO: add variable namespace, loop nesting...

variables = {}

#--------------------------------------
# TOKENS
#--------------------------------------

tokens = (
    # general
    'ID',

    # constants
    'INT', 'FLOAT', 'STRINGA', 'STRINGB',

    # keywords
    'DO', 'TO', 'FUCK', 'END', 'WHILE',
    'NO', 'GIVEN', 'FOR', 'SURE', 'NAH', 'SMY',

    # assignment
    'DICK',

    # symbols
    'COMMA', 'LPAREN', 'RPAREN', 'LBRACKET',
    'RBRACKET', 'LBRACE', 'RBRACE', 'COLON', 
    'QUEST', 

    # operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

)

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

# keywords and ID

t_DO      = r'do'
t_TO      = r'to|with|on'
t_FUCK    = r'fuck'
t_END     = r'end'
t_WHILE   = r'while'
t_NO      = r'no'
t_GIVEN   = r'given'
t_FOR     = r'for'
t_SURE    = r'sure'
t_NAH     = r'nah'

t_SMY	  = r'smy'

keywords = (t_DO, t_TO, t_FUCK, t_END,
            t_WHILE, t_NO, t_GIVEN, t_FOR,
            t_SURE, t_NAH, t_SMY,)

# build this automatically bc duh
t_ID = r'(?!'                    \
     + r'('                      \
     + r'|'.join(keywords)       \
     + r')'                      \
     + r'[^A-Za-z0-9_]'          \
     + r')'                      \
     + r'[A-Za-z_][A-Za-z0-9_]*'

print(t_ID)

#t_ID = r'(?!do|to|fuck|end)[A-Za-z_][A-Za-z0-9_]*'

#--------------------------------------

# assignment

t_DICK = r'8=+(>|\))-*'

#--------------------------------------

# symbols

t_COMMA            = r','
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COLON            = r':'
t_QUEST            = r'\?'

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
                 | assign
                 | func_def
                 | while
                 | for_iter
                 | for_items
                 | sure_nah
                 | print'''

#--------------------------------------

# expressions

def p_expr_id(p):
    '''expr : ID'''
    try:
            p[0] = variables[p[1]]
    except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = None

def p_expr_const(p):
    '''expr : constant'''
    p[0] = p[1]

def p_expr_func_call(p):
    '''expr : func_name LPAREN optargs RPAREN'''

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''

#--------------------------------------

# expressions - binops

def p_expr_add(p):
    '''expr : expr PLUS expr'''
    p[0] = p[1] + p[3]

def p_expr_sub(p):
    '''expr : expr MINUS expr'''
    p[0] = p[1] - p[3]

def p_expr_mul(p):
    '''expr : expr TIMES expr'''
    p[0] = p[1] * p[3]

def p_expr_div(p):
    '''expr : expr DIVIDE expr'''
    p[0] = p[1] / p[3]

#--------------------------------------

# expressions - unops

def p_expr_negate(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = -p[2]

#--------------------------------------

# task

def p_task(p):
    '''task : offender DO func_name TO args'''
    print('task')

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
    variables[p[1]] = p[3]
    p[0] = None

# note: lval and rval could be
#  formalized to replace expression

def p_lval(p):
    '''lval : ID'''
    p[0] = p[1]

def p_rval(p):
    '''rval : expr'''
    p[0] = p[1]

#--------------------------------------

# function definition

def p_func_def(p):
    '''func_def : FUCK ID LPAREN optargs RPAREN statements end'''

def p_end(p):
    '''end : END'''

#--------------------------------------

# print

def p_print(p):
	'''print : offender SMY expr'''
	print(p[3])

#--------------------------------------

# while

def p_while(p):
    '''while : WHILE NO itervar GIVEN DO statements end'''

def p_itervar(p):
    '''itervar : ID'''

#--------------------------------------

# for

def p_for_iter(p):
    '''for_iter : FOR expr itervar GIVEN DO statements end'''

def p_for_items(p):
    '''for_items : FOR expr itervar DO statements end'''

#--------------------------------------

# surenah

def p_sure_nah(p):
    '''sure_nah : DO expr QUEST SURE DO statements nah
                | DO expr QUEST SURE DO statements end'''

def p_nah(p):
    '''nah : NAH DO statements end'''

#--------------------------------------

# constants

def p_constant(p):
    '''constant : INT
                | FLOAT
                | string
                | list
                | tuple
                | dict'''
    p[0] = p[1]

def p_string(p):
    '''string : STRINGA
              | STRINGB'''

#--------------------------------------

# constants - list

def p_list(p):
    '''list : LBRACKET optargs RBRACKET'''

#--------------------------------------

# constants - tuple

def p_tuple(p):
    '''tuple : LPAREN tuple_args RPAREN'''

def p_tuple_args(p):
    '''tuple_args : arg COMMA optargs
                  | empty'''

#--------------------------------------

# constants - dict

def p_dict(p):
    '''dict : LBRACE dict_args RBRACE
            | LBRACE RBRACE'''

def p_dict_args(p):
    '''dict_args : dict_arg
                 | dict_arg COMMA
                 | dict_arg COMMA dict_args'''

def p_dict_arg(p):
    '''dict_arg : expr COLON expr'''

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