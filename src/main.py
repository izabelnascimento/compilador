from src.compiler import Compiler


def main():
    file_name = f'code1_1.txt'
    Compiler.compile(file_name)

    # for i in range(1, 11):
    #     file_name = f'code{i}_1.txt'
    #     Compiler.compile(file_name)
    #     file_name = f'code{i}_2.txt'
    #     Compiler.compile(file_name)


if __name__ == "__main__":
    main()