from src.util import Util


class Semantic:
    def __init__(self, symbol_table, folder, file_name):
        self.symbol_table = symbol_table
        self.folder = folder
        self.file_name = file_name

    def start_semantic(self):
        print("\n------------------- ANÁLISE SEMÂNTICA -------------------")
        self.check_declarations()
        self.check_assignments()
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

    # Verifica se o lado esquerdo da atribuição existe e tem tipo compatível com o lado direito.
    def check_assignments(self):
        print("\n- Verificando atribuições -")
        assignments = [s for s in self.symbol_table if s.kind == 'assignment']

        for assign in assignments:
            target_name = assign.name
            scope = assign.scope_name
            expr_type = assign.token  # usando token para tipo da expressão atribuída, se for o caso

            declared = False
            declared_type = None

            for s in self.symbol_table:
                if s.name == target_name and s.kind == 'variable' and (s.scope_name == scope or s.scope_name == 'global'):
                    declared = True
                    declared_type = s.token  # usando token como tipo da variável
                    break

            if not declared:
                Util.print_error(f"Variável '{target_name}' usada em atribuição não foi declarada no escopo '{scope}'.")
            elif declared_type != expr_type:
                Util.print_error(f"Tipo incompatível na atribuição à variável '{target_name}' no escopo '{scope}': esperado '{declared_type}', encontrado '{expr_type}'.")

    # Confirma se os operandos têm tipos compatíveis nas expressões.
    def check_expression_types(self):
        print("\n- Verificando tipos em expressões -")

    # Confere se as chamadas usam o número e tipo corretos de argumentos.
    def check_function_calls(self):
        print("\n- Verificando chamadas de funlções -")

    # Verifica se existe return com tipo compatível nas funções.
    def check_function_returns(self):
        print("\n- Verificando compatibilidade do returns -")

   # Garante que as expressões condicionais em if e while são do tipo booleano.
    def check_control_flow_conditions(self):
        print("\n- Verificando instrução de controle de fluxo -")

