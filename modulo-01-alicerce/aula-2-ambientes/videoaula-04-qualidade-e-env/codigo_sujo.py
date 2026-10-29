"""
VIDEOAULA 4 — Código propositalmente "sujo".

NÃO corrija à mão: deixe o `ruff` e o `black` fazerem o trabalho ao vivo.
"""
import os, sys
import json


def  calcular_prioridade( titulo,urgente ):
    if urgente == True:
        return 'alta'
    if titulo == None:
        return 'baixa'
    resultado = {'titulo':titulo,'prioridade':'media'}
    return resultado

class chamado:
    def __init__(self,titulo,descricao):
        self.titulo=titulo
        self.descricao=descricao
    def resumo(self):
        return self.titulo+' - '+self.descricao
