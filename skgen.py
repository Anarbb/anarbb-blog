import random
import string


# Generates a random sequence of Upper and lowercase letters for the secret key
class SkGen():
    def __init__(self, length):
        self.length = length

    def gen(self):
        letters = string.ascii_lowercase + \
            string.ascii_uppercase
        result_str = ''.join(random.choice(letters)
                             for i in range(self.length))
        return result_str
