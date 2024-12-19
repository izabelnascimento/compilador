from src.util import Util


class Syntax:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.current_token_index = 0

    def start_syntax(self):
        print("\n------------------- ANÁLISE SINTÁTICA -------------------")
        self.parse()
        print("\nSymbol Table:", self.symbol_table)
        Util.print_sucess("\nAnálise sintática concluída sem erros.")

    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def eat(self, token_type):
        if self.current_token() and self.current_token()[1] == token_type:
            self.current_token_index += 1
        else:
            expected = token_type
            found = self.current_token()[1] if self.current_token() else "EOF"
            raise SyntaxError(
                f"Esperado token '{expected}', mas encontrado '{found}' na linha {self.current_token()[3] if self.current_token() else 'desconhecida'}."
            )

    def parse(self):
        self.program()

    def program(self):
        self.eat('PROGRAM')
        self.eat('IDENTIFIER')
        self.eat('SEMICOLON')
        self.eat('BEGIN')
        self.body()
        self.eat('END')

    def body(self):
        if self.current_token() and self.current_token()[1] == 'VAR':
            self.declaration()
        elif self.current_token() and self.current_token()[1] == 'IF':
            self.conditional()
        elif self.current_token() and self.current_token()[1] in ('PROCEDURE', 'FUNCTION'):
            self.subroutine()
        elif self.current_token() and self.current_token()[1] in 'WHILE':
            self.loop()
        elif self.current_token() and self.current_token()[1] in 'IDENTIFIER':
            self.assignment()
        elif self.current_token() and self.current_token()[1] in 'SHOW':
            self.show()
        elif self.current_token() and self.current_token()[1] in 'CALL':
            self.call()
            self.eat('SEMICOLON')
            self.body()
        elif self.current_token() and self.current_token()[1] in 'RETURN':
            self.return_statement()

    def declaration(self):
        self.eat('VAR')
        tokens_id = []
        while True:
            current_token = self.current_token()
            tokens_id.append(current_token[0])
            self.eat('IDENTIFIER')  # Nome da variável
            if current_token and self.current_token()[1] == 'COMMA':
                self.eat('COMMA')
            else:
                break
        self.eat('COLON')
        self.eat_type_var(tokens_id)
        self.eat('SEMICOLON')
        self.body()

    def subroutine(self):
        if self.current_token()[1] == 'PROCEDURE':
            self.procedure_declaration()
        elif self.current_token()[1] == 'FUNCTION':
            self.function_declaration()
        self.body()

    def procedure_declaration(self):
        self.eat('PROCEDURE')
        self.eat('IDENTIFIER')
        if self.current_token()[1] == 'LPAREN':
            self.eat('LPAREN')
            self.parameters()
            self.eat('RPAREN')
        self.eat('SEMICOLON')
        self.eat('BEGIN')
        self.body()
        self.eat('END')

    def function_declaration(self):
        self.eat('FUNCTION')
        self.eat('IDENTIFIER')
        if self.current_token()[1] == 'LPAREN':
            self.eat('LPAREN')
            self.parameters()
            self.eat('RPAREN')
        self.eat('RETURN')
        self.eat_type_var([self.current_token()[0]])
        self.eat('SEMICOLON')
        self.eat('BEGIN')
        self.body()
        self.eat('END')

    def parameters(self):
        while True:
            self.eat('IDENTIFIER')
            self.eat('COLON')
            self.eat_type_var([self.current_token()[0]])
            if self.current_token() and self.current_token()[1] == 'COMMA':
                self.eat('COMMA')
            else:
                break

    def arguments(self):
        while True:
            # self.eat('IDENTIFIER')
            self.expression()
            if self.current_token() and self.current_token()[1] == 'COMMA':
                self.eat('COMMA')
            else:
                break

    def statement(self):
        token_id, token_type, value, line_number = self.current_token()
        if token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token()[1] == 'ASSIGN':
                self.eat('ASSIGN')
                self.expression()
            elif self.current_token()[1] == 'LPAREN':
                self.eat('LPAREN')
                while self.current_token() and self.current_token()[1] != 'RPAREN':
                    self.expression()
                    if self.current_token()[1] == 'COMMA':
                        self.eat('COMMA')
                self.eat('RPAREN')
            self.eat('SEMICOLON')
        elif token_type == 'IF':
            self.conditional()
        elif token_type == 'WHILE':
            self.loop()
        elif token_type == 'RETURN':
            self.return_statement()
        elif token_type == 'BREAK':
            self.break_statement()
        elif token_type == 'SHOW':
            self.show()
        else:
            raise SyntaxError(f"Comando inválido na linha {line_number}")

    def conditional(self):
        self.eat('IF')
        self.expression()
        self.eat('THEN')
        self.statement()
        if self.current_token() and self.current_token()[1] == 'ELSE':
            self.eat('ELSE')
            self.statement()
        self.eat('END')
        self.body()

    def loop(self):
        self.eat('WHILE')
        self.expression()
        self.eat('DO')
        self.body()
        self.eat('END')
        self.body()

    def return_statement(self):
        self.eat('RETURN')
        if self.current_token() and self.current_token()[1] != 'SEMICOLON':
            self.expression()
        self.eat('SEMICOLON')

    def break_statement(self):
        self.eat('BREAK')
        if self.current_token() and self.current_token()[1] != 'SEMICOLON':
            self.expression()
        self.eat('SEMICOLON')

    def expression(self):
        self.simple_expression()
        while self.current_token() and self.current_token()[1] in ('EQUAL', 'NOT_EQUAL', 'GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL'):
            self.eat(self.current_token()[1])
            self.simple_expression()

    def simple_expression(self):
        if self.current_token() and self.current_token()[1] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[1])
        self.term()
        while self.current_token() and self.current_token()[1] in ('PLUS', 'MINUS'):
            self.eat(self.current_token()[1])
            self.term()

    def term(self):
        self.factor()
        while self.current_token() and self.current_token()[1] in ('MULTIPLY', 'DIVIDE', 'AND', 'OR', 'RESTO'):
            self.eat(self.current_token()[1])
            self.factor()

    def factor(self):
        token_id, token_type, value, line_number = self.current_token()
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
        elif token_type == 'CALL':
            self.call()
        else:
            raise SyntaxError(f"Fator inválido na linha {line_number}")

    def eat_type_var(self, tokens_id):
        token_id, token_type, value, line_number = self.current_token()
        if self.current_token() and self.current_token()[1] == 'INT':
            self.symbol_table = self.add_symbol_type(tokens_id, 'INT')
            self.eat('INT')
        elif self.current_token() and self.current_token()[1] == 'BOOL':
            self.symbol_table = self.add_symbol_type(tokens_id, 'BOOL')
            self.eat('BOOL')
        else:
            raise SyntaxError(f"esperava o tipo 'INT ou BOOL' na linha {line_number}")

    def assignment(self):
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        self.expression()
        self.eat('SEMICOLON')
        self.body()

    def add_symbol_type(self, tokens_id, symbol_type):
        new_table = []

        for symbol in self.symbol_table:
            if symbol.id in tokens_id:
                symbol.kind = symbol_type
            new_table.append(symbol)

        self.symbol_table = new_table
        return new_table

    def search_symbol(self, id):
        for symbol in self.symbol_table:
            if symbol.id == id:
                return symbol
        return None

    def show(self):
        self.eat('SHOW')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        self.body()

    def call(self):
        self.eat('CALL')
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        self.arguments()
        self.eat('RPAREN')
