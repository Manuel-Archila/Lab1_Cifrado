from Cifrados.Ceasar import Ceasar
from Cifrados.Afin import Afin
from Cifrados.Vigenere import Vigenere
import unicodedata
import matplotlib.pyplot as plt
import itertools

# 1 Cifrar
# 2 Frecuencias
# 3 Ordenar de mayor a menor
# 4 Definir el desplazamiento



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

def brute_force_cesar(distribuciones, probabilidad_real, mensaje_cifrado):
    letras = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    letra_mas_frecuente_dist = max(distribuciones, key=distribuciones.get)
    letra_mas_frecuente_real = max(probabilidad_real, key=probabilidad_real.get)

    desplazamiento_inicial = (letras.index(letra_mas_frecuente_real) - letras.index(letra_mas_frecuente_dist)) % len(letras)
    print(f"Desplazamiento inicial: {desplazamiento_inicial}")
    indice_inicial = letras[letras.index(letra_mas_frecuente_real) - desplazamiento_inicial]

    # Probando desplazamientos a partir del desplazamiento inicial
    with open('ceasar.txt', 'w', encoding='utf-8') as file:
        for i in range(len(letras)):
            desplazamiento_actual = (desplazamiento_inicial + i) % len(letras)
            cesar = Ceasar(desplazamiento_actual)
            mensaje_descifrado = cesar.decrypt(mensaje_cifrado)
            file.write(f"Desplazamiento: {desplazamiento_actual} - Mensaje: {mensaje_descifrado}\n")
    
def brute_force_afin(mensaje_cifrado):
    letras = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    with open('afin.txt', 'w', encoding='utf-8') as file:
        for i in range(len(letras)):
            for j in range(len(letras)):
                try:
                    afin = Afin(i+1, j+1)
                    mensaje_descifrado = afin.decrypt(mensaje_cifrado)
                    file.write(f"Multiplicador: {i+1}, Offset: {j+1} - Mensaje: {mensaje_descifrado}\n")
                except:
                    pass
                    #print(f"ERROR: Multiplicador: {i+1}, Offset: {j+1} - Mensaje: {mensaje_descifrado}")

def calcular_indices_de_coincidencia(texto_cifrado, max_key_length=10):
    texto_cifrado = texto_cifrado.replace(" ", "").upper()
    longitud = len(texto_cifrado)
    indices_de_coincidencia = []

    # Compara el texto con una versión desplazada de sí mismo
    for desplazamiento in range(1, max_key_length + 1):
        coincidencias = 0
        for i in range(longitud - desplazamiento):
            if texto_cifrado[i] == texto_cifrado[i + desplazamiento]:
                coincidencias += 1
        indices_de_coincidencia.append((desplazamiento, coincidencias))

    return indices_de_coincidencia

def clave_vigenere(texto_cifrado):
    indices = calcular_indices_de_coincidencia(texto_cifrado)
    key_length = 0
    max_coincidencias = 0
    for i in range(len(indices)):
        if indices[i][1] > max_coincidencias:
            max_coincidencias = indices[i][1]
            key_length = indices[i][0]
        else:
            break
    return key_length

            
def brute_force_vigenere(mensaje_cifrado):
    letras = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    key_length = clave_vigenere(mensaje_cifrado)
    print(f"Longitud de clave: {key_length}")

    

    with open('vigenere.txt', 'w', encoding='utf-8') as file:
        for key in itertools.product(letras, repeat=key_length):

            possible_key = ''.join(key)
            decrypted_text = Vigenere(possible_key).decrypt(mensaje_cifrado)
            # Aquí puedes implementar una verificación para ver si el texto descifrado tiene sentido
            file.write(f"Clave probada: {possible_key} -> Mensaje: {decrypted_text}\n")




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
    print("4. Probar archivos predefinidos")
    print("5. Salir")

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
        #Lab 1 parte B
        brute_force_cesar(distribuciones, probabilidad_real, encrypted)


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
        #Lab 1 parte B
        brute_force_afin(encrypted)

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
            #Lab 1 parte B
            brute_force_vigenere(encrypted, 5)
    
    elif option == 4:
        ceasar_encrypted = ''
        afin_encrypted = ''
        vigenere_encrypted = ''
        with open('./texts/cipher1.txt', 'r', encoding='utf-8') as archivo:
            ceasar_encrypted = archivo.read()
        
        with open('./texts/cipher2.txt', 'r', encoding='utf-8') as archivo:
            afin_encrypted = archivo.read()
        
        with open('./texts/cipher3.txt', 'r', encoding='utf-8') as archivo:
            vigenere_encrypted = archivo.read()
        
        #print(ceasar_encrypted)
        #print(afin_encrypted)
        #print(vigenere_encrypted)
        distribuciones = calcular_distribucion(ceasar_encrypted)
        brute_force_cesar(distribuciones, probabilidad_real, ceasar_encrypted)
        brute_force_afin(afin_encrypted)
        brute_force_vigenere(vigenere_encrypted)

        print("Cifrado Cesar")
        print("Desplazamiento 19")
        print("Cifrado afin")
        print("Multiplicador 23, Offset 7")
        print("Cifrado Vigenere")
        print("Clave: BEES")


    elif option == 5:
        start = False
        print("Saliendo...")
    else:
        print("Opcion invalida")
    # except:
    #     print("Opcion invalida")