import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'DOC_START',
    'DOC_END',
    'DOCNO_START',
    'DOCNO_END',
    'DOCNO_CONTENT',
    'TEXT',
)

# Regular expression rules for simple tokens
t_DOC_START = r'<doc>'
t_DOC_END = r'</doc>'
t_DOCNO_START = r'<docno>'
t_DOCNO_END = r'</docno>'

def t_DOCNO_CONTENT(t):
    r'\d+'
    return t

def t_TEXT(t):
    r'[^<]+'
    return t

# Ignored characters
t_ignore = " \t\n"

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_document(p):
    '''document : DOC_START DOCNO_START DOCNO_CONTENT DOCNO_END TEXT DOC_END'''
    p[0] = {
        'docno': p[3],
        'content': p[5]
    }

def p_error(p):
    print(f"Syntax error at token {p.value}")

parser = yacc.yacc()