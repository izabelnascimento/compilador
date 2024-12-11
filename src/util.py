import csv
import sys


class Util:

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

    @staticmethod
    def save_tokens_to_csv(tokens, folder, file_name):
        with open(f'../resources/out/{folder}/{file_name}_tokens.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Token', 'Lexema', 'Line'])  # Cabeçalho
            for token_type, token_value, token_line in tokens:
                writer.writerow([token_type, token_value, token_line])
        print("Tokens salvos em 'tokens.csv'.")

    @staticmethod
    def save_symbol_table_to_csv(symbol_table, folder, file_name):
        with open(f'../resources/out/{folder}/{file_name}_symbol_table.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Type', 'Line'])  # Cabeçalho
            for symbol in symbol_table:
                writer.writerow([symbol.id, symbol.kind, symbol.line])
        print("Tabela de símbolos salva em 'symbol_table.csv'.")
