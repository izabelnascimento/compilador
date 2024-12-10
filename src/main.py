from src.compiler import Compiler


def main():
    compiler = Compiler()
    for i in range(1, 11):
        file_path = f'../resources/test_lexer/code{i}_1.txt'
        compiler.compile(file_path)
        file_path = f'../resources/test_lexer/code{i}_2.txt'
        compiler.compile(file_path)


if __name__ == "__main__":
    main()
