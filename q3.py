class AutomatoPilha:
    def __init__(self, palavra) -> None: #os objetos vão precisar passar a palavra
        self.palavra = palavra # na criação do objeto
        self.alfabeto = 'abc'
        self.estado = 'EI' #define estado inicial
        self.pilha = []

    def verificaPalavra(self):
        quantb = 0
        if self.palavra == '':
            return 'Palavra nao aceita'
        for simbolo in self.palavra:
            if simbolo not in self.alfabeto or self.palavra[0] != 'a': # verifica alfabeto
                return 'Palavra nao aceita' # e a condição de pelo menos uma simbolo 'a'

            if self.estado == 'EI' and simbolo == 'a':
                self.pilha.append('B') #comeca a empilhar um B para cada 'a'

            elif self.estado == 'EI' and simbolo != 'a':
                if simbolo == 'b': #se o proximo simbolo diferente de 'a' for 'b'
                    self.estado = 'E1' # muda estado
                    # não vou deletar nenhum elemento nessa interação para a
                    # lógica de transição do b pro c
                    quantb += 1
                else: # caso de j = 0, ou seja i > j
                    return 'Palavra nao aceita'

            elif self.estado == 'E1' and simbolo == 'b':
                quantb += 1
                try:
                    self.pilha.pop() # desempilha 'B'
                except: # se der erro quer dizer que tem mais 'b' que a
                    pass #então esta correto

            elif self.estado == 'E1' and simbolo == 'c':
                if len(self.pilha) > 0: # quer dizer que a lista tinha mais 'a' que 'b'
                    return 'Palavra nao aceita'
                self.estado = 'EF'
                for i in range (1, quantb):# empilha 'B' novamente com um a menos
                    self.pilha.append('B') # economiza a linha do pop()

            elif self.estado == 'EF' and simbolo == 'c':
                self.pilha.pop() # desempilha 'B'
                if len(self.pilha) == 0: # quer dizer que k >= j
                    return 'Palavra nao aceita'
        return 'Sucesso!'
    
                             # resultado esperado:
a = AutomatoPilha('aaabbc')  # 'Palavra nao aceita'
b = AutomatoPilha('abbc')    # 'Sucesso!'
c = AutomatoPilha('abbccc')  # 'Palavra nao aceita'
d = AutomatoPilha('abbcd')   # 'Palavra nao aceita'
e = AutomatoPilha('abBc')    # 'Palavra nao aceita'
f = AutomatoPilha('aabbcc')  # 'Palavra nao aceita'
g = AutomatoPilha('aabbbc')  # 'Sucesso!'
h = AutomatoPilha('bbc')     # 'Palavra nao aceita'
i = AutomatoPilha('')        # 'Palavra nao aceita'
j = AutomatoPilha('aabbbbcc')# 'Sucesso!'
k = AutomatoPilha('abb')     # 'Sucesso!'

print(a.verificaPalavra())
print(b.verificaPalavra())
print(c.verificaPalavra())
print(d.verificaPalavra())
print(e.verificaPalavra())
print(f.verificaPalavra())
print(g.verificaPalavra())
print(h.verificaPalavra())
print(i.verificaPalavra())
print(j.verificaPalavra())
print(k.verificaPalavra())