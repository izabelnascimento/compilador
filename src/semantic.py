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

    def check_expression_types(self):
        print("\n- Verificando tipos em expressões -")
        for i in range(len(self.tokens) - 1):
            current = self.tokens[i]
            next_token = self.tokens[i + 1]

            if current[1] == 'IDENTIFIER' and next_token[1] == 'ASSIGN':
                try:
                    symbol = self.find_symbol(current[0])
                    if symbol and symbol.kind in {'INT', 'BOOL'}:
                        self.check_expression(symbol.kind, i + 2)
                except Exception as e:
                    raise SyntaxError(f"[Erro] Atribuição inválida na linha {current[3]}: {str(e)}")

    def check_function_calls(self):
        print("\n- Verificando chamadas de funções -")
        for symbol in self.symbol_table:
            if symbol.kind in ('FUNCTION', 'PROCEDURE'):
                index = 0
                for token in self.tokens:
                    if token[0] == symbol.id and self.tokens[index-1][1] in ('FUNCTION', 'PROCEDURE'):
                        args = list()
                        index += 1
                        for i in range(index, len(self.tokens)):
                            actual_token = self.tokens[i]
                            if actual_token[1] == 'INT':
                                args.append('INT')
                            elif actual_token[1] == 'BOOL':
                                args.append('BOOL')
                            elif actual_token[1] == 'RPAREN':
                                break
                        self.check_calls(args)
                    else:
                        index += 1

    def check_function_returns(self):
        print("\n- Verificando compatibilidade do returns -")
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            if token[1] == 'FUNCTION':
                # Pega o identificador da função (vem logo após o token FUNCTION)
                func_identifier_token = self.tokens[i + 1]
                function_symbol = self.find_symbol(func_identifier_token[0])
                expected_type = self.get_function_type(function_symbol)

                found_return = False

                # Avança até o início do corpo da função (BEGIN)
                while i < len(self.tokens) and self.tokens[i][1] != 'BEGIN':
                    i += 1

                body_start = i
                nest = 1
                i += 1

                # Percorre o corpo da função até o END correspondente
                while i < len(self.tokens) and nest > 0:
                    if self.tokens[i][1] == 'BEGIN':
                        nest += 1
                    elif self.tokens[i][1] == 'END':
                        nest -= 1
                    i += 1

                body_end = i

                # Procura por RETURN dentro do corpo da função
                for j in range(body_start, body_end):
                    if self.tokens[j][1] == 'RETURN':
                        found_return = True
                        try:
                            self.check_expression(expected_type, j + 1)
                        except SyntaxError as e:
                            raise SyntaxError(
                                f"[Erro] Tipo de retorno inválido na função '{function_symbol.name}' "
                                f"na linha {self.tokens[j][3]}: {str(e)}"
                            )

                if not found_return:
                    raise SyntaxError(
                        f"[Erro] Função '{function_symbol.name}' na linha {token[3]} não possui retorno."
                    )
            else:
                i += 1


    def check_control_flow_conditions(self):
        print("\n- Verificando instrução de controle de fluxo -")
        for i, token in enumerate(self.tokens):
            if token[1] in {'IF', 'WHILE'}:
                condition_token = self.tokens[i + 2]  # Assume estrutura: SE ( condição ) ...
                token_type = condition_token[1]

                if token_type == 'IDENTIFIER':
                    cond_symbol = self.find_symbol(condition_token[0])
                    cond_type = cond_symbol.kind
                elif token_type in {'TRUE', 'FALSE'}:
                    cond_type = 'BOOL'
                elif token_type == 'NUMBER':
                    cond_type = 'INT'
                else:
                    cond_type = None

                # Agora aceitamos INT ou BOOL como condição válida
                if cond_type not in {'INT', 'BOOL'}:
                    raise SyntaxError(
                        f"[Erro] Condição em '{token[1]}' na linha {token[3]} precisa ser do tipo INT ou BOOL."
                    )

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
        return declared.scope_id == 2 or symbol.scope_token in {'IF', 'WHILE'}

    def update_symbol(self, symbol, kind):
        for i, s in enumerate(self.symbol_table):
            if s == symbol:
                symbol.kind = kind
                self.symbol_table[i] = symbol
                break
        Util.save_symbol_table_to_csv(self.symbol_table, f'{self.folder}/semantic', self.file_name)

    def check_expression(self, expected_kind, index):
        line_number = self.tokens[index][3]
        allowed_kinds = {'INT', 'BOOL'}
        expression_types = set()

        while index < len(self.tokens) and self.tokens[index][1] != 'SEMICOLON':
            token_id, token_type, token_value, line_number = self.tokens[index]

            try:
                if token_type == 'CALL':
                    func_id_token = self.tokens[index + 1]
                    func_symbol = self.find_symbol(func_id_token[0])
                    if func_symbol.kind == 'FUNCTION':
                        expression_types.add(self.get_function_type(func_symbol))
                    index += 1  # pular o identificador da função
                elif token_type == 'IDENTIFIER':
                    symbol = self.find_symbol(token_id)
                    if symbol and symbol.kind in allowed_kinds:
                        expression_types.add(symbol.kind)
                    elif symbol and not symbol.kind:
                        raise SyntaxError(
                            f"[Erro] Identificador '{symbol.name}' usado na linha {line_number} "
                            f"não possui tipo definido."
                        )
                elif token_type == 'NUMBER':
                    expression_types.add('INT')
                elif token_type in {'TRUE', 'FALSE'}:
                    expression_types.add('BOOL')
            except Exception as e:
                raise SyntaxError(
                    f"[Erro] Problema ao verificar expressão na linha {line_number}: {str(e)}"
                )

            index += 1

        if not expression_types:
            raise SyntaxError(
                f"[Erro] Expressão vazia ou inválida na linha {line_number}."
            )

        if expected_kind not in expression_types:
            raise SyntaxError(
                f"[Erro] Atribuição ou retorno com tipo incompatível na linha {line_number}. "
                f"Esperado: {expected_kind}, encontrado: {', '.join(expression_types)}."
            )

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
                print(f"✔️ Encontrado símbolo '{symbol.name}' (tipo: {symbol.kind}) na linha {symbol.line}")
                return symbol
        print(f"❌ Token ID {token_id} não encontrado na tabela de símbolos.")
        raise SyntaxError(
            f"[Erro] Atribuição de tipo errada na linha {line}."
        )

    def find_next_token_in_function(self, symbol, token_name):
        for index, token in enumerate(self.tokens):
            if symbol.id == token[0]:
                for i in range(index, len(self.tokens)):
                    if self.tokens[i][1] == token_name:
                        return self.tokens[i + 1]
                break
        return None

    def find_next_token(self, symbol, token_name):
        index = 0
        for token in self.tokens:
            index += 1
            if symbol.id == token[0] and self.tokens[index][1] == token_name:
                return index

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
            elif token[1] in {'FALSE', 'TRUE'}:
                args.append('BOOL')
            elif token[1] == 'IDENTIFIER':
                args.append(self.get_symbol_type_by_id(token[0]))
            elif token[1] == 'RPAREN':
                break
            index += 1
        if args_defined != args:
            raise SyntaxError(
                f"[Erro] Argumentos inválidos na linha {line}. "
            )

    def get_symbol_type_by_id(self, token_id):
        symbol = self.find_symbol(token_id)
        return symbol.kind
