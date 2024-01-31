from Cifrados.Ceasar import Ceasar
from Cifrados.Afin import Afin
from Cifrados.Vigenere import Vigenere
import unicodedata
import matplotlib.pyplot as plt

# 1 Cifrar
# 2 Frecuencias
# 3 Ordenar de mayor a menor
# 



def crear_histograma(distribuciones, probabilidad_real):
    etiquetas = probabilidad_real.keys()
    valores_reales = [probabilidad_real[letra] for letra in etiquetas]
    valores_calculados = [distribuciones.get(letra, 0) for letra in etiquetas]

    x = range(len(etiquetas))
    ancho = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, valores_reales, ancho, label='Frecuencias Reales')
    rects2 = ax.bar([p + ancho for p in x], valores_calculados, ancho, label='Frecuencias Calculadas')

    ax.set_ylabel('Frecuencias')
    ax.set_title('Comparación de Frecuencias Reales y Calculadas por Letra')
    ax.set_xticks([p + ancho / 2 for p in x])
    ax.set_xticklabels(etiquetas)
    ax.legend()

    plt.show()

# def brute_force(distribuciones, probabilidad_real):
#     distribuciones_ordenadas = dict(sorted(distribuciones.items(), key=lambda item: item[1], reverse=True))
#     probabilidad_real_ordenada = dict(sorted(probabilidad_real.items(), key=lambda item: item[1], reverse=True))
#     # print(distribuciones_ordenadas)
#     print(probabilidad_real_ordenada)


def clean_message(message):
    message = unicodedata.normalize('NFKD', message)

    clean = ''
    for char in message:
        if char.isalpha() or char == ' ':
            clean += char

    clean = clean.upper()

    return ''.join(c for c in clean if not unicodedata.combining(c))

def calcular_distribucion(texto):
    alfabeto = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    frecuencias = {letra: 0 for letra in alfabeto}

    for char in texto:
        if char in alfabeto:
            frecuencias[char] += 1

    total_caracteres = sum(frecuencias.values())

    probabilidades = {letra: (frecuencia / total_caracteres) * 100  for letra, frecuencia in frecuencias.items()}

    return probabilidades

probabilidad_real = {
                    "A": 12.53, "B": 1.42, "C": 4.68, "D": 5.86, "E": 13.68, "F": 0.69, "G": 1.01, "H": 0.70, 
                    "I": 6.25, "J": 0.44, "K": 0.02, "L": 4.97, "M": 3.15, "N": 6.71, "Ñ": 0.31, "O": 8.68, 
                    "P": 2.51, "Q": 0.88, "R": 6.87, "S": 7.98,"T": 4.63, "U": 3.93, "V": 0.90, "W": 0.01, 
                    "X": 0.22, "Y": 0.90, "Z": 0.52
                    }




start = True
while start:
    print("\nSeleccione un tipo de cifrado:\n")
    print("1. Cifrado Cesar")
    print("2. Cifrado Afin")
    print("3. Cifrado Vigenere")
    print("4. Salir")

    # try:
    option = int(input("Opcion: "))
    if option == 1:
        key = int(input("Ingrese la llave: "))
        message = input("Ingrese el mensaje: ")
        message = message.upper()
        message = clean_message(message)
        ceasar = Ceasar(key)
        encrypted = ceasar.encrypt(message)
        print("Mensaje cifrado: " + encrypted + "\n")
        decrypted = ceasar.decrypt(encrypted)
        print("Mensaje descifrado: " + decrypted + "\n")
        distribuciones = calcular_distribucion(encrypted)
        crear_histograma(distribuciones, probabilidad_real)
        # #Lab 1 parte B
        # brute_force(distribuciones, probabilidad_real)


    elif option == 2:
        multiplier = int(input("Ingrese el multiplicador: "))
        offset = int(input("Ingrese el offset: "))
        message = input("Ingrese el mensaje: ")
        message = message.upper()
        message = clean_message(message)
        afin = Afin(multiplier, offset)
        encrypted = afin.encrypt(message)
        print("Mensaje cifrado: " + encrypted + "\n")
        decrypted = afin.decrypt(encrypted)
        print("Mensaje descifrado: " + decrypted + "\n")
        distribuciones = calcular_distribucion(encrypted)
        crear_histograma(distribuciones, probabilidad_real)

    elif option == 3:
            keyword = input("Ingrese la palabra clave: ")
            message = input("Ingrese el mensaje: ")
            message = clean_message(message)
            vigenere = Vigenere(keyword)
            encrypted = vigenere.encrypt(message)
            print("Mensaje cifrado: " + encrypted + "\n")
            decrypted = vigenere.decrypt(encrypted)
            print("Mensaje descifrado: " + decrypted + "\n")
            distribuciones = calcular_distribucion(encrypted)
            crear_histograma(distribuciones, probabilidad_real)
    elif option == 4:
        start = False
        print("Saliendo...")
    else:
        print("Opcion invalida")
    # except:
    #     print("Opcion invalida")