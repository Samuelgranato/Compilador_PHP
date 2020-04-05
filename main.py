import sys
import copy
import re


class SymbolTable():
    
    def __init__(self):
        self.table = {}


class Node:
    def __init__(self,value):
        self.value = value
        self.children = []

    def Evaluate(symboltable):
        pass


class BinOp(Node):
    def Evaluate(self,symboltable):
        if self.value == '+':
            return self.children[0].Evaluate(symboltable) + self.children[1].Evaluate(symboltable)
        
        if self.value == '-':
            return self.children[0].Evaluate(symboltable) - self.children[1].Evaluate(symboltable)

        if self.value == '*':
            return self.children[0].Evaluate(symboltable) * self.children[1].Evaluate(symboltable)

        if self.value == '/':
            return self.children[0].Evaluate(symboltable) // self.children[1].Evaluate(symboltable)



class UnOp(Node):
    def Evaluate(self,symboltable):
        if self.value == '+':
            return self.children[0].Evaluate(symboltable)
        else:
            return -self.children[0].Evaluate(symboltable)

class IntVal(Node):
    def Evaluate(self,symboltable):
        return self.value

class NoOp(Node):
    def Evaluate(self,symboltable):
        pass

class Commands(Node):
    def Evaluate(self,symboltable):
        for child in self.children:
            child.Evaluate(symboltable)

class Echo(Node):
    def Evaluate(self,symboltable):
        print(self.children[0].Evaluate(symboltable))

class Assignment(Node):
    def Evaluate(self,symboltable):
        value = self.children[1].Evaluate(symboltable)
        symboltable.table[self.children[0].value] = value

class Identifier(Node):
    def Evaluate(self,symboltable):
        return symboltable.table[self.value]

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()

    def get_special_type(special):
        if special[0] == '$':
            pattern = re.compile("[$][a-zA-Z][a-zA-Z0-9_]*")
            if pattern.match(special):
                return 'identifier'
            else:
                raise TypeError
        if special == 'echo':
            return 'echo'

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
        if character == '{':
            return 'open_block'
        if character == '}':
            return 'close_block'
        if character == '=':
            return 'assignment'
        if character == ';':
            return 'semi-collon'
        else:
            return 'special'


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

        if next_token.type != 'special':
            while Tokenizer.get_type(current_char) == next_token.type:
                next_token.value += self.origin[self.position]
                self.position += 1

                if self.position == len(self.origin) or (Tokenizer.get_type(self.origin[self.position]) != 'int' and Tokenizer.get_type(self.origin[self.position]) != 'function'):
                    self.actual = next_token
                    return

                current_char = self.origin[self.position]


            self.actual = next_token

        else:
            while Tokenizer.get_type(current_char) != 'space':
                next_token.value += self.origin[self.position]
                self.position += 1

                if self.position == len(self.origin) or (Tokenizer.get_type(self.origin[self.position]) != 'int' and Tokenizer.get_type(self.origin[self.position]) != 'special'):
                    self.actual = next_token
                    if next_token.value == '\n':
                        self.selectNext()
                        return
                    self.actual.type = Tokenizer.get_special_type(self.actual.value)
                    return

                current_char = self.origin[self.position]



            if next_token.value == '\n':
                self.selectNext()
                return
            self.actual = next_token
            self.actual.type = Tokenizer.get_special_type(self.actual.value)


class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL) ,"" ,code)
        return code

class Parser:
    @staticmethod
    def parseBlock(tokenizer):
        node_root = Node(None)
        block_root = Commands(node_root)

        if tokenizer.actual.value == '{':
            tokenizer.selectNext()

            while tokenizer.actual.value != '}':
                command = Parser.parseCommand(tokenizer)
                if command != None:
                    block_root.children.append(command)
                tokenizer.selectNext()

        else:
            raise TypeError

        return block_root


    @staticmethod
    def parseCommand(tokenizer):
        if tokenizer.actual.type == 'identifier':
            command = Assignment(None)
            identifier = Identifier(tokenizer.actual.value)
            command.children.append(identifier)
            tokenizer.selectNext()

            if tokenizer.actual.value == '=':
                tokenizer.selectNext()
                
                command.children.append(Parser.parseExpression(tokenizer))
                return command
        elif tokenizer.actual.value == 'echo':
            command = Echo(tokenizer.actual.value)
            tokenizer.selectNext()
            command.children.append(Parser.parseExpression(tokenizer))
            return command

        elif tokenizer.actual.value == ';':
            pass

        else:
            command = Parser.parseBlock(tokenizer)
            return command

        
        
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

    @staticmethod
    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            factor_root = IntVal(int(tokenizer.actual.value))
            return factor_root
        
        elif tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '(' or tokenizer.actual.value == ')' or tokenizer.actual.type == 'identifier':
            if tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
                factor_root = UnOp(tokenizer.actual.value)
                tokenizer.selectNext()
                factor_root.children.append(Parser.parseFactor(tokenizer))

        
            elif tokenizer.actual.value == '(':
                tokenizer.selectNext()
                factor_root = Parser.parseExpression(tokenizer)

                if(tokenizer.actual.value != ')'):
                    raise TypeError

            elif tokenizer.actual.type == 'identifier':
                factor_root = Identifier(tokenizer.actual.value)

            return factor_root
        else:
            raise TypeError

    @staticmethod
    def run(source):
        sourcefile = open(source, 'r') 
        lines = sourcefile.read() 

        # line = Pre_proc.remove_comments(line.strip())
        tokenizer = Tokenizer(lines)
        ast = Parser.parseBlock(tokenizer)
        symboltable = SymbolTable()
        ast.Evaluate(symboltable)
        

def main():
    # source = sys.argv[1]
    source = 'input.php'
    Parser.run(source)


if __name__== "__main__":
  main()
