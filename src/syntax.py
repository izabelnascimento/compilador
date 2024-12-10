

class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        """Retorna o token atual."""
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type):
        """Avança para o próximo token se o tipo atual for igual ao esperado."""
        if self.current_token() and self.current_token()[0] == token_type:
            self.current_token_index += 1
        else:
            raise SyntaxError(
                f"Esperado {token_type}, mas encontrado {self.current_token()}."
            )

    def parse(self):
        """Inicia a análise sintática."""
        self.program()

    def program(self):
        """Reconhece o programa completo conforme a BNF."""
        self.eat('PROGRAM')
        self.eat('IDENTIFIER')
        self.eat('SEMICOLON')
        self.body()

    def body(self):
        """Reconhece o corpo do programa, incluindo blocos de código."""
        while self.current_token() and self.current_token()[0] != 'END':
            token_type, value, line_number = self.current_token()

            if token_type == 'IDENTIFIER' and value == 'var':
                self.declaration()
            elif token_type == 'IDENTIFIER' and value == 'inicio':
                self.eat('IDENTIFIER')  # Consome 'inicio'
                self.block()  # Processa o bloco de comandos
            else:
                raise SyntaxError(f"Comando inválido na linha {line_number}")

def block(self):
    """Reconhece o bloco de comandos dentro de 'inicio ... fim'."""
    while self.current_token() and self.current_token()[0] != 'END':
        token_type, value, line_number = self.current_token()

        if token_type == 'IDENTIFIER':
            self.statement()
        elif token_type == 'IDENTIFIER' and value == 'fim':
            self.eat('IDENTIFIER')  # Consome 'fim' e encerra o bloco
            return
        else:
            raise SyntaxError(f"Comando inválido na linha {line_number}")


    def declaration(self):
        """Reconhece declarações de variáveis."""
        self.eat('IDENTIFIER')  # 'var'
        self.eat('IDENTIFIER')  # Nome da variável
        while self.current_token() and self.current_token()[0] == 'COMMA':
            self.eat('COMMA')
            self.eat('IDENTIFIER')  # Mais variáveis
        self.eat('COLON')
        self.eat('IDENTIFIER')  # Tipo
        self.eat('SEMICOLON')

    def statement(self):
        """Reconhece comandos no corpo do programa."""
        token_type, value, line_number = self.current_token()

        if token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')  # Nome da variável
            self.eat('ASSIGN')      # Sinal =>
            self.expression()       # Atribuição de expressão
            self.eat('SEMICOLON')
        elif token_type == 'IDENTIFIER' and value == 'mostre':
            self.eat('IDENTIFIER')  # 'mostre'
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
            self.eat('SEMICOLON')
        else:
            raise SyntaxError(f"Comando inválido na linha {line_number}")

    def expression(self):
        """Reconhece expressões matemáticas e booleanas."""
        self.term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[0])  # '+' ou '-'
            self.term()

    def term(self):
        """Reconhece multiplicação, divisão e fatores."""
        self.factor()
        while self.current_token() and self.current_token()[0] in ('MULTIPLY', 'DIVIDE'):
            self.eat(self.current_token()[0])  # '*' ou '/'
            self.factor()

    def factor(self):
        """Reconhece números, variáveis e valores booleanos."""
        token_type, value, line_number = self.current_token()
        if token_type == 'NUMBER':
            self.eat('NUMBER')
        elif token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        else:
            raise SyntaxError(f"Fator inválido na linha {line_number}")
