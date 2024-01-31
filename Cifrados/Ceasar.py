class Ceasar():
    def __init__(self, key):
        self.key = key
        self.alphabet = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

    
    def encrypt(self, message):
        encrypted = ""
        for letter in message:
            if letter == " ":
                encrypted += " "
            else:
                encrypted += self.alphabet[(self.alphabet.index(letter) + self.key) % 27]
        return encrypted

    def decrypt(self, message):
        decrypted = ""
        for letter in message:
            if letter == " ":
                decrypted += " "
            else:
                decrypted += self.alphabet[(self.alphabet.index(letter) - self.key) % 27]
        return decrypted
    
