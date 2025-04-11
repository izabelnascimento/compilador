from src.compiler import Compiler


def execute_one(folder, file_name):
    Compiler.compile(folder, file_name)


def execute_all_folder(folder, n):
    for i in range(1, n):
        file_name = f'code{i}_1'
        Compiler.compile(folder, file_name)
        if folder != 'test_lexer':
            file_name = f'code{i}_2'
            Compiler.compile(folder, file_name)


def execute_all():
    execute_all_folder('test_lexer', 11)
    execute_all_folder('test_syntax', 6)
    execute_all_folder('test_semantic', 5)
    execute_all_folder('test_tac_generator', 5)


def main():
    folder = 'test_semantic'
    # folder = 'test_tac_generator'
    execute_one(folder, f'code2_1')
    # execute_all_folder(folder, 5)
    # execute_all()


if __name__ == "__main__":
    main()
