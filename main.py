import sys
import copy
import re
import header

class asmGen():
    def __init__(self):
        self.buffer = header.header
        self.AddLine("")

    def AddLine(self, line):
        self.buffer.append(line)

    def finish(self):
        self.AddLine("")
        self.buffer += header.exiter

class SymbolTable():
    
    def __init__(self):
        self.table = {}
        self.var_count = 0
        self.loop_count = 0

    def get_inc_loop(self):
        loop_count = self.loop_count
        self.loop_count +=1
        return loop_count
    
    def get_inc_var(self):
        self.var_count +=1
        return self.var_count * 4




class Node:
    def __init__(self,value,node_type):
        self.value = value
        self.children = []
        self.type = node_type

    def Evaluate(symboltable, asm):
        pass


class BinOp(Node):
    def Evaluate(self, symboltable, asm):
        self.children[0].Evaluate(symboltable, asm)
        asm.AddLine('PUSH EBX ; O BinOp guarda o resultado na pillha')
        self.children[1].Evaluate(symboltable, asm)

        # if self.type == 'concat':
        #     return str(child0_value) + str(child1_value)

        if self.type == 'equals':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('CMP EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('CALL binop_je ; Chamada da funcao comparacao')

        if self.type == 'plus':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('ADD EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('MOV EBX, EAX ; O BinOp retorna o valor em EBX')

        if self.type == 'minus':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('SUB EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('MOV EBX, EAX ; O BinOp retorna o valor em EBX')

        if self.type == 'mult':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('IMUL EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('MOV EBX, EAX ; O BinOp retorna o valor em EBX')

        if self.type == 'div':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('IDIV EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('MOV EBX, EAX ; O BinOp retorna o valor em EBX')

        if self.type == 'and':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('AND EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('CALL binop_jl ; Chamada da funcao comparacao')

        if self.type == 'or':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('OR EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('CALL binop_jl ; Chamada da funcao comparacao')

        if self.type == 'greater':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('CMP EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('CALL binop_jg ; Chamada da funcao comparacao')

        if self.type == 'less':
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('CMP EAX, EBX ; O BinOp executa a operacao correspondente')
            asm.AddLine('CALL binop_jl ; Chamada da funcao comparacao')




            
class UnOp(Node):
    def Evaluate(self, symboltable, asm):
        if self.type == 'plus':
            self.children[0].Evaluate(symboltable, asm)
            self.children[0].Evaluate(symboltable, asm)
            asm.AddLine('PUSH EBX ; O BinOp guarda o resultado na pillha')
            asm.AddLine('MOV EBX, 0 ; O BinOp guarda o resultado na pillha')
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('ADD EBX, EAX ; O BinOp executa a operacao correspondente')

        elif self.type == 'minus':
            self.children[0].Evaluate(symboltable, asm)
            asm.AddLine('PUSH EBX ; O BinOp guarda o resultado na pillha')
            asm.AddLine('MOV EBX, 0 ; O BinOp guarda o resultado na pillha')
            asm.AddLine('POP EAX ; O BinOp recupera o valor da pilha para EAX')
            asm.AddLine('SUB EBX, EAX ; O BinOp executa a operacao correspondente')
        else:
            self.children[0].Evaluate(symboltable, asm)
            asm.AddLine('NOT EBX ; O BinOp executa a operacao correspondente')

class IntVal(Node):
    def Evaluate(self, symboltable, asm):
        # return self.value
        asm.AddLine('MOV EBX, {0} ; Evaluate do IntVal'.format(self.value))

    
class BoolVal(Node):
    def Evaluate(self, symboltable, asm):
        return self.value

class StringVal(Node):
    def Evaluate(self, symboltable, asm):
        return self.value

class NoOp(Node):
    def Evaluate(self, symboltable, asm):
        pass

class Commands(Node):
    def Evaluate(self, symboltable, asm):
        for child in self.children:
            child.Evaluate(symboltable, asm)

class Program(Node):
    def Evaluate(self, symboltable, asm):
       self.children[0].Evaluate(symboltable, asm)

class Echo(Node):
    def Evaluate(self, symboltable, asm):
        self.children[0].Evaluate(symboltable, asm)
        asm.AddLine('PUSH EBX ; Empilha os argumentos')
        asm.AddLine('CALL print ; Chama a funcao')
        asm.AddLine('POP EBX ; Desempilha os argumentos')


class Assignment(Node):
    def Evaluate(self, symboltable, asm):
        if self.children[0].value not in symboltable.table:
            asm.AddLine('PUSH DWORD 0 ; Alocacao da primeira atribuicao')

            var_address = symboltable.get_inc_var()
            self.children[1].Evaluate(symboltable, asm)
            symboltable.table[self.children[0].value] = (var_address, self.children[1].type)
        else:
            self.children[1].Evaluate(symboltable, asm)
            var_address = symboltable.table[self.children[0].value][0]


        asm.AddLine('MOV [EBP-{0}], EBX ; Resultado da atribuicao'.format(var_address))
    

class Identifier(Node):
    def Evaluate(self, symboltable, asm):
        self.type = symboltable.table[self.value][1] 
        var_address = symboltable.table[self.value][0] 
        asm.AddLine('MOV EBX, [EBP-{0}] ; Evaluate do identifier'.format(var_address))


class While(Node):
    def Evaluate(self, symboltable, asm):
        loop_count = symboltable.get_inc_loop()
        asm.AddLine('LOOP_{0}: ; unique identifier do contador de loops'.format(loop_count))
        self.children[0].Evaluate(symboltable, asm)
        asm.AddLine('CMP EBX, False ; verifica se o teste deu falso'.format(loop_count))
        asm.AddLine('JE EXIT_{0} ; se falso sai do loop'.format(loop_count))
        self.children[1].Evaluate(symboltable, asm)
        asm.AddLine('JMP LOOP_{0} ; volta para testar de novo'.format(loop_count))
        asm.AddLine('EXIT_{0}: ; Label de saída'.format(loop_count))



class If(Node):
    def Evaluate(self, symboltable, asm):
        loop_count = symboltable.get_inc_loop()
        has_else = len(self.children) == 3
        self.children[0].Evaluate(symboltable, asm)
        asm.AddLine('CMP EBX, False ; verifica se o teste deu falso'.format(loop_count))

        if has_else:
            asm.AddLine('JE ELSE_{0} ; se falso vai pro else'.format(loop_count))
        else:
            asm.AddLine('JE EXIT_{0} ; se falso sai do loop'.format(loop_count))


        self.children[1].Evaluate(symboltable, asm)
        asm.AddLine('JMP EXIT_{0} ; sai do if'.format(loop_count))
        if has_else:
            asm.AddLine('ELSE_{0}: ; unique identifier do contador de loops'.format(loop_count))
            self.children[2].Evaluate(symboltable, asm)
        asm.AddLine('EXIT_{0}: ; Label de saída'.format(loop_count))

class Readline(Node):
    def Evaluate(self, symboltable, asm):
        return int(input())

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()


    def get_matches(token):
        matches = 0
        ret_type = None
        for token_type, regex in Tokenizer.get_tokens_regex().items():
            pattern = re.compile(regex[0]) if regex[1] == None else re.compile(regex[0], flags = regex[1])
            if pattern.match(token):
                matches += 1
                ret_type = token_type
        return matches,ret_type

    def get_tokens_reserved():
        tokens_reserved = {}

        tokens_reserved['readline']        = 'readline()'
        tokens_reserved['open_program']    = '<?php'
        tokens_reserved['close_program']   = '?>'
        tokens_reserved['while']           = 'while'
        tokens_reserved['if']              = 'if'
        tokens_reserved['else']            = 'else'
        tokens_reserved['and']             = 'and'
        tokens_reserved['or']              = 'or'
        tokens_reserved['equals']          = '=='
        tokens_reserved['echo']            = 'echo'
        tokens_reserved['readline']        = 'readline()'
        tokens_reserved['true']            = 'true'
        tokens_reserved['false']           = 'false'

        return tokens_reserved



    def get_tokens_regex():
        tokens_regex = {}

        tokens_regex['plus']              = ('^[+]$',None)
        tokens_regex['minus']             = ('^[-]$',None)
        tokens_regex['mult']              = ('^[*]$',None)
        tokens_regex['div']               = ('^[/]$',None)
        tokens_regex['space']             = ('^[ ]+$' ,None)
        tokens_regex['int']               = ('^[0-9]+$',None)
        tokens_regex['open_parentheses']  = ('^[(]$',None)
        tokens_regex['close_parentheses'] = ('^[)]$',None)
        tokens_regex['open_block']        = ('^[{]$',None)
        tokens_regex['close_block']       = ('^[}]$',None)
        tokens_regex['assignment']        = ('^[=]$',None)
        tokens_regex['semi-collon']       = ('^[;]$',None)
        tokens_regex['identifier']        = ('^[$][a-zA-Z][a-zA-Z0-9_]*$',None)
        tokens_regex['string']        = ('^\".*\"$',None)
        tokens_regex['not']        = ('^!$',None)
        tokens_regex['notequals']        = ('^!=$',None)
        tokens_regex['greater']        = ('^>$',None)
        tokens_regex['less']        = ('^<$',None)
        tokens_regex['concat']        = ('^\.$',None)

        return tokens_regex


    def get_token_value(self,tokens_dict):
        token_value = self.origin[self.position]

        token_value = self.origin[self.position]
        while token_value == '\n' and self.position + 1  != len(self.origin):
            self.position += 1
            token_value = self.origin[self.position]
        matches, token_type = Tokenizer.get_matches(token_value)
        
        while matches != 1:
            self.position += 1
            token_value += self.origin[self.position]
            matches, token_type = Tokenizer.get_matches(token_value)

        token_value_aux = token_value

        while matches != 0 and self.position + 1  != len(self.origin):
            token_value = token_value_aux
            self.position += 1
            token_value_aux += self.origin[self.position]
            matches, token_type_dummy = Tokenizer.get_matches(token_value_aux)

        return token_value, token_type

    def get_token_reserved_value(self):
        reserved_tokens = Tokenizer.get_tokens_reserved()

        for token_type, value in reserved_tokens.items():
            word = self.origin[self.position: self.position + len(value)]
            if word.lower() == value:
                self.position += len(value)
                return value, token_type

        return





    def selectNext(self):
        if self.position == len(self.origin):
            next_token = Token('EOF')
            self.actual = next_token
            return

        while self.origin[self.position] == '\n' or self.origin[self.position] == ' ':
            self.position += 1
            
            if self.position == len(self.origin):
                next_token = Token('EOF')
                self.actual = next_token
                return

        position_aux = self.position
        token_return = self.get_token_reserved_value()
        if token_return == None:
            self.position = position_aux
            token_return = self.get_token_value(Tokenizer.get_tokens_regex())

        token_value = token_return[0]
        token_type = token_return[1]

        if token_value.endswith('\n'):
            token_value = token_value.replace('\n','')

        if ' ' in token_value and token_type != 'string':
            self.selectNext()
            return
        
        self.actual = Token(token_type)
        self.actual.value = token_value

        

class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL) ,"" ,code)
        return code

class Parser:
    @staticmethod
    def parseProgram(tokenizer):
        commands = Commands(None,'commands')
        if tokenizer.actual.type == 'open_program':
            tokenizer.selectNext()
            while tokenizer.actual.type != 'close_program':
                commands.children.append(Parser.parseCommand(tokenizer))
                tokenizer.selectNext()

        return commands


    @staticmethod
    def parseBlock(tokenizer):
        node_root = Node(None,'block')
        block_root = Commands(node_root,'block')

        if tokenizer.actual.type == 'open_block':
            tokenizer.selectNext()

            while tokenizer.actual.type != 'close_block':
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
            command = Assignment(None, tokenizer.actual.type)
            identifier = Identifier(tokenizer.actual.value, tokenizer.actual.type)
            command.children.append(identifier)
            tokenizer.selectNext()

            if tokenizer.actual.type == 'assignment':
                tokenizer.selectNext()
                
                command.children.append(Parser.parseRelexpr(tokenizer))
                return command


        elif tokenizer.actual.type == 'echo':
            command = Echo(tokenizer.actual.value, tokenizer.actual.type)
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))
            
            if tokenizer.actual.type != 'semi-collon':
                raise TypeError
            return command


        elif tokenizer.actual.type == 'while':
            command = While(tokenizer.actual.value, tokenizer.actual.type)
            tokenizer.selectNext()

            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()

            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.type != 'close_parentheses':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.type == 'open_block':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.type != 'close_block':
                    raise TypeError
            else:
                command.children.append(Parser.parseBlock(tokenizer))


            return command
            
        elif tokenizer.actual.type == 'if':
            command = If(tokenizer.actual.value,'if')
            tokenizer.selectNext()

            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.type != 'close_parentheses':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.type == 'open_block':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.type != 'close_block':
                    raise TypeError
            else:
                command.children.append(Parser.parseCommand(tokenizer))

            tokenizer_next = copy.copy(tokenizer)
            tokenizer_next.selectNext()
            if tokenizer_next.actual.type == 'else':
                tokenizer.selectNext()
                tokenizer.selectNext()
                if tokenizer.actual.type == 'open_block':
                    command.children.append(Parser.parseBlock(tokenizer))
                    if tokenizer.actual.type != 'close_block':
                        raise TypeError
                else:
                    command.children.append(Parser.parseCommand(tokenizer))
            

            return command
            
        elif tokenizer.actual.type == 'semi-collon':
            pass

        else:
            command = Parser.parseBlock(tokenizer)
            return command

    @staticmethod
    def parseRelexpr(tokenizer):
        node = Parser.parseExpression(tokenizer)
        relexpr_root = node

        
        while tokenizer.actual.type == 'equals' or tokenizer.actual.type == 'greater' or tokenizer.actual.type == 'less' or tokenizer.actual.type == 'notequals':
            if len(relexpr_root.children) == 2:
                relexpr_root_aux = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                relexpr_root_aux.children.append(relexpr_root)
                tokenizer.selectNext()
                relexpr_root_aux.children.append(Parser.parseExpression(tokenizer))
                relexpr_root = relexpr_root_aux
            else:
                relexpr_root = BinOp(tokenizer.actual.value,tokenizer.actual.type)
                relexpr_root.children.append(node)
                tokenizer.selectNext()
                relexpr_root.children.append(Parser.parseExpression(tokenizer))

        return relexpr_root
        
    @staticmethod
    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        root = node

        while tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'or' or tokenizer.actual.type == 'concat':
                if len(root.children) == 2:
                    root_aux = BinOp(tokenizer.actual.value,tokenizer.actual.type)
                    root_aux.children.append(root)
                    tokenizer.selectNext()
                    root_aux.children.append(Parser.parseTerm(tokenizer))
                    root = root_aux
                else:
                    root = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                    root.children.append(node)
                    tokenizer.selectNext()
                    root.children.append(Parser.parseTerm(tokenizer))           
        return root

    @staticmethod
    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        term_root = node
        tokenizer.selectNext()

        
        while tokenizer.actual.type == 'mult' or tokenizer.actual.type == 'div' or tokenizer.actual.type == 'and':
            if len(term_root.children) == 2:
                term_root_aux = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                term_root_aux.children.append(term_root)
                tokenizer.selectNext()
                term_root_aux.children.append(Parser.parseFactor(tokenizer))
                term_root = term_root_aux
            else:
                term_root = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                term_root.children.append(node)
                tokenizer.selectNext()
                term_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return term_root

    @staticmethod
    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            factor_root = IntVal(int(tokenizer.actual.value),tokenizer.actual.type)
            return factor_root
        elif tokenizer.actual.type == 'true' or tokenizer.actual.type == 'false':
            if tokenizer.actual.type == 'true':
                factor_root = BoolVal(True, tokenizer.actual.type)
            else:
                factor_root = BoolVal(False, tokenizer.actual.type)
            return factor_root
        elif tokenizer.actual.type == 'string':
            tokenizer.actual.value = tokenizer.actual.value.replace('"','')
            factor_root = StringVal(str(tokenizer.actual.value),tokenizer.actual.type)
            return factor_root
        
        elif tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'not' or tokenizer.actual.type == 'open_parentheses' or tokenizer.actual.type == 'close_parentheses' or tokenizer.actual.type == 'identifier' or tokenizer.actual.type == 'readline':
            if tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'not':
                factor_root = UnOp(tokenizer.actual.value, tokenizer.actual.type)
                tokenizer.selectNext()
                factor_root.children.append(Parser.parseFactor(tokenizer))

        
            elif tokenizer.actual.type == 'open_parentheses':
                tokenizer.selectNext()
                factor_root = Parser.parseRelexpr(tokenizer)

                if(tokenizer.actual.type != 'close_parentheses'):
                    raise TypeError

            elif tokenizer.actual.type == 'identifier':
                factor_root = Identifier(tokenizer.actual.value, tokenizer.actual.type)

            elif tokenizer.actual.type == 'readline':
                factor_root = Readline(tokenizer.actual.value, tokenizer.actual.type)

            return factor_root
        else:
            raise TypeError

    @staticmethod
    def run(source):
        sourcefile = open(source, 'r') 
        lines = sourcefile.read() 
        sourcefile.close()

        lines = Pre_proc.remove_comments(lines)
        tokenizer = Tokenizer(lines)
        ast = Parser.parseProgram(tokenizer)
        symboltable = SymbolTable()
        asm = asmGen()
        ast.Evaluate(symboltable,asm)
        asm.finish()

        for buf in asm.buffer:
            print(buf)
        

def main():
    source = sys.argv[1]
    Parser.run(source)


if __name__== "__main__":
  main()
