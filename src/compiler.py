import sys

from src.lexer import Lexer
from src.symbol import Symbol
from src.syntax import Syntax


class Compiler:

    def compile(self, file_path):
        code = self.read_code_from_file(file_path)
        if not code:
            return

        print(f"\n-------------- Compilando arquivo {file_path} -------------- ")
        try:
            lexer = Lexer()
            tokens = list(lexer.tokenize(code))
            print("\nTokens:", tokens)
            symbol_table = Symbol.symbol_table(tokens)
            print("\nSymbol Table:", symbol_table)
            self.print_sucess("Análise Léxica concluída sem erros")
            try:
                syntax = Syntax(tokens)
                # syntax.parse()
                # self.print_sucess("\nAnálise sintática concluída sem erros.")
            except SyntaxError as e:
                self.print_error(f"\nErro durante a análise sintática: {e}")
        except SyntaxError as e:
            self.print_error(f"\nErro durante a análise léxica: {e}")

    @staticmethod
    def read_code_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            return code
        except FileNotFoundError:
            print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
            return ""
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return ""

    @staticmethod
    def print_error(texto):
        print(f"\033[31m{texto}\033[0m")

    @staticmethod
    def print_sucess(mensagem):
        sys.stdout.write(f"\033[32m{mensagem}\033[0m\n")
