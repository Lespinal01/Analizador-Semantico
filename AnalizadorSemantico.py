import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens que vamos a usar
tokens = (
    'NUMBER', 'ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'SEMICOLON'
)

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'

# Definición de número (solo enteros en este ejemplo)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Definición de identificador (variables)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Ignoramos los espacios en blanco
t_ignore = ' \t'

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construimos el lexer
lexer = lex.lex()

# Tabla de símbolos para el análisis semántico
symbol_table = {}

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Reglas de la gramática

# Asignación de una expresión a una variable
def p_statement_assign(p):
    '''statement : ID ASSIGN expression
                 | ID ASSIGN expression SEMICOLON'''
    var_name = p[1]
    var_type = type(p[3])
    symbol_table[var_name] = var_type  # Agregamos la variable a la tabla de símbolos
    print(f"Asignación: {var_name} = {p[3]} (tipo: {var_type.__name__})")

# Expresión como una declaración por sí misma
def p_statement_expr(p):
    '''statement : expression
                 | expression SEMICOLON'''
    print(f"Resultado de la expresión: {p[1]}")

# Operadores binarios (suma, resta, multiplicación, división)
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    left_type = type(p[1])
    right_type = type(p[3])
    if left_type != right_type:
        raise TypeError(f"Error de tipo: no se puede operar {left_type.__name__} con {right_type.__name__}")
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            raise ZeroDivisionError("Error: división entre cero")
        p[0] = p[1] / p[3]

# Expresión con un número
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

# Expresión con un identificador (variable)
def p_expression_id(p):
    'expression : ID'
    var_name = p[1]
    if var_name not in symbol_table:
        raise NameError(f"Error: variable '{var_name}' no declarada")
    # Asumimos valor 0 para simulación (sin valor concreto de la variable)
    p[0] = 0 if symbol_table[var_name] is int else 0.0

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis")

# Construimos el parser
parser = yacc.yacc()

# Función principal para ejecutar el analizador
def main():
    print("Escribe expresiones; termina con EOF (Ctrl+D en Unix, Ctrl+Z en Windows)")
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        try:
            parser.parse(s)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
