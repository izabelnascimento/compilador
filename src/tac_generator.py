from src.util import Util


class TACGenerator:
    def __init__(self, tokens, symbol_table, folder, file_name):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.folder = folder
        self.file_name = file_name
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self):
        print("\n------------------- TRADUÇÃO CÓDIGO DE 3 ENDEREÇOS -------------------")
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            token_type = token[1]

            if token_type == "IDENTIFIER" and self._is_assignment(i):
                i = self._handle_assignment(i)
            elif token_type == "SHOW":
                i = self._handle_show(i)
            elif token_type == "IF":
                i = self._handle_if(i)
            else:
                i += 1

        for line in self.code:
            print(line)
        Util.save_three_address_code(self.folder, self.file_name, self.code)
        Util.print_sucess("\nGeração de código de 3 endereços concluída com sucesso.")

    def _is_assignment(self, i):
        return i + 1 < len(self.tokens) and self.tokens[i + 1][1] == "ASSIGN"

    def _handle_assignment(self, i):
        var_name = self.tokens[i][2]
        value_token = self.tokens[i + 2]

        if value_token[1] in ("NUMBER", "TRUE", "FALSE"):
            self.code.append(f"{var_name} = {value_token[2]}")
            return i + 4  # pula até o ;

        if value_token[1] == "CALL":
            return self._handle_function_call_assignment(i, var_name)

        return self._handle_expression_assignment(i, var_name)

    def _handle_function_call_assignment(self, i, var_name):
        func_name = self.tokens[i + 3][2]
        j = i + 4  # após CALL e IDENTIFIER
        args = []

        while self.tokens[j][1] != "RPAREN":
            if self.tokens[j][1] in ("NUMBER", "IDENTIFIER", "TRUE", "FALSE"):
                args.append(self.tokens[j][2])
            j += 1

        call_temp = self.new_temp()
        self.code.append(f"{call_temp} = call {func_name}({', '.join(args)})")
        self.code.append(f"{var_name} = {call_temp}")
        return j + 2  # pula RPAREN e SEMICOLON

    def _handle_expression_assignment(self, i, var_name):
        expr_tokens = []
        j = i + 2
        while j < len(self.tokens) and self.tokens[j][1] != "SEMICOLON":
            expr_tokens.append(self.tokens[j])
            j += 1

        if not expr_tokens:
            raise SyntaxError(f"[Erro] Expressão inválida ou vazia após atribuição em {self.tokens[i][3]}")

        expr_code, result = self.handle_expression(expr_tokens)
        self.code.extend(expr_code)
        self.code.append(f"{var_name} = {result}")
        return j + 1

    def _handle_show(self, i):
        if (i + 4 < len(self.tokens)
                and self.tokens[i + 1][1] == "LPAREN"
                and self.tokens[i + 2][1] == "IDENTIFIER"
                and self.tokens[i + 3][1] == "RPAREN"):
            var_name = self.tokens[i + 2][2]
            self.code.append(f"print {var_name}")
            return i + 5
        return i + 1

    def _handle_if(self, i):
        if self.tokens[i + 1][1] != "LPAREN":
            return i + 1

        cond_tokens = []
        j = i + 2
        while self.tokens[j][1] != "RPAREN":
            cond_tokens.append(self.tokens[j])
            j += 1

        cond_code, cond_expr = self.handle_condition(cond_tokens)
        self.code.extend(cond_code)

        label_true = f"L{self.temp_count + 1}"
        label_end = f"L{self.temp_count + 2}"
        self.code.append(f"if {cond_expr} goto {label_true}")
        j += 1

        if self.tokens[j][1] == "THEN":
            j += 1

        assign_false = self._collect_assignments(j, until=("ELSE", "ENDIF"))
        j += len(assign_false) * 4

        if self.tokens[j][1] == "ELSE":
            self.code.extend(assign_false)
            self.code.append(f"goto {label_end}")
            self.code.append(f"{label_true}:")
            j += 1

            assign_true = self._collect_assignments(j, until=("END",))
            self.code.extend(assign_true)
            self.code.append(f"{label_end}:")
            return j + len(assign_true) * 4 + 1
        else:
            self.code.append(f"{label_true}:")
            self.code.extend(assign_false)
            return j + 1

    def _collect_assignments(self, start_idx, until):
        assignments = []
        j = start_idx
        while self.tokens[j][1] not in until:
            if (self.tokens[j][1] == "IDENTIFIER"
                    and self.tokens[j + 1][1] == "ASSIGN"):
                var = self.tokens[j][2]
                val = self.tokens[j + 2][2]
                assignments.append(f"{var} = {val}")
                j += 4
            else:
                j += 1
        return assignments

    def handle_expression(self, expr_tokens):
        ops_stack, vals_stack, code = [], [], []
        precedence = {"*": 2, "/": 2, "+": 1, "-": 1}

        def apply_op():
            right = vals_stack.pop()
            left = vals_stack.pop()
            op = ops_stack.pop()
            temp = self.new_temp()
            code.append(f"{temp} = {left} {op} {right}")
            vals_stack.append(temp)

        for token in expr_tokens:
            if token[1] in ("IDENTIFIER", "NUMBER", "TRUE", "FALSE"):
                vals_stack.append("1" if token[1] == "TRUE" else "0" if token[1] == "FALSE" else token[2])
            elif token[1] in ("PLUS", "MINUS", "MULTIPLY", "DIVIDE"):
                op = token[2]
                while ops_stack and precedence[op] <= precedence.get(ops_stack[-1], 0):
                    apply_op()
                ops_stack.append(op)

        while ops_stack:
            apply_op()

        return code, vals_stack[-1]

    def handle_condition(self, cond_tokens):
        code = []
        if len(cond_tokens) == 3:
            left, op, right = cond_tokens[0][2], cond_tokens[1][2], cond_tokens[2][2]
            temp = self.new_temp()
            code.append(f"{temp} = {left} {op} {right}")
            return code, f"{left} {op} {right}"
        return code, ""
