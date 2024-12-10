from src.compiler import Compiler


def main():
    compiler = Compiler()
    for i in range(1, 11):
        file_path = f'../resources/code{i}.txt'  #Nos exemplos do 1 a 4 são acertos, do 5 ao 10 são erros, mas t´não tá se comportando assim. Precisa ser revisto
        compiler.compile(file_path)


if __name__ == "__main__":
    main()
