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

#tokens = ('DICK', 'INT', 'FLOAT', 'WORD')

tokens = [
    # CRASS-specific
    'DICK', 'TO', 'DO', 'POUND', 'FUCK', 'SMY','WHILE_NO','OFFEND','BEGET','FROM','SURE','NAH',
    'FOR','AS', 'GIVEN', 'COMMENT',

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

    #Ternary operator (?)
    'QUEST',
    
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
t_QUEST          = r'\?'

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


# We designed these...

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

#t_TO = r'(to)|(with)|(on)'

def t_TO(t):
    r'(to)|(with)|(on)'
    print('t_TO')

#t_DO = r'do'
t_POUND = r'\#'

def t_DO(t):
    r'do'
    print('t_DO')

t_FUCK = r'fuck'
t_OFFEND = r'offend'
t_FOR = r'for'
t_GIVEN = r'given'
t_WHILE_NO = r'while no'
t_SURE = r'sure'
t_NAH = r'nah'
t_BEGET = r'beget'
t_FROM = r'from'
t_AS = r'as'
t_SMY = r'show me your'

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

def t_comment(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1

t_ignore = ' \t'

def t_error(t):
    print('error: bad token %s' % t)
    t.lexer.skip(1)

lever = lev.lev()

#------------------------------------------------
# PARSER
#------------------------------------------------

precedence = (
    ('left','PLUS','MINUS','DIVIDE','TIMES'),
    ('right','UMINUS'),
)

start = 'statements'

def p_statements(p):
    '''statements : statements statement 
                  | statement'''
    print('stmts')

#def p_statement(p):
#    '''statement : task
#                 | for
#                 | while
#                 | surenah
#                 | assign
#                 | beget
#                 | print
#                 | func_def
#                 | COMMENT'''

def p_statement(p):
    '''statement : task
    			 | assign
    			 | beget'''
    print('stmt')

def p_func_def(p):
    '''func_def : FUCK ID LPAREN optargs RPAREN DO statements OFFEND'''
    print('func def')

def p_for(p):
    '''for : basic_for
           | iter_for'''
    print('for')

def p_basic_for(p):
    '''basic_for : FOR expression itervar GIVEN DO statements OFFEND'''
    print('basic_for')

def p_iter_for(p):
    '''iter_for : FOR expression itervar DO statements OFFEND'''
    print('iter_for')

def p_itervar(p):
    '''itervar : ID'''
    print('itervar')

def p_while(p):
    '''while : WHILE_NO itervar GIVEN DO statements OFFEND'''
    print('while')

def p_surenah(p):
    '''surenah : sure OFFEND
               | sure nah'''
    print('surenah')

def p_sure(p):
    '''sure : expression QUEST SURE DO statements'''
    print('sure')

def p_nah(p):
    '''nah : NAH DO statements OFFEND'''
    print('nah')

def p_beget(p):
    '''beget : optfrom basic_beget optas'''
    print('beget')

def p_basic_beget(p):
    '''basic_beget : BEGET ID'''
    print('basic beget')

def p_optfrom(p):
    '''optfrom : FROM ID
               | empty'''
    print('optfrom')

def p_optas(p):
    '''optas : AS ID
             | empty'''
    print('optas')

def p_print(p):
    '''print : optoffender SMY expression'''
    print('print')

def p_optoffender(p):
    '''optoffender : offender
                   | empty'''
    print('optoff')

def p_task(p):
    '''task : named_task
            | unnamed_task'''
    print('task')

def p_named_task(p):
    '''named_task : offender unnamed_task'''
    print('named_task')

def p_offender(p):
    '''offender : ID'''
    print('off')

def p_unnamed_task(p):
    '''unnamed_task : DO operation TO''' 
    #'''unnamed_task : DO operation TO args qualifier''' 
    print('unnamed_task')

def p_operation(p):
    '''operation : func_name'''
    print('op')

def p_func_name(p):
    '''func_name : word'''
    print('func name')

def p_word(p):
    '''word : ID'''
    print('word')

def p_args(p):
    '''args : arg
            | arg COMMA args'''
    print('args')

def p_arg(p):
    '''arg : expression'''
    print('arg')

def p_qualifier(p):
    '''qualifier : phrase'''
    print('qual')

def p_phrase(p):
    '''phrase : word optphrase'''
    print('phrase')

def p_optphrase(p):
    '''optphrase : phrase
                 | empty'''
    print('optphrase')

def p_expression(p):
    '''expression : function
                  | constant
                  | math
                  | ID'''
    print('expr')

def p_function(p):
    '''function : ID LPAREN optargs RPAREN'''
    print('func')

def p_optargs(p):
    '''optargs : args
               | empty'''
    print('optargs')

def p_empty(p):
    '''empty : '''
    print('empty')

def p_constant(p):
    '''constant : number
                | STRINGA
                | STRINGB'''
    print('const')

def p_number(p):
    '''number : INT
              | FLOAT
              | negative_number'''
    print('num')

def p_negative_number(p):
    '''negative_number : MINUS INT %prec UMINUS
                       | MINUS FLOAT %prec UMINUS'''
    print('neg')

def p_math(p):
    '''math : add
            | sub
            | mul
            | div'''
    print('math')

def p_add(p):
    '''add : expression PLUS expression'''
    print('add')

def p_sub(p):
    '''sub : expression MINUS expression'''
    print('sub')

def p_mul(p):
    '''mul : expression TIMES expression'''
    print('mul')

def p_div(p):
    '''div : expression DIVIDE expression'''
    print('div')

def p_assign(p):
    '''assign : lval DICK rval'''
    print('assign!!')

def p_lval(p):
    '''lval : ID'''
    print('lval')

def p_rval(p):
    '''rval : expression'''
    print('rval')

def p_error(p):
    if p:
        print("Syntax error at line %d: '%s'" % (p.lineno, p.value))
        print(p)
    else:
        pass
        #print("Syntax error at EOF")

#parser = yacc.yacc(start=start)
parser = yacc.yacc()

#------------------------------------------------
# RUN
#------------------------------------------------

while True:
    try:
        s = raw_input('CRASS 8===>- ')
    except EOFError:
        break

    r = parser.parse(s, lexer=lever)

    if r is not None:
        print(r)
