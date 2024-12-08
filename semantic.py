class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, tokens):
        for token_type, value in tokens:
            if token_type == 'IDENTIFIER':
                # Exemplo: Checar se a variável foi declarada
                if value not in self.symbol_table:
                    raise ValueError(f"Undefined variable: {value}")
            elif token_type == 'ASSIGN':
                pass  # Validação de atribuições pode ir aqui
            elif token_type == 'NUMBER':
                pass  # Exemplo: verificar tipos, etc.
