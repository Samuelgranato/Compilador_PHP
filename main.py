import sys

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()

    def get_type(character):
        if character == '+':
            return 'plus'
        if character == '-':
            return 'minus'
        if character == '*':
            return 'mult'
        if character == '-/':
            return 'div'
        if character == ' ':
            return 'space'
        if character.isdigit():
            return 'int'

    def selectNext(self):
        if self.position == len(self.origin):
            next_token = Token('EOF')
            self.actual = next_token
            return

        current_char = self.origin[self.position]
        while(current_char == ' '):
            self.position += 1
            if self.position == len(self.origin):
                next_token = Token('EOF')
                self.actual = next_token
                return

            current_char = self.origin[self.position]
            
        next_token = Token(Tokenizer.get_type(current_char))
        while Tokenizer.get_type(current_char) == next_token.type:
            next_token.value += self.origin[self.position]
            self.position += 1

            if self.position == len(self.origin):
                self.actual = next_token
                return

            current_char = self.origin[self.position]

        self.actual = next_token




class Parser:
    @staticmethod
    def parseExpression(tokenizer):
        if tokenizer.actual.type == 'int':
            resultado = int(tokenizer.actual.value)
            tokenizer.selectNext()

            while tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '*' or tokenizer.actual.value == '/':
                if tokenizer.actual.value == '+':
                    tokenizer.selectNext()
                    if tokenizer.actual.type == 'int':
                        resultado += int(tokenizer.actual.value)
                    else:
                        raise TypeError
                if tokenizer.actual.value == '-':
                    tokenizer.selectNext()
                    if tokenizer.actual.type == 'int':
                        resultado -= int(tokenizer.actual.value)
                    else:
                        raise TypeError
                if tokenizer.actual.value == '*':
                    tokenizer.selectNext()
                    if tokenizer.actual.type == 'int':
                        resultado *= int(tokenizer.actual.value)
                    else:
                        raise TypeError
                if tokenizer.actual.value == '/':
                    tokenizer.selectNext()
                    if tokenizer.actual.type == 'int':
                        resultado /= int(tokenizer.actual.value)
                    else:
                        raise TypeError
                tokenizer.selectNext()
            if(tokenizer.actual.type != 'EOF'):
                raise TypeError
            return resultado
        else:
            raise TypeError

    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code)
        return Parser.parseExpression(tokenizer)

def main():
    source = sys.argv[1]
    # source = '   111 1   + 23'
    print(Parser.run(source))


if __name__== "__main__":
  main()
