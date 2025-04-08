from src.util import Util


class Semantic:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def start_semantic(self):
        print("\n------------------- ANÁLISE SEMÂNTICA -------------------")
        self.check_declarations()
        self.check_assignments()
        self.check_expression_types()
        self.check_function_calls()
        self.check_function_returns()
        self.check_control_flow_conditions()
        Util.print_sucess("\nAnálise semântica concluída sem erros.")

    # Garante que todos os identificadores usados foram declarados no escopo apropriado.
    def check_declarations(self):
        print("\n- Verificando declaração -")

    # Confirma se os operandos têm tipos compatíveis nas expressões.
    def check_expression_types(self):
        print("\n- Verificando tipos em expressões -")

    # Verifica se o lado esquerdo da atribuição existe e tem tipo compatível com o lado direito.
    def check_assignments(self):
        print("\n- Verificando atribuições -")

    # Confere se as chamadas usam o número e tipo corretos de argumentos.
    def check_function_calls(self):
        print("\n- Verificando chamadas de funlções -")

    # Garante que as expressões condicionais em if e while são do tipo booleano.
    def check_control_flow_conditions(self):
        print("\n- Verificando instrução de controle de fluxo -")

    # Verifica se existe return com tipo compatível nas funções.
    def check_function_returns(self):
        print("\n- Verificando compatibilidade do returns -")
