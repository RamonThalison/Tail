def pacman(arr) -> int:
    tamTabuleiro = int
    if arr[0] < 2 or arr[0] > 50: #checando umas das condições impostas pela questão
        print(f'Tamanho inválido!')
        return -1
    else:
        tamTabuleiro = int(arr[0])

    x = nElementos = 0
    for i in arr: #fiz um for it para acessar todos os elementos do array
        if type(i) == str: # fiz essa linha para ignorar o primeiro elemento
            for j in i:
                nElementos += 1
                if j != '.' and j != 'o' and j != 'G': # checa mais uma condição para o jogo funcinar
                    x += 1
            if nElementos != tamTabuleiro: # checa o tamanho das linhas
                x += 1
                break
            else:
                nElementos = 0

    if arr[1][0] != '.' or x >= 1 or len(arr) != tamTabuleiro+1: # checa outras condições
        print(f'Formatação de tabuleiro errada!') # além de servir para printar algum erro existente detectado nas linhas acima
        return -1

    pont = mPont = movimento = 0
    x = -1
    for i in arr:
        if type(i) == str: #novamente a estrategia dos for it para percorer o tabuleiro

            for j in i:

                if i[movimento] == 'o':
                    pont += 1
                elif i[movimento] == 'G':
                    pont = 0

                if pont > mPont: # pegando a melhor parada possivel
                        mPont = pont

                if x % 2 == 0:
                    if movimento < tamTabuleiro-1: #faz o movimento do pacman
                        movimento += 1
                else:
                    if movimento > 0:
                        movimento -= 1
        x += 1
    return mPont

arr = [3, ".o.", "oGG", "ooo"]
arr2 = [4, ".ooG", "oGG.", "oo.G", ".ooG"]
print(pacman(arr))
print(pacman(arr2))