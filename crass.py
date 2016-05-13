from __future__ import print_function

import ply.lex as lev
lev.lev = lev.lex
import ply.yacc as yacc

import sys

if sys.version_info[0] >= 3:
    raw_input = input

#------------------------------------------------
# LEX
#------------------------------------------------

tokens = ('DICK', 'INT', 'FLOAT', 'WORD')

tokens = [
    # CRASS-specific
    'DICK',

    # Literals (identifier, integer constant, float constant, string constant, char const)
    'ID', 'TYPEID', 'INT', 'FLOAT', 'STRINGA', 'STRINGB',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    #'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    #'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    #'INCREMENT', 'DECREMENT',

    # Structure dereference (->)
    #'ARROW',

    # Ternary operator (?)
    #'TERNARY',
    
    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Ellipsis (...)
    #'ELLIPSIS',
]

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MODULO           = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators

'''
t_EQUALS           = r'='
t_TIMESEQUAL       = r'\*='
t_DIVEQUAL         = r'/='
t_MODEQUAL         = r'%='
t_PLUSEQUAL        = r'\+='
t_MINUSEQUAL       = r'-='
t_LSHIFTEQUAL      = r'<<='
t_RSHIFTEQUAL      = r'>>='
t_ANDEQUAL         = r'&='
t_OREQUAL          = r'\|='
t_XOREQUAL         = r'\^='

# Increment/decrement
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'
'''

# ->
#t_ARROW            = r'->'

# ?
#t_TERNARY          = r'\?'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'

#t_ELLIPSIS         = r'\.\.\.'

# Identifiers
t_ID = r'[A-Za-z_][A-Za-z0-9_]*'

# Integer literal
#t_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
#t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_STRINGA = r'\"([^\\\n]|(\\.))*?\"'
t_STRINGB = r'\'([^\\\n]|(\\.))*?\''

t_DICK = r'8=+(>|\))-*'

#t_WORD = r'[a-zA-z_][a-zA-Z0-9_]*'

def t_INT(t):
    r'(\d(?!\.))+(?![\d=])'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.(\d*)?(e\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print('error: bad token %s' % t)
    t.lexer.skip(1)


lever = lev.lev()

#------------------------------------------------
# PARSER
#------------------------------------------------

precedence = ()

start = 'statements'

def p_statements(p):
    '''statements : statements 
                  | statements'''

def p_statement(p):
    '''statement : task
                 | for
                 | while
                 | surenah
                 | assign
                 | beget
                 | print
                 | func_def
                 | comment
                 | expression'''

def p_task(p):
    '''task : named_task
            | unnamed_task'''

def p_named_task(p):
    '''named_task : offender unnamed_task'''

def p_offender(p):
    '''offender : ID'''

def p_unnamed_task(p):
    '''unnamed_task : 'do' operation to args qualifier'''

def p_operation(p):
    '''operation : func_name'''

def p_func_name(p):
    '''func_name : word'''

def p_word(p):
    '''word : ID'''

def p_args(p):
    '''args : arg
            | arg COMMA args'''

def p_arg(p):
    '''arg : expression'''

def p_qualifier(p):
    '''qualifier : phrase'''

def p_phrase(p):
    '''phrase : word phrase
              | phrase word
              | word'''

def p_expression(p):
    '''expression : function
                  | constant
                  | math'''

def p_function(p):
    '''function : ID LPAREN optargs RPAREN'''

def p_optargs(p):
    '''optargs : args
               | empty'''

def p_empty(p):
    '''empty : '''

def p_constant(p):
    '''constant : number
                | STRINGA
                | STRINGB'''

def p_number(p):
    '''number : INT
              | FLOAT
              | negative_number'''

def p_negative_number(p):
    '''negative_number : MINUS INT
                       | MINUS FLOAT'''

def p_math(p):
    '''math : add
            | sub
            | mul
            | div'''

def p_add(p):
    '''add : number PLUS number'''

def p_sub(p):
    '''sub : number MINUS number'''

def p_mul(p):
    '''mul : number MULTIPLY number'''

def p_div(p):
    '''div : number DIVIDE number'''

def p_assign(p):
    '''assign : lval DICK rval'''

def p_lval(p):
    '''lval : ID'''

def p_rval(p):
    '''rval : expression'''


parser = yacc.yacc(start=start)

#------------------------------------------------
# RUN
#------------------------------------------------

