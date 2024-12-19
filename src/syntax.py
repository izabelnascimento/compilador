from src.util import Util


class Syntax:
    def __init__(self, tokens, symbol_table, current_scope):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.current_token_index = 0
        self.current_scope = current_scope

    def start_syntax(self, folder, file_name):
        print("\n------------------- ANÁLISE SINTÁTICA -------------------")
        self.parse()
        print("\nSymbol Table:", self.symbol_table)
        Util.save_symbol_table_to_csv(self.symbol_table, f'{folder}/syntax', file_name)
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
        token = self.current_token()
        self.add_symbol_type([token[0]], 'PROGRAM')
        self.current_scope = token
        self.add_scope([token[0]])
        self.add_scope([self.current_token()[0]])
        self.eat('IDENTIFIER')
        self.eat('SEMICOLON')
        self.eat('BEGIN')
        self.body()
        self.eat('END')

    def body(self):
        token = self.current_token()
        if token:
            token_type = self.current_token()[1]
            if token_type == 'VAR':
                self.declaration()
            elif token_type == 'IF':
                self.conditional()
            elif token_type in ('PROCEDURE', 'FUNCTION'):
                self.subroutine()
            elif token_type == 'WHILE':
                self.loop()
            elif token_type == 'IDENTIFIER':
                self.assignment()
            elif token_type == 'SHOW':
                self.show()
            elif token_type == 'CALL':
                self.call()
                self.eat('SEMICOLON')
                self.body()
            elif token_type == 'RETURN':
                self.return_statement()
            elif token_type == 'BREAK':
                self.break_statement()

    def declaration(self):
        self.eat('VAR')
        tokens_id = []
        while True:
            current_token = self.current_token()
            tokens_id.append(current_token[0])
            self.add_scope([current_token[0]])
            self.eat('IDENTIFIER')
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
        self.add_symbol_type([self.current_token()[0]], 'PROCEDURE')
        self.add_scope([self.current_token()[0]])
        before_scope = self.current_scope
        self.update_scope()
        self.eat('IDENTIFIER')
        if self.current_token()[1] == 'LPAREN':
            self.eat('LPAREN')
            self.parameters()
            self.eat('RPAREN')
        self.eat('SEMICOLON')
        self.eat('BEGIN')
        self.body()
        self.eat('END')
        self.return_scope(before_scope)

    def function_declaration(self):
        self.eat('FUNCTION')
        self.add_symbol_type([self.current_token()[0]], 'FUNCTION')
        self.add_scope([self.current_token()[0]])
        before_scope = self.current_scope
        self.update_scope()
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
        self.return_scope(before_scope)

    def parameters(self):
        while True:
            token_id = self.current_token()[0]
            self.add_scope([self.current_token()[0]])
            self.eat('IDENTIFIER')
            self.eat('COLON')
            self.eat_type_var([token_id])
            if self.current_token() and self.current_token()[1] == 'COMMA':
                self.eat('COMMA')
            else:
                break

    def arguments(self):
        while True:
            self.expression()
            if self.current_token() and self.current_token()[1] == 'COMMA':
                self.eat('COMMA')
            else:
                break

    def statement(self):
        token_id, token_type, value, line_number = self.current_token()
        if token_type == 'IDENTIFIER':
            self.add_scope([self.current_token()[0]])
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
        before_scope = self.current_scope
        self.update_scope()
        self.eat('IF')
        self.expression()
        self.eat('THEN')
        self.statement()
        if self.current_token() and self.current_token()[1] == 'ELSE':
            self.eat('ELSE')
            self.statement()
        self.eat('END')
        self.return_scope(before_scope)
        self.body()

    def loop(self):
        before_scope = self.current_scope
        self.update_scope()
        self.eat('WHILE')
        self.expression()
        self.eat('DO')
        self.body()
        self.eat('END')
        self.return_scope(before_scope)
        self.body()

    def return_statement(self):
        token = self.current_token()
        # if self.current_scope[1] != 'FUNCTION':
        #     raise SyntaxError(f"RETURN deve estar dentro de uma FUNCTION, linha {token[3]}")
        self.eat('RETURN')
        if token and token[1] != 'SEMICOLON':
            self.expression()
        self.eat('SEMICOLON')

    def break_statement(self):
        token = self.current_token()
        # if self.current_scope[1] != 'WHILE':
        #     raise SyntaxError(f"BREAK deve estar dentro de um LOOP, linha {token[3]}")
        self.eat('BREAK')
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
            self.add_scope([self.current_token()[0]])
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
        elif token_type == 'BREAK':
            self.break_statement()
        else:
            raise SyntaxError(f"Fator inválido na linha {line_number}")

    def eat_type_var(self, tokens_id):
        token_id, token_type, value, line_number = self.current_token()
        if self.current_token() and token_type == 'INT':
            self.symbol_table = self.add_symbol_type(tokens_id, 'INT')
            self.eat('INT')
        elif self.current_token() and token_type == 'BOOL':
            self.symbol_table = self.add_symbol_type(tokens_id, 'BOOL')
            self.eat('BOOL')
        else:
            raise SyntaxError(f"esperava o tipo 'INT ou BOOL' na linha {line_number}")

    def assignment(self):
        self.add_scope([self.current_token()[0]])
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        self.expression()
        self.eat('SEMICOLON')
        self.body()

    def show(self):
        self.eat('SHOW')
        self.eat('LPAREN')
        self.expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        self.body()

    def call(self):
        self.eat('CALL')
        self.add_scope([self.current_token()[0]])
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        self.arguments()
        self.eat('RPAREN')

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

    def add_scope(self, tokens_id):
        new_table = []
        for symbol in self.symbol_table:
            if symbol.id in tokens_id:
                symbol.scope_id = self.current_scope[0]
                symbol.scope_token = self.current_scope[1]
                symbol.scope_name = self.current_scope[2]
            new_table.append(symbol)
        self.symbol_table = new_table
        return new_table

    def update_scope(self):
        self.current_scope = self.current_token()

    def return_scope(self, before_scope):
        self.current_scope = before_scope
