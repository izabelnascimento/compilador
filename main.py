from lexer import Lexer
# from semantic import SemanticAnalyzer


def main():
    code = read_code_from_file('code.txt')
    lexer = Lexer()
    tokens = list(lexer.tokenize(code))

    print("Tokens:", tokens)

    # semantic_analyzer = SemanticAnalyzer()
    # try:
    #     semantic_analyzer.analyze(tokens)
    #     print("Análise semântica concluída sem erros.")
    # except Exception as e:
    #     print(f"Erro semântico: {e}")


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
