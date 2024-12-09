from lexer import Lexer
from syntax import Syntax


def main():
    file_path = 'code.txt'
    code = read_code_from_file(file_path)
    if not code:
        return

    try:
        lexer = Lexer()
        tokens = list(lexer.tokenize(code))
        print("\nTokens:", tokens)
        try:
            syntax = Syntax(tokens)
            syntax.parse()
            print("\nAnálise sintática concluída sem erros.")
        except SyntaxError as e:
            print(f"\nErro durante a análise sintática: {e}")
    except SyntaxError as e:
        print(f"\nErro durante a análise léxica: {e}")


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


if __name__ == "__main__":
    main()
