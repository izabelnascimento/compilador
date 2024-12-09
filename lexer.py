import re


class Lexer:
    def __init__(self):
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
        line_number = 1
        while position < len(code):
            match = None
            for token_type, pattern in self.tokens:
                regex = re.compile(pattern)
                match = regex.match(code, position)
                if match:
                    if token_type == 'WHITESPACE':
                        line_number += match.group(0).count('\n')
                    else:
                        yield (token_type, match.group(0), line_number)
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character '{code[position]}' on line {line_number}")
        print("Análise Léxica concluída sem erros")
