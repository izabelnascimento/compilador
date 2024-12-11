from src.compiler import Compiler


def main():
    compiler = Compiler()
    for i in range(1, 11):
        file_name = f'code{i}_1.txt'
        compiler.compile(file_name)
        file_name = f'code{i}_2.txt'
        compiler.compile(file_name)


if __name__ == "__main__":
    main()
