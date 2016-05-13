from __future__ import print_function

import ply.lex as lex
import ply.yacc as yacc

import sys

if sys.version_info[0] >= 3:
    raw_input = input


variables = {}

# LEXER

tokens = ('VARNAME', 'NUMBER', 'PLUS', 'MINUS', 'EQUALS', 'INT')

#literals = ('=', '+', '-')
literals = ()

t_VARNAME = r'[a-zA-z_][a-zA-Z0-9_]*'

t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUALS = r'='

# Integer literal
#t_ICONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
#t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

def t_INT(t):
    r'(\d(?!\.))+(?!\d)'
    #r'\d+(e\d+)??=[^\.=]'
    t.value = int(t.value)
    return t

def t_NUMBER(t):
    r'\d+(\.\d*)?(e\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

def t_error(t):
    print('error: bad token %s' % t)
    t.lexer.skip(1)

lexer = lex.lex()

# RULES

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('right', 'UMINUS'),
    ('right', 'EQUALS'),
)

# note this is a statement not expression!!
def p_statement_assign(p):
    'expression : VARNAME EQUALS expression'
    variables[p[1]] = p[3]
    p[0] = p[3]
    #p[0] = None

#def p_statement_expr(p):
#    'statement : expression'
#    p[0] = p[1]

def p_expression_add(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_sub(p):
    'expression : expression MINUS expression'
    p[0] = p[1] - p[3]

def p_expression_negate(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_number(p):
    '''expression : INT
                  | NUMBER'''
    p[0] = p[1]

#def p_expression_int(p):
#    'expression : INT'
#    p[0] = p[1]

def p_expression_name(p):
    'expression : VARNAME'
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print('%s not recognized' % p[1])
        p[0] = None

def p_error(p):
    if p:
        print("Syntax error at line %d: '%s'" % (p.lineno, p.value))
    else:
        pass
        #print("Syntax error at EOF")

parser = yacc.yacc()

# RUN MAIN LOOP

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break

    r = parser.parse(s, lexer=lexer)

    if r is not None:
        print(r)