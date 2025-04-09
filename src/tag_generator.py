from src.util import Util


class TACGenerator:
    def __init__(self, tokens, symbol_table, folder, file_name):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.folder = folder
        self.file_name = file_name
        self.code = []
        self.temp_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate(self):
        print("\n------------------- TRADUÇÃO CÓDIGO DE 3 ENDEREÇOS -------------------")
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            # Detecta: IDENTIFIER => (ASSIGN) => valor ou expressão
            if token[1] == "IDENTIFIER" and i+1 < len(self.tokens) and self.tokens[i+1][1] == "ASSIGN":
                var_name = token[2]
                assign_op = self.tokens[i+1]
                value_token = self.tokens[i+2]

                # Expressão simples? (como x => 5;)
                if value_token[1] == "NUMBER":
                    self.code.append(f"{var_name} = {value_token[2]}")
                    i += 4  # pula até depois do ;

                else:
                    # Expressão complexa (ex: z => x + y * w)
                    expr_tokens = []
                    j = i + 2
                    while self.tokens[j][1] != "SEMICOLON":
                        expr_tokens.append(self.tokens[j])
                        j += 1
                    expr_code, result = self.handle_expression(expr_tokens)
                    self.code.extend(expr_code)
                    self.code.append(f"{var_name} = {result}")
                    i = j + 1  # pula até depois do ;
            else:
                i += 1
        for line in self.code:
            print(line)
        Util.save_three_address_code(self.folder, self.file_name, self.code)
        Util.print_sucess("\nGeração de código de 3 endereços concluída com sucesso.")

    def handle_expression(self, expr_tokens):
        """
        Recebe tokens da expressão (ex: x + y * w)
        Gera código de 3 endereços com precedência
        Retorna lista de linhas de código e o resultado final (ex: t2)
        """
        ops_stack = []
        vals_stack = []
        code = []

        precedence = {"*": 2, "/": 2, "+": 1, "-": 1}

        def apply_op():
            right = vals_stack.pop()
            left = vals_stack.pop()
            op = ops_stack.pop()
            temp = self.new_temp()
            code.append(f"{temp} = {left} {op} {right}")
            vals_stack.append(temp)

        i = 0
        while i < len(expr_tokens):
            token = expr_tokens[i]
            if token[1] in ("IDENTIFIER", "NUMBER"):
                vals_stack.append(token[2])
            elif token[1] in ("PLUS", "MINUS", "MULTIPLY", "DIVIDE"):
                op = token[2]
                while (ops_stack and
                       precedence[op] <= precedence.get(ops_stack[-1], 0)):
                    apply_op()
                ops_stack.append(op)
            i += 1

        while ops_stack:
            apply_op()

        return code[-(len(vals_stack) - 1):], vals_stack[-1]

    def handle_condition(self, cond_tokens):
        code = []
        if len(cond_tokens) == 3:
            left = cond_tokens[0][2]
            op = cond_tokens[1][2]
            right = cond_tokens[2][2]
            temp = self.new_temp()
            code.append(f"{temp} = {left} {op} {right}")
            return code, f"{left} {op} {right}"  # pode usar direto sem temp, se preferir
        return code, ""