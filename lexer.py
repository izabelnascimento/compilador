import re


class Lexer:
    def __init__(self):
        # Define os padrões de tokens
        self.tokens = [
            ('NUMBER', r'\d+'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN', r'='),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('WHITESPACE', r'\s+'),
        ]

    def tokenize(self, code):
        position = 0
        while position < len(code):
            match = None
            for token_type, pattern in self.tokens:
                regex = re.compile(pattern)
                match = regex.match(code, position)
                if match:
                    if token_type != 'WHITESPACE':  # Ignora espaços
                        yield (token_type, match.group(0))
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {code[position]}")
        print("Análise Léxica concluída sem erros")
