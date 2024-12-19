import re

from src.util import Util
from src.symbol import Symbol


class Lexer:
    def __init__(self):
        self.tokens = [
            ('PROGRAM', r'\bprograma\b'),
            ('ASSIGN', r'=>'),
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
            ('RESTO', r'%'),
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

    def start_lexer(self, code, folder, file_name):
        print("\n------------------- ANÁLISE LEXICA -------------------")
        tokens = list(self.tokenize(code))
        print("\nTokens:", tokens)
        Util.save_tokens_to_csv(tokens, f'{folder}/lexer', file_name)
        symbol_table = Symbol.symbol_table(tokens)
        print("\nSymbol Table:", symbol_table)
        Util.save_symbol_table_to_csv(symbol_table, f'{folder}/lexer', file_name)
        Util.print_sucess("Análise Léxica concluída sem erros")
        return tokens, symbol_table

    import re

    def tokenize(self, code):
        position = 0
        line_number = 1
        token_id = 1  # Inicializa o ID do token

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
                        # Retorna a estrutura com o ID
                        yield token_id, token_type, match.group(0), line_number
                        token_id += 1  # Incrementa o ID
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character '{code[position]}' on line {line_number}")

