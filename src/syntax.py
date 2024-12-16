from src.util import Util


class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def start_syntax(self):
        print("\n------------------- ANÁLISE SINTÁTICA -------------------")
        self.parse()
        Util.print_sucess("\nAnálise sintática concluída sem erros.")

    def current_token(self):
        """Retorna o token atual."""
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type):
        """Avança para o próximo token se o tipo atual for igual ao esperado."""
        if self.current_token() and self.current_token()[0] == token_type:
            self.current_token_index += 1
        else:
            expected = token_type
            found = self.current_token()[0] if self.current_token() else "EOF"
            raise SyntaxError(
                f"Esperado token '{expected}', mas encontrado '{found}' na linha {self.current_token()[2] if self.current_token() else 'desconhecida'}."
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
        """Reconhece o corpo do programa."""
        if self.current_token() and self.current_token()[0] == 'VAR':
            self.declaration()
        while self.current_token() and self.current_token()[0] in ('PROCEDURE', 'FUNCTION'):
            self.subroutine()
        self.actions()

    def declaration(self):
        """Reconhece declarações de variáveis."""
        self.eat('VAR')
        while True:
            self.eat('IDENTIFIER')  # Nome da variável
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.eat('COMMA')
            else:
                break
        self.eat('COLON')
        self.type_var()
        self.eat('SEMICOLON')
        # if self.current_token() and self.current_token()[0] == 'IDENTIFIER':
        #     self.declaration()  # Declaração múltipla

    def subroutine(self):
        """Reconhece procedimentos e funções."""
        if self.current_token()[0] == 'PROCEDURE':
            self.procedure_declaration()
        elif self.current_token()[0] == 'FUNCTION':
            self.function_declaration()

    def procedure_declaration(self):
        self.eat('PROCEDURE')
        self.eat('IDENTIFIER')
        if self.current_token()[0] == 'LPAREN':
            self.eat('LPAREN')
            self.parameters()
            self.eat('RPAREN')
        self.eat('SEMICOLON')
        self.body()

    def function_declaration(self):
        self.eat('FUNCTION')
        self.eat('IDENTIFIER')
        if self.current_token()[0] == 'LPAREN':
            self.eat('LPAREN')
            self.parameters()
            self.eat('RPAREN')
        self.eat('RETURNS')
        self.eat('IDENTIFIER')
        self.eat('SEMICOLON')
        self.body()

    def parameters(self):
        while True:
            self.eat('IDENTIFIER')  # Nome do parâmetro
            self.eat('COLON')
            self.eat('IDENTIFIER')  # Tipo do parâmetro
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.eat('COMMA')
            else:
                break

    def actions(self):
        if self.current_token() and self.current_token()[0] == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            self.assignment()
        else:
            self.eat('BEGIN')
        while self.current_token() and self.current_token()[0] != 'END':
            self.statement()
        self.eat('END')

    def statement(self):
        token_type, value, line_number = self.current_token()

        if token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token()[0] == 'ASSIGN':
                self.eat('ASSIGN')
                self.expression()
            elif self.current_token()[0] == 'LPAREN':  # Chamada de função ou procedimento
                self.eat('LPAREN')
                while self.current_token() and self.current_token()[0] != 'RPAREN':
                    self.expression()
                    if self.current_token()[0] == 'COMMA':
                        self.eat('COMMA')
                self.eat('RPAREN')
            self.eat('SEMICOLON')
        elif token_type == 'IF':
            self.conditional()
        elif token_type == 'WHILE':
            self.loop()
        elif token_type == 'RETURN':
            self.return_statement()
        elif token_type == 'SHOW':
            self.eat('SHOW')
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
            self.eat('SEMICOLON')
        else:
            raise SyntaxError(f"Comando inválido na linha {line_number}")

    def conditional(self):
        self.eat('IF')
        self.expression()
        self.eat('THEN')
        self.statement()
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.eat('ELSE')
            self.statement()

    def loop(self):
        self.eat('WHILE')
        self.expression()
        self.eat('DO')
        self.actions()

    def return_statement(self):
        self.eat('RETURN')
        if self.current_token() and self.current_token()[0] != 'SEMICOLON':
            self.expression()
        self.eat('SEMICOLON')

    def expression(self):
        self.simple_expression()
        while self.current_token() and self.current_token()[0] in ('EQUAL', 'NOT_EQUAL', 'GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL'):
            self.eat(self.current_token()[0])
            self.simple_expression()

    def simple_expression(self):
        if self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[0])
        self.term()
        while self.current_token() and self.current_token()[0] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[0])
            self.term()

    def term(self):
        self.factor()
        while self.current_token() and self.current_token()[0] in ('MULTIPLY', 'DIVIDE', 'AND', 'OR'):
            self.eat(self.current_token()[0])
            self.factor()

    def factor(self):
        token_type, value, line_number = self.current_token()
        if token_type == 'NUMBER':
            self.eat('NUMBER')
        elif token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            self.expression()
            self.eat('RPAREN')
        elif token_type in ('TRUE', 'FALSE'):
            self.eat(token_type)
        elif token_type == 'NOT':
            self.eat('NOT')
            self.factor()
        else:
            raise SyntaxError(f"Fator inválido na linha {line_number}")

    def type_var(self):
        token_type, value, line_number = self.current_token()

        if self.current_token() and self.current_token()[0] == 'INT':
            self.eat('INT')
        elif self.current_token() and self.current_token()[0] == 'BOOL':
            self.eat('BOOL')
        else:
            raise SyntaxError(f"esperava o tipo 'INT ou BOOL' na linha {line_number}")
    def assignment(self):
        token_type, value, line_number = self.current_token()
        if self.current_token() and self.current_token()[0] == 'ASSIGN':
            self.eat('ASSIGN')
            if self.current_token() and self.current_token()[0] == 'NUMBER':
                self.eat('NUMBER')
                if self.current_token() and self.current_token()[0] == 'SEMICOLON':
                    self.eat('SEMICOLON')
                else:
                    raise SyntaxError(f"esperava um semicolon na linha {line_number}")
            else:
                raise SyntaxError(f"esperava um number na linha {line_number}")

        else:
            raise SyntaxError(f"esperava um assign na linha {line_number}")