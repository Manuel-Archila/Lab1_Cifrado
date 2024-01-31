class Afin():
    def __init__(self, multiplier, offset):
        self.multiplier = multiplier
        self.offset = offset
        self.alphabet = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        


    def encrypt(self, message):
        encrypted = ''
        for char in message:
            if char in self.alphabet:
                encrypted += self.alphabet[(self.alphabet.index(char) * self.multiplier + self.offset) % len(self.alphabet)]
            else:
                encrypted += char
        return encrypted

    def inverse_modulo(self, a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        

    def decrypt(self, message):
        decrypted = ''
        multiplier_inverse = self.inverse_modulo(self.multiplier, len(self.alphabet))
        for char in message:
            if char in self.alphabet:
                index = self.alphabet.index(char)
                decrypted_index = (multiplier_inverse * (index - self.offset)) % len(self.alphabet)
                decrypted += self.alphabet[decrypted_index]
            else:
                decrypted += char
        return decrypted
