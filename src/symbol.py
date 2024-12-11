class Symbol:
    def __init__(self, id, kind, line):
        self.id = id
        self.kind = kind
        self.line = line

    def __repr__(self):
        return f"Symbol(id='{self.id}', kind='{self.kind}', line={self.line})"

    @staticmethod
    def symbol_table(tokens) -> list:
        symbol_table = []
        for token_type, token_value, token_line in tokens:
            if token_type == 'IDENTIFIER':
                symbol_table.append(Symbol(token_value, 'IDENTIFIER', token_line))
        return symbol_table
