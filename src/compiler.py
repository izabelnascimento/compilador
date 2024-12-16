from src.lexer import Lexer
from src.syntax import Syntax
from src.util import Util


class Compiler:

    @staticmethod
    def compile(file_name):
        code = Util.read_code_from_file(f'../resources/test_lexer/{file_name}')
        if not code:
            return

        print(f"\n-------------- Compilando arquivo {file_name} -------------- ")
        try:
            lexer = Lexer()
            tokens = lexer.start_lexer(code, file_name)
            try:
                syntax = Syntax(tokens)
                syntax.start_syntax()
            except SyntaxError as e:
                Util.print_error(f"\nErro durante a análise sintática: {e}")
        except SyntaxError as e:
            Util.print_error(f"\nErro durante a análise léxica: {e}")
