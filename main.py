from lexer import Lexer
from semantic import SemanticAnalyzer


def main():
    code = """
    x = 5
    y = x + 2
    """
    lexer = Lexer()
    tokens = list(lexer.tokenize(code))

    print("Tokens:", tokens)

    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.analyze(tokens)
        print("Análise semântica concluída sem erros.")
    except Exception as e:
        print(f"Erro semântico: {e}")


if __name__ == "__main__":
    main()
