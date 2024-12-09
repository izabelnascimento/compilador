class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {"global": {}}  # Tabela de símbolos com escopos
        self.current_scope = "global"  # Controle do escopo atual

    def enter_scope(self, scope_name):
        if scope_name not in self.symbol_table:
            self.symbol_table[scope_name] = {}
            self.current_scope = scope_name

    def exit_scope(self):
        self.current_scope = "global"

    def analyze(self, tokens, token_context=None, previous_token=None):
        for token_type, value in tokens:
            # Exemplo: Validação de Identificadores
            if token_type == 'IDENTIFIER' and 'usage' in token_context:
                if value not in self.symbol_table[self.current_scope] and value not in self.symbol_table["global"]:
                    raise ValueError(f"Undefined variable '{value}' in scope '{self.current_scope}'.")

            # Exemplo: Declaração de Variável
            if token_type == 'IDENTIFIER' and 'declaration' in token_context:
                if value in self.symbol_table[self.current_scope]:
                    raise ValueError(f"Variable '{value}' already declared in scope '{self.current_scope}'.")
                self.symbol_table[self.current_scope][value] = "int"  # Adiciona com tipo 'int'

            # Exemplo: Validação de Atribuição
            if token_type == 'ASSIGN':
                variable = previous_token[1]  # Token anterior assume ser variável
                if (variable not in self.symbol_table[self.current_scope] and variable
                        not in self.symbol_table["global"]):
                    raise ValueError(f"Cannot assign to undefined variable '{variable}'.")
