from PIL import Image
from random import randint
import matplotlib.pyplot as pl

'''
Ordena os valores lidos a partir de um vetor que é ordenado de acordo com as 
frequencias de maior valor,em ordem decrescente e em módulo. 
Disto os "n" primeiros valores de frequencia são preservados e o restante colocado para zero.
'''
def GetDados(ListDados):
    newDados = []   #vetor que recebe os valores filtrados
    for i in range(len(ListDados)):
        j,temp = ListDados[i]
        newDados.append(temp) 
    return(newDados)

def Filter_N(amostras):
    aux = list(enumerate(amostras)) #Cria uma lista com os valores lidos
    print(aux)
    print("------------------------------------------------------------------------")
    #aux = (ind,val)
    aux.sort(key=lambda tup: abs(tup[1]), reverse=True)  #ordena em forma decrescente, de acordo com val
    i=0
    n = 5800     #separa os valores mais importantes para acima de um limiar 'n' 

    for i in range(len(aux)):
        if(i>=n):
            indice,dado = aux[i]
            aux[i] = (indice,0)  

    imagefilter = GetDados(aux)

    #ordena as amostras em suas posições originais
    aux.sort(key=lambda tup: abs(tup[0]))  

    newimage = GetDados(aux)
    print(newimage)

    pl.figure(1)
    pl.subplot(211)
    pl.plot(imagefilter)

    pl.subplot(212)
    pl.plot(newimage)

    pl.show()


if __name__ == "__main__":
    
    amostras=[]
    for i in range(10000):
        amostras.append(randint(-255, 255))
    Filter_N(amostras)