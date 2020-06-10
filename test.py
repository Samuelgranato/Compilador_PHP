#by samuelvgb

import unittest
import main
from io import StringIO 
import sys
import os
test_fileName = 'testfile.temp'

def create_tempTestfile():
    f = open(test_fileName, "w")
    f.close()

def write_testFile(source):
    f = open(test_fileName, "w")
    f.write(source)
    f.close()

class TestSum(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        sys.argv.append(test_fileName)
        create_tempTestfile()

    def tearDown(self):
        os.remove(test_fileName)

    def test_1(self):
        source= '''<?php
    $i = 2;
    $n = 5;
    $f = 1;
    $g = 0;

    if($i < $n + 1){
        echo $f;

    }else{
        echo $f;
    }

    $i = 2;
    $n = 5;
    $f = 1;

    while($i < $n + 1){
        $f = $f * $i;
        $i = $i + 1;
    }
    
    echo $f;
?>'''
        write_testFile(source)
        expected = '''; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment .data
segment .bss  ; variaveis
res RESB 1
section .text
global _start
print:  ; subrotina print
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer
MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
XOR ESI, ESI
print_dec: ; empilha todos os digitos
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0'
PUSH EDX
INC ESI ; contador de digitos
CMP EAX, 0
JZ print_next ; quando acabar pula
JMP print_dec
print_next:
CMP ESI, 0
JZ print_exit ; quando acabar de imprimir
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res], ECX
MOV ECX, res
MOV EDX, 1
INT 0x80
JMP print_next
print_exit:
POP EBP
RET
; subrotinas if/while
binop_je:
JE binop_true
JMP binop_false
binop_jg:
JG binop_true
JMP binop_false
binop_jl:
JL binop_true
JMP binop_false
binop_false:
MOV EBX, False
JMP binop_exit
binop_true:
MOV EBX, True
binop_exit:
RET
_start:
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer
; codigo gerado pelo compilador

PUSH DWORD 0 ; Alocacao da primeira atribuicao
MOV EBX, 2 ; Evaluate do IntVal
MOV [EBP-4], EBX ; Resultado da atribuicao
PUSH DWORD 0 ; Alocacao da primeira atribuicao
MOV EBX, 5 ; Evaluate do IntVal
MOV [EBP-8], EBX ; Resultado da atribuicao
PUSH DWORD 0 ; Alocacao da primeira atribuicao
MOV EBX, 1 ; Evaluate do IntVal
MOV [EBP-12], EBX ; Resultado da atribuicao
PUSH DWORD 0 ; Alocacao da primeira atribuicao
MOV EBX, 0 ; Evaluate do IntVal
MOV [EBP-16], EBX ; Resultado da atribuicao
MOV EBX, [EBP-4] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, [EBP-8] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, 1 ; Evaluate do IntVal
POP EAX ; O BinOp recupera o valor da pilha para EAX
ADD EAX, EBX ; O BinOp executa a operacao correspondente
MOV EBX, EAX ; O BinOp retorna o valor em EBX
POP EAX ; O BinOp recupera o valor da pilha para EAX
CMP EAX, EBX ; O BinOp executa a operacao correspondente
CALL binop_jl ; Chamada da funcao comparacao
CMP EBX, False ; verifica se o teste deu falso
JE ELSE_0 ; se falso vai pro else
MOV EBX, [EBP-12] ; Evaluate do identifier
PUSH EBX ; Empilha os argumentos
CALL print ; Chama a funcao
POP EBX ; Desempilha os argumentos
JMP EXIT_0 ; sai do if
ELSE_0: ; unique identifier do contador de loops
MOV EBX, [EBP-12] ; Evaluate do identifier
PUSH EBX ; Empilha os argumentos
CALL print ; Chama a funcao
POP EBX ; Desempilha os argumentos
EXIT_0: ; Label de saída
MOV EBX, 2 ; Evaluate do IntVal
MOV [EBP-4], EBX ; Resultado da atribuicao
MOV EBX, 5 ; Evaluate do IntVal
MOV [EBP-8], EBX ; Resultado da atribuicao
MOV EBX, 1 ; Evaluate do IntVal
MOV [EBP-12], EBX ; Resultado da atribuicao
LOOP_1: ; unique identifier do contador de loops
MOV EBX, [EBP-4] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, [EBP-8] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, 1 ; Evaluate do IntVal
POP EAX ; O BinOp recupera o valor da pilha para EAX
ADD EAX, EBX ; O BinOp executa a operacao correspondente
MOV EBX, EAX ; O BinOp retorna o valor em EBX
POP EAX ; O BinOp recupera o valor da pilha para EAX
CMP EAX, EBX ; O BinOp executa a operacao correspondente
CALL binop_jl ; Chamada da funcao comparacao
CMP EBX, False ; verifica se o teste deu falso
JE EXIT_1 ; se falso sai do loop
MOV EBX, [EBP-12] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, [EBP-4] ; Evaluate do identifier
POP EAX ; O BinOp recupera o valor da pilha para EAX
IMUL EBX ; O BinOp executa a operacao correspondente
MOV EBX, EAX ; O BinOp retorna o valor em EBX
MOV [EBP-12], EBX ; Resultado da atribuicao
MOV EBX, [EBP-4] ; Evaluate do identifier
PUSH EBX ; O BinOp guarda o resultado na pillha
MOV EBX, 1 ; Evaluate do IntVal
POP EAX ; O BinOp recupera o valor da pilha para EAX
ADD EAX, EBX ; O BinOp executa a operacao correspondente
MOV EBX, EAX ; O BinOp retorna o valor em EBX
MOV [EBP-4], EBX ; Resultado da atribuicao
JMP LOOP_1 ; volta para testar de novo
EXIT_1: ; Label de saída
MOV EBX, [EBP-12] ; Evaluate do identifier
PUSH EBX ; Empilha os argumentos
CALL print ; Chama a funcao
POP EBX ; Desempilha os argumentos

; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
'''
        main.main()
        
        sourcefile = open("program.asm", 'r') 
        lines = sourcefile.read() 
        sourcefile.close()

        print(lines)
        self.assertEqual(lines, expected, "Should be {0}".format(expected))

if __name__ == '__main__':
    unittest.main()