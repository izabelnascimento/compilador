import re


class Lexer:
    def __init__(self):
        self.tokens = [
            ('PROGRAM', r'\bprograma\b'),
            ('ASSIGN', r'=>'),  # Certifique-se de que ASSIGN esteja antes
            ('EQUAL', r'=='),
            ('NOT_EQUAL', r'!='),
            ('GREATER_EQUAL', r'>='),
            ('LESS_EQUAL', r'<='),
            ('NUMBER', r'\b\d+\b'),
            ('BREAK', r'\bquebra\b'),
            ('PLUS', r'\+'),
            ('MINUS', r'-(?!>)'),
            ('MULTIPLY', r'\*'),
            ('COMMENT', r'//.*'),
            ('BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMICOLON', r';'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('QUOTES', r'\"'),
            ('WHITESPACE', r'\s+'),
            ('BEGIN', r'\binicio\b'),
            ('END', r'\bfim\b'),
            ('SHOW', r'\bmostre\b'),
            ('TRUE', r'\bverdadeiro\b'),
            ('FALSE', r'\bfalso\b'),
            ('NOT', r'\bnao\b'),
            ('AND', r'\be\b'),
            ('OR', r'\bou\b'),
            ('GREATER', r'>(?<!-)'),
            ('LESS', r'<'),
            ('VAR', r'\bvar\b'),
            ('INT', r'\bint\b'),
            ('BOOL', r'\bbool\b'),
            ('DO', r'\bfaca\b'),
            ('IF', r'\bse\b'),
            ('ELSE', r'\bsenao\b'),
            ('THEN', r'\bentao\b'),
            ('FUNCTION', r'\bfuncao\b'),
            ('PROCEDURE', r'\bprocedimento\b'),
            ('RETURN', r'\bretorna\b'),
            ('CALL', r'\bchamar\b'),
            ('WHILE', r'\benquanto\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
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
