import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def random_pw_gen():
    nr_letters = random.randint(8,10)
    nr_numbers = random.randint(2,4)
    nr_symbols = random.randint(2,4)

    final_password_list = []

    letter_list = [random.choice(letters) for _ in range(nr_letters)]
    number_list = [random.choice(numbers) for _ in range(nr_numbers)]
    symbol_list = [random.choice(symbols) for _ in range(nr_symbols)]

    password = letter_list + number_list + symbol_list

    random.shuffle(password)

    return "".join(password)




