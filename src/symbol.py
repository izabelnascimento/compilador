class Symbol:
    def __init__(self, id, token, name, kind, line, scope_name, scope_token, scope_id):
        self.id = id
        self.token = token
        self.name = name
        self.kind = kind
        self.line = line
        self.scope_name = scope_name
        self.scope_token = scope_token
        self.scope_id = scope_id

    def __repr__(self):
        return f"Symbol(" \
               f"id={self.id}, " \
               f"name='{self.name}', " \
               f"token='{self.token}', " \
               f"kind='{self.kind}', " \
               f"line={self.line}, " \
               f"scope_name='{self.scope_name}' " \
               f"scope_token='{self.scope_token}' " \
               f"scope_id={self.scope_id})"

    @staticmethod
    def symbol_table(tokens) -> list:
        symbol_table = []
        for token_id, token_type, token_value, token_line in tokens:
            if token_type == 'IDENTIFIER':
                symbol_table.append(Symbol(token_id, 'IDENTIFIER', token_value, '', token_line, '', '', ''))
        return symbol_table
