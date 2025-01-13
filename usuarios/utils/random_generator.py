import random


class CodeGenerator:
    def __init__(self, code_longitude = 4):
        self.code_longitude = code_longitude
        self.code = ""

    def generate_code(self):
        code = [random.randint(0, 9) for _ in range(4)]
        random.shuffle(code)

        self.code = "".join((str(char) for char in code))

        return self.code

combination = CodeGenerator()
