from src.compiler import Compiler


def main():
    folder = 'test_syntax'
    file_name = f'code1_1.txt'
    Compiler.compile(folder, file_name)

    # for i in range(2, 3):
    #     file_name = f'code{i}_1.txt'
    #     Compiler.compile(folder, file_name)
    #     file_name = f'code{i}_2.txt'
    #     Compiler.compile(folder, file_name)


if __name__ == "__main__":
    main()