#!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys
from PIL import Image
import matplotlib.pyplot as plt
import math
import itertools

##########################
#Segundo Trabalho de PDI#
##########################

def MyDCT(vector):
  result = []
  factor = math.pi / len(vector)
  for i in range(len(vector)):
    soma = 0.0
    for (j, val) in enumerate(vector):
      soma += val * math.cos((j + 0.5) * i * factor)
    result.append(soma)
  return result

def InvMyDCT(vector):
	result = []
	factor = math.pi / len(vector)
	for i in range(len(vector)):
		soma = vector[0] / 2.0
		for j in range(1, len(vector)):
			soma += vector[j] * math.cos(j * (i + 0.5) * factor)
		result.append(soma)
	return result

def pegaPixel(imagem, i, j):
  width, height = imagem.size
  if((i > width) or (j > height)):
    return None
  pixel = imagem.getpixel((i, j))
  return pixel

def pegaLinhaPixel(imagem, row):
  width, height = imagem.size
  pixel = []
  if(row > width or row < 0):
    return None
  for i in range(height):
    pixel.append(imagem.getpixel((row, i)))
  return pixel

def pegaColunaPixel(imagem, col):
  width, height = imagem.size
  pixel = []
  if(col > height or col < 0):
    return None
  for i in range(width):
    pixel.append(imagem.getpixel((i, col)))
  return pixel

def abreImagem(destino):
  imagem = Image.open(destino)
  return imagem

def salvaImagem(imagem, destino):
  imagem.save(destino, 'png')

def criaImagem(i, j):
  imagem = Image.new("L", (i, j))
  return imagem

def cinzaScale(imagem):
  return imagem.convert('L')

def trans(mat):
  result = []
  for n in range(len(mat[0])):
    aux = []
    for m in range(len(mat)):
      aux+=[mat[m][n]]
    result.append(aux)
  return result

def zigzag(rows,columns,matrix):
  solution=[[] for i in range(rows+columns-1)] 
  for i in range(rows): 
    for j in range(columns): 
      soma=i+j 
      if(soma%2 ==0): 
        solution[soma].insert(0,matrix[i][j]) 
      else: 
        solution[soma].append(matrix[i][j])
  return solution 

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

def Filter_N(amostras, n, n_colunas,n_elements):

    aux = list(enumerate(itertools.chain.from_iterable(amostras))) #join - Cria uma lista com os valores lidos

    aux.sort(key=lambda tup: abs(tup[1]), reverse=True)  #ordena em forma decrescente, de acordo com val
    i=0

    #figura DCT
    plt.figure(1)
    plt.subplot(211)
    plt.ylabel("Freq")
    plt.xlabel("Original")
    plt.plot(list(aux))

    #n -> separa os valores mais importantes para acima de um limiar 'n' 
    for i in range(len(aux)):
        if(i>=n):
            indice,dado = aux[i]
            aux[i] = (indice,0)  

    #figura filtrada
    plt.subplot(212)
    plt.ylabel("Freq")
    plt.xlabel("Filtrado")
    plt.plot(list(aux))
    plt.show()

    #ordena as amostras em suas posições originais
    aux.sort(key=lambda tup: abs(tup[0]))  
    newimage = GetDados(aux)

    return  [newimage[i: i+n_elements] for i in range(0, len(newimage), n_elements)]


if __name__ == "__main__":
  for indice in range(2):
    if(indice > 0):
      imagem = abreImagem(str(indice)+".jpg")
      imagem = cinzaScale(imagem)
      width, height = imagem.size
      ParcialDCTCol = []
      ParcialDCTRow = []
      FullDCT = []
      iDCT = []
      LinhasiDCT = []
      parinv = []
      N = 5000

      #DCT
      for n in range(width): #Primeira DCT (DCT da Linha)
        RowVetPixel = pegaLinhaPixel(imagem,n)
        ParcialDCTRow.append(MyDCT(RowVetPixel))
      ParcialDCTCol = trans(ParcialDCTRow)
      for i in range(height):
        FullDCT.append(MyDCT(ParcialDCTCol[i]))  #Segunda DCT (DCT da coluna)

      #Filtro N importantes
      n_colunas = len(FullDCT)
      n_elements= len(FullDCT[0])
      FullDCT = Filter_N(FullDCT,N,n_colunas,n_elements)   #e recebe os valores filtrados

      # inversa DCT
      for i in range(height):
        parinv.append(InvMyDCT(FullDCT[i]))
      LinhasiDCT = trans(parinv)
      for i in range(width):
        iDCT.append(InvMyDCT(LinhasiDCT[i]))

      adt = 0
      newImage = criaImagem(width,height)
      pixel = newImage.load()
      for i in range(height):
        for j in range(width):
          pixel[j,i] = (int((iDCT[j][i]+adt)/10000))
      salvaImagem(newImage,str(indice)+"_output_"+str(N)+".png")