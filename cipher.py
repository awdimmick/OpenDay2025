def letter_to_number(letter):
    return ord(letter) - 64

def number_to_letter(number):
    return chr(number + 64)

def shift_letter(letter, key):
    shiftedNum = letter_to_number(letter) + key
    
    if shiftedNum < 1:
        shiftedNum = shiftedNum + 26
    elif shiftedNum > 26:
        shiftedNum = shiftedNum - 26

    return number_to_letter(shiftedNum)

message = input("Enter a message to encrypt: ")
key = int(input("Enter the key: "))

output = ""

for letter in message:
    output += shift_letter(letter, key)

print(output)


