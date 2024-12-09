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
        while self.current_token():
            self.statement()

    def statement(self):
        """Reconhece uma atribuição, como: x = 5"""
        token_type, value, line_number = self.current_token()

        if token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')  # Nome da variável
            self.eat('ASSIGN')      # Sinal '='
            self.expression()       # Atribuição de expressão
        else:
            raise SyntaxError(f"Comando inválido na linha {line_number}")

    def expression(self):
        """Reconhece expressões matemáticas, como: 5 + 2."""
        self.term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[0])  # '+' ou '-'
            self.term()

    def term(self):
        """Reconhece multiplicação e divisão."""
        self.factor()
        while self.current_token() and self.current_token()[0] in ('MULTIPLY', 'DIVIDE'):
            self.eat(self.current_token()[0])  # '*' ou '/'
            self.factor()

    def factor(self):
        """Reconhece números e parênteses."""
        token_type, value, line_number = self.current_token()
        if token_type == 'NUMBER':
            self.eat('NUMBER')
        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        else:
            raise SyntaxError(f"Fator inválido na linha {line_number}")
