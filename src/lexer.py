import re


class Lexer:
    def __init__(self):
        self.tokens = [
            ('PROGRAM', r'programa'),
            ('ASSIGN', r'=>'),
            ('NUMBER', r'\d+'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('WHITESPACE', r'\s+'),
            ('BEGIN', r'inicio'),
            ('END', r'fim'),
            ('SHOW', r'mostre'),
            ('TRUE', r'verdadeiro'),
            ('FALSE', r'falso'),
            ('NOT', r'nao'),
            ('AND', r'e'),
            ('OR', r'ou'),
            ('EQUAL', r'=='),
            ('NOT_EQUAL', r'!='),
            ('GREATER', r'>'),
            ('GREATER_EQUAL', r'>='),
            ('LESS', r'<'),
            ('LESS_EQUAL', r'<='),
            ('COMMENT', r'//.*'),
            ('BLOCK_COMMENT', r'/\*.*?\*/')
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
                    elif token_type in ('COMMENT', 'BLOCK_COMMENT'):
                        pass  # Ignorar comentários
                    else:
                        yield token_type, match.group(0), line_number
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character '{code[position]}' on line {line_number}")
        print("Análise Léxica concluída sem erros")
