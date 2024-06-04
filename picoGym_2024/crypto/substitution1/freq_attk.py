with open('message.txt') as f:
    data = f.read().lower()

mappings = {'b' : 'P',
            'z' : 'I',
            's' : 'C',
            'k' : 'O',
            'y' : 'T',
            't' : 'F',
            'd' : 'R',
            'v' : "K",
            'u' : 'Q',
            'n' : 'U',
            'c' : 'N',
            'o' : 'Y',
            'x' : 'M',
            'r' : 'E',
            'j' : 'A',
            'a' : 'H',
            'e' : 'S',
            'h' : 'L',
            'm' : 'G',
            'g' : 'T',
            'g' : 'W',
            'w' : 'V',
            'q' : 'D',
            'l' : 'B'
        }

for key, value in mappings.items():
    data = data.replace(key, value)

print(data.lower())