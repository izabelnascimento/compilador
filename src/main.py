from src.compiler import Compiler


def execute_one(folder, file_name):
    Compiler.compile(folder, file_name)


def execute_all_folder(folder, n):
    for i in range(1, n):
        file_name = f'code{i}_1'
        Compiler.compile(folder, file_name)
        file_name = f'code{i}_2'
        Compiler.compile(folder, file_name)


def execute_all():
    execute_all_folder('test_lexer', 11)
    execute_all_folder('test_syntax', 6)


def main():
    folder = 'test_syntax'
    # execute_one(folder, f'code1_1')
    # execute_all_folder(folder)
    execute_all()


if __name__ == "__main__":
    main()
