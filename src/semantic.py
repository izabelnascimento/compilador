from src.util import Util


class Semantic:
    def __init__(self, tokens, symbol_table, folder, file_name):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.folder = folder
        self.file_name = file_name

    def start_semantic(self):
        print("\n------------------- ANÁLISE SEMÂNTICA -------------------")
        self.check_declarations()
        self.check_expression_types()
        self.check_function_calls()
        self.check_function_returns()
        self.check_control_flow_conditions()
        Util.save_symbol_table_to_csv(self.symbol_table, f'{self.folder}/semantic', self.file_name)
        Util.print_sucess("\nAnálise semântica concluída sem erros.")

    # Garante que todos os identificadores usados foram declarados no escopo apropriado.
    def check_declarations(self):
        print("\n- Verificando declaração -")
        declared_symbols = list()

        for symbol in self.symbol_table:
            if symbol.kind:
                declared_symbols.append(symbol)
            elif not self.contains(symbol, declared_symbols):
                raise SyntaxError(
                    f"[Erro] Identificador '{symbol.name}' usado na linha {symbol.line} mas não declarado."
                )

    # Confirma se os operandos têm tipos compatíveis nas expressões.
    def check_expression_types(self):
        print("\n- Verificando tipos em expressões -")
        for symbol in self.symbol_table:
            next_token_index = self.find_next_token(symbol, 'ASSIGN')
            if next_token_index:
                self.check_expression(symbol.kind, next_token_index + 1)

    # Confere se as chamadas usam o número e tipo corretos de argumentos.
    def check_function_calls(self):
        print("\n- Verificando chamadas de funções -")
        for symbol in self.symbol_table:
            if symbol.kind in ('FUNCTION', 'PROCEDURE'):
                for token in self.tokens:
                    index = 0
                    if token[0] == symbol.id and token[1] in ('FUNCTION', 'PROCEDURE'):
                        args = list()
                        index += 4
                        for i in range(index, len(self.tokens)):
                            if self.tokens[i][1] == 'INT':
                                args.append('INT')
                            elif self.tokens[i][1] == 'BOOL':
                                args.append('BOOL')
                            elif self.tokens[i][1] == 'SEMICOLON':
                                break
                        self.check_calls(args)

    # Verifica se existe return com tipo compatível nas funções.
    def check_function_returns(self):
        print("\n- Verificando compatibilidade do returns -")

   # Garante que as expressões condicionais em if e while são do tipo booleano.
    def check_control_flow_conditions(self):
        print("\n- Verificando instrução de controle de fluxo -")

    # check_declarations
    def contains(self, symbol, declared_symbols):
        for declared in declared_symbols:
            if declared.name == symbol.name and (
                    declared.scope_id == symbol.scope_id
                    or self.parent_scope(declared, symbol)
            ):
                self.update_symbol(symbol, declared.kind)
                return True
        return False

    @staticmethod
    def parent_scope(declared, symbol):
        if declared.scope_id == 2 or symbol.scope_token == 'IF' or symbol.scope_token == 'WHILE':
            return True
        return False

    def update_symbol(self, symbol, kind):
        for i, s in enumerate(self.symbol_table):
            if s == symbol:
                symbol.kind = kind
                self.symbol_table[i] = symbol
                break
        Util.save_symbol_table_to_csv(self.symbol_table, f'{self.folder}/semantic', self.file_name)

    # check_expression_types
    def check_expression(self, expected_kind, index):
        while self.tokens[index][1] != 'SEMICOLON':
            token_id, token_type, token_value, line_number = self.tokens[index]

            if token_type == 'IDENTIFIER':
                symbol = self.find_symbol(token_id)
                symbol_kind = symbol.kind if symbol and symbol.kind else None
                if symbol_kind == 'FUNCTION':
                    symbol_kind = self.get_function_type(symbol)
            elif token_type == 'NUMBER':
                symbol_kind = 'INT'
            elif token_type in {'TRUE', 'FALSE'}:
                symbol_kind = 'BOOL'
            else:
                index += 1
                continue

            if symbol_kind != expected_kind:
                raise SyntaxError(
                    f"[Erro] Atribuição de tipo incompatível na linha {line_number}. "
                    f"Esperado: {expected_kind}, encontrado: {symbol_kind or 'desconhecido'}."
                )
            return

    def get_function_type(self, symbol):
        original_symbol = self.find_symbol_by_name_and_scope(symbol)
        return self.find_next_token_in_function(original_symbol, 'RETURN')[1]

    def find_symbol_by_name_and_scope(self, symbol):
        for symbol_one in self.symbol_table:
            if symbol_one.name == symbol.name and symbol_one.scope_id == symbol.scope_id:
                return symbol_one

    def find_symbol(self, token_id):
        line = 1
        for symbol in self.symbol_table:
            line = symbol.line
            if symbol.id == token_id:
                return symbol
        raise SyntaxError(
            f"[Erro] Atribuição de tipo errada na linha {line}."
        )

    def find_next_token_in_function(self, symbol, token_name):
        for index, token in enumerate(self.tokens):
            if symbol.id == token[0]:
                # A partir desse ponto, procura por um token 'RETURN'
                for i in range(index, len(self.tokens)):
                    if self.tokens[i][1] == token_name:
                        return self.tokens[i+1]
                break  # Se não encontrar 'RETURN' após o símbolo, encerra
        return None  # Caso não encontre o símbolo ou o RETURN

    def find_next_token(self, symbol, token_name):
        index = 0
        for token in self.tokens:
            index += 1
            if symbol.id == token[0] and self.tokens[index][1] == token_name:
                return index

    # check_function_calls
    def check_calls(self, args_defined):
        index = 0
        for token in self.tokens:
            if token[1] == 'CALL':
                index += 2
                self.get_arguments(index, args_defined, token[3])
            index += 1

    def get_arguments(self, index, args_defined, line):
        args = list()
        for i in range(index, len(self.tokens)):
            token = self.tokens[index]
            if token[1] == 'NUMBER':
                args.append('INT')
            elif token[1] == 'BOOL':
                args.append('BOOL')
            elif token[1] == 'RPAREN':
                break
            index += 1
        if args_defined != args:
            raise SyntaxError(
                f"[Erro] Argumentos inválidos na linha {line}. "
            )
