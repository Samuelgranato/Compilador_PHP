import sys
import copy
import re

class Node:
    # value = 0

    def __init__(self,value):
        self.value = value
        self.children = []


    def Evaluate():
        pass


class BinOp(Node):
    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        
        if self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()

        if self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()

        if self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()



class UnOp(Node):
    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate()
        else:
            return -self.children[0].Evaluate()

class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def Evaluate(self):
        pass

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
        if character == '/':
            return 'div'
        if character == ' ':
            return 'space'
        if character.isdigit():
            return 'int'
        if character == '(':
            return 'open_parentheses'
        if character == ')':
            return 'close_parentheses'
        raise TypeError

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

            if self.position == len(self.origin) or Tokenizer.get_type(self.origin[self.position]) != 'int':
                self.actual = next_token
                return

            current_char = self.origin[self.position]


        self.actual = next_token


class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL) ,"" ,code)
        return code

class Parser:
    @staticmethod
    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        root = node

        while tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
                if len(root.children) == 2:
                    root_aux = BinOp(tokenizer.actual.value)
                    root_aux.children.append(root)
                    tokenizer.selectNext()
                    root_aux.children.append(Parser.parseTerm(tokenizer))
                    root = root_aux
                else:
                    root = BinOp(tokenizer.actual.value)
                    root.children.append(node)
                    tokenizer.selectNext()
                    root.children.append(Parser.parseTerm(tokenizer))           
        return root

    @staticmethod
    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        term_root = node
        tokenizer.selectNext()

        
        while tokenizer.actual.value == '*' or tokenizer.actual.value == '/':
            if len(term_root.children) == 2:
                term_root_aux = BinOp(tokenizer.actual.value)
                term_root_aux.children.append(term_root)
                tokenizer.selectNext()
                term_root_aux.children.append(Parser.parseFactor(tokenizer))
                term_root = term_root_aux
            else:
                term_root = BinOp(tokenizer.actual.value)
                term_root.children.append(node)
                tokenizer.selectNext()
                term_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return term_root



    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            factor_root = IntVal(int(tokenizer.actual.value))
            return factor_root
        
        elif tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '(' or tokenizer.actual.value == ')':
            if tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
                factor_root = UnOp(tokenizer.actual.value)
                tokenizer.selectNext()
                factor_root.children.append(Parser.parseFactor(tokenizer))

        
            elif tokenizer.actual.value == '(':
                tokenizer.selectNext()
                factor_root = Parser.parseExpression(tokenizer)
                # new_node.children.append(Parser.parseFactor(tokenizer))
                # tokenizer.selectNext()
                # resultado += Parser.parseExpression(tokenizer)

                if(tokenizer.actual.value != ')'):
                    raise TypeError

            return factor_root
        else:
            raise TypeError


    @staticmethod
    def run(code):
        code = Pre_proc.remove_comments(code)
        tokenizer = Tokenizer(code)
        parse_result = Parser.parseExpression(tokenizer)
        if tokenizer.actual.type != 'EOF':
            raise TypeError

        result = parse_result.Evaluate()


        return result

def main():
    source = sys.argv[1]
    # source = '   1   -  3    0   '
    print(Parser.run(source))


if __name__== "__main__":
  main()
