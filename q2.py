from typing import Any
from random import randint


def busca_linear(lista, elemento) -> Any:
  for i in range(0, len(lista)):
    if lista[i] == elemento:
      return i
  return -1

def insertionSort(lista): #implementação de um insertion sort
    listaInicial = lista
    for i in range(1, len(lista)):
        if type(lista[i]) == str or type(lista[i-1]) == str:
            return listaInicial # para o código n quebrar caso aja arrays com tipos diferentes
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


def busca_ordenada(lista, elemento, ordenacao) -> Any: #adcionei um parametro
    if type(ordenacao) != bool:
        return 'Use ordenação como True(se já estiver ordenado) ou False(caso não esteja ordenado)'
    listaI = lista
    if ordenacao == False: #só ordena a lista caso ela não esteja ordenada
        lista = insertionSort(lista)

    if lista == -1: #caso seja tenha que a str na lista a função chama a busca linear
        return busca_linear(listaI, elemento) # não faz sentido ordenar strings

    comeco = 0
    fim = len(lista) - 1
    while comeco <= fim:
        meio = (comeco + fim) // 2 #implementação da busca binária

        if type(lista[meio]) == str or type(elemento) == str: # para não quabrar com listas variadas
            return busca_linear(listaI, elemento)

        if lista[meio] == elemento:
            return meio
        elif lista[meio] < elemento:
            comeco = meio + 1
        else:
            fim = meio - 1
    return -1

def busca_saltos(lista, elemento, saltos, ordenacao) -> Any:
    if type(ordenacao) != bool:
        return 'Use ordenação como True(se já estiver ordenado) ou False(caso não esteja ordenado)'
    listaI = lista
    if ordenacao == False: #mesma lógica da busca ordenada
        lista = insertionSort(lista)

    if lista == -1:
        return busca_linear(listaI, elemento)

    tamPulo = saltos
    id = 0 # index da busca

    while True:
        if type(lista[id]) == str or type(elemento) == str: # para não quabrar
            return busca_linear(listaI, elemento)          #com listas variadas

        if lista[id] > elemento: #saí do while quando o encontrar um numero
            break                #maior for maior q o elemento

        if tamPulo + id < len(lista) - 1:
            id += tamPulo
        else:
            id = len(lista) - 1

    for i in range(id, id-tamPulo, -1): #checa voltando o intervalo em que o
        if lista[i] == elemento:        #número está
            return i
    return -1

def busca_hybrid(lista, elemento, ordenacao) -> Any:
    if type(ordenacao) != bool:
        return 'Use ordenação como True(se já estiver ordenado) ou False(caso não esteja ordenado)'

    if ordenacao == False: #se o array não está ordenado então é melhor buscar
        return busca_linear(lista, elemento) # do que ordenar antes

    elif len(lista) > 16: # momento em que a busca binária fica mais eficiente
        return busca_ordenada(lista, elemento, ordenacao) # do que a de saltos

    else:
        return busca_saltos(lista, elemento, (len(lista)**(1/2)), ordenacao)

#testes

lista = []
elemento = 'banana'

print(busca_linear(lista, elemento))

lista = ['apple', 'banana', 'cherry']
elemento = 'banana'
lista1 = [55, 30, 23, 12, 5, 67, 199]
elemento1 = 67

print(busca_ordenada(lista, elemento, True))
print(busca_ordenada(lista1, elemento1, False))

lista = ['apple', 1, 'banana', 77, 99, 'cherry']
elemento = 'banana'
lista1 = [55, 30, 23, 12, 5, 67, 199]
elemento1 = 67

print(busca_saltos(lista, elemento, 2, True))
print(busca_saltos(lista1, elemento1, 3, False))

lista = []
for i in range(0, 100):
    x = randint(-6477, 8389)
    lista.append(x)

elemento = lista[randint(0, 99)]
listaDesorganizada = lista.copy()
insertionSort(lista)
print(f'encontrei o elemento no indice {busca_hybrid(listaDesorganizada, elemento, False)} na lista não ordenada')
print(listaDesorganizada)
print(f'encontrei o elemento no indice {busca_hybrid(lista, elemento, True)} na lista ordenada')
print(lista)