### Task1

- task: log in as administrator

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/b10a1ce3-97e4-4d9d-815f-0d3e044dff80">
</p>

- the hint and the “forgotten password” talk about mascot of the most viewed czech server ⇒ seznam and their mascot is “krasty”
- bruteforce was not neccasery as I guessed a few combinations and found login `adminstrator` and the password `Krasty`

### Task 2

- task: same goal as in task 1, but we get additional infromation which suggested, that we are loggining into “D-Link router” with Firmware DI-604UP

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/cf01eff8-1ffb-402f-98db-63777b150f6d">
</p>

- after a little bit of [googling](https://support.dlink.com/resource/PRODUCTS/TM-G5240/REVA/TM-G5240_SECURITY_ADVISORY_1.00_EN.PDF) I found out that this version has CVE, where the login is bypassed with User-agent
- being `xmlset_roodkcableoj28840ybtide`

### Task 3

- task: same as in task 1, but the hint says that the server contains backups of sensitive data
- when intercepting the request I noticed that the request now goes to `/library/login.php` instead of going directly to `/level3.php` as in previous challenges
- after changing the request to use the GET method and accessing library endpoint directly, the website leaks the directory structure, from which we can see that the server has `topsecret.txt` file

<p align="center">
<img  src="https://github.com/AdamZvara/CTF/assets/36104483/327b10c9-e1b7-4328-8067-e31a149e7e24">
</p>

- we can get the topsecret file which has the username and the password to log in
  
<p align="center">
<img align="center" src="https://github.com/AdamZvara/CTF/assets/36104483/12aa3f7e-f606-4c10-b28d-1906e4a89e1e">
</p>

### Task 4

- task: log in as administrator of the page
- user id is passed via the GET parameter and the hint is SQL injection … I guessed that the SQL injection will not be in the login form but in the GET parameter
- when first accessing the page, the uid is set to value 1 and the login is already filled with name `john` … I tried other uids but only found another user `bob` at uid = 2
- to make life easier I have used the `sqlmap` tool to inject the uid parameter and get the contents of the users database
- `sqlmap -u https://safeweb.aec.cz/level4.php?uid=1 --dump -T users -p uid --cookie "PHPSESSID=rjevvhai4..."`

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/d1596cda-e4e4-484c-8418-cfc98e688641">
</p>

- as we can see the password is not encrypted and we can log in directly

### Task 5

- task: log in as admin, we are provided with account `guest/tajneheslo` and the hint is “cookies”

<p align="center">
<img  src="https://github.com/AdamZvara/CTF/assets/36104483/e7a72cf8-52fd-4b13-b30e-a462e7912947">
</p>

- first, lets see the request after correct login attempt
  
<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/76008e7d-d58b-45ca-8c45-b4ab93aae2c9">
</p>

- the server responds with 2 cookies … the second one looks like it is encoded in base64 so after decoding it we get string `guest7`
- we can edit the cookie value with base64 encoded string “admin” (`YWRtaW4=`), refresh the page and we solve the challange

### Task 6

- task: use XSS to call alert function which writes the contents of the cookie, the hint was multiline javascript comment

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/4822b74d-a5e4-4605-bba1-3050aaa53a72">
</p>

- the javascript code to print the contents of the cookie is `"><script>alert(document.cookie)</script>`, but the length of this code is above 30 characters, which is the maximum length allowed in each field
- therefore we need to split the code into multiple parts using the multiline comment in javascript

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/36df10e6-0dd6-4869-8e8c-2aea727f2e2f">
</p>

### Task 7

- task: log in into private section of the web … the assignment contained link to a pdf file

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/cc426dd6-4d6e-4e4a-84f6-528df1a4209e">
</p>

- when looking at the request after following the link from the assignment we can see that we are using the download.php file to get some file with id = 42 `/download.php?file_id=42`
- we can bruteforce the numbers (from 0 to 100) to find the flag
    - I saved the request from burp into file, set the destination to `GET /download.php?file_id=FUZZ HTTP/1.1` and used ffuf to filter 200 status code responses

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/a78cc9b0-0c18-41fc-a62c-37a69d91810c">
</p>

- after accessing the /download.php?file_id=87 I found the password and logged in

### Task 8

- task: log in into private section of web … the hint is that password validation is at client side
- right click is disabled on the website … probably so we can’t debug the javascript and get the flag right away
    - we can save the captured response from burp into file, remove the HTTP header to get the website contents
    - to enable rightclick remove the line with `contextmenu` variable being set to false

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/c9e670e7-ec33-4f57-8c44-23d89c429b10">
</p>

- we did all this so we don’t have to actually understand the javascript, god forbid
- now we can open the page locally, go into developer mode, set breakpoint to where the password is being compared and print to what value we are comparing it with

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/9a6103cd-5b56-4560-a33c-05b775ebaba0">
</p>

### Task 9

- task: log in … we are given an executable file and the hint is that we do not need to know assembly

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/0ec1c551-7fa8-4d01-a5bc-b93bf23f8ec1">
</p>

- since we probably don’t need to decompile it I assumed that the flag is hardcoded as a string and found it with strings command

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/53ab6ac5-dc1c-4226-a525-00aaa050e40d">
</p>

### Task 10

- task: print the contents of `/etc/passwd`, the hint is null byte
- path traversal from the GET parameter `https://safeweb.aec.cz/level10.php?page=main`
    - after trying to access `/level10.php?page=../etc/passwd` the server replied with “File /var/www/../etc/passwd.php not found or does not exist”
    - from this we know that we need to go 3 directories to the back and that the server always appends `.php` extension to the name we give it … so we need to end the request with null byte to skip the extension
    - `https://safeweb.aec.cz/level10.php?page=../../../etc/passwd%00`

### Task 11

- this was the task I was stuck the longest on (tried alot of things but then got lucky when revisiting the page after some time)
- task: upload a file, which after being loaded into browser executes PHP script with any function

<p align="center">
<img  src="https://github.com/AdamZvara/CTF/assets/36104483/f6b517da-4bf0-4231-8f8e-9db433490c3f">
</p>

- let’s try and upload normal image called `burrito.png` and then `test.php` with php code that calls phpinfo()
    - the normal image gets uploaded, but no code is executed as expected

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/788c1bfe-565c-4c99-ac7b-9252bf3feedc">
</p>

- the php file gets blocked by some filter, which looks for the extension of the file

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/3802a302-d36d-490d-9669-e01ed8f06e57">
</p>

- let’s play abit with the request when uploading the php file and try to find something useful
    - if I try to change the extension of the file to `test.png` the file still gets blocked probably due to the content type of MIME being set to `Content-Type: application/x-php`
    - if I try to change it to `image/png` the file gets uploaded but no code is executed
    - changing the filename to `test.php.png` works (the file gets uploaded) but the code is not yet executed
    - however when changing the filename to `test.php.abcpng` the file gets uploaded and the script executes aswell

### Task 12

- task: rewrite the CAPTCHA code presented on the page 500 times
  
<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/4f993dac-dc42-486e-9c22-bf634cd2de45">
</p>

- I made a simple python script which consisted of 3 parts
    - first, get the captcha value from a request

```python
def get_captcha_value(url, cookie):
    response = requests.get(url, cookies=cookie)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        captcha_element = soup.find("span",id='cid')
        if captcha_element:
            return captcha_element.text
    return None
```

- set the parameters

```python
base_url = "https://safeweb.aec.cz"  # Replace with the actual base URL
post_url = f"{base_url}/level12.php"
captcha_parameter = "captcha"
ok_parameter = "ok"
ok_value = "Send"
cookie = {"PHPSESSID": "2fa8mpjr73v8kjsdgnte5fn7f1"}
```

- do the captcha

```python
for i in range(500):
    # Get captcha value
    captcha_value = get_captcha_value(post_url, cookie)

    # Make POST request
    if captcha_value:
        data = {captcha_parameter: captcha_value, ok_parameter: ok_value}
        response = requests.post(post_url, data=data, cookies=cookie)
    else:
        print("Failed to get captcha value.")
```

### Task 13

- task: run the phpinfo function on the server
- the hint is “process environment”
- after googling abit I found out that it probably has to do something with the linux `/proc/self/environ` file, like [in this link](https://www.linkedin.com/pulse/burp-procselfenviron-its-shell-time-melina-phillips-cissp-ejpt-sscp/)
- since the script is passed via GET parameter, we can use LFI to leak the contents of environ file

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/8d1ceabe-6421-4e7c-9abe-76bafde877e8">
</p>

- the environ file contains the user-agent, so if we smuggle call to phpinfo inside the user-agent we should be able to call the function

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/bc43ff99-1060-4660-9268-32540dad7298">
</p>

### Task 14

- using waybackmachine to recover some page and print the name of the virus

### Task 15

- task: log in .. the password is the name of the user running the script, hint: full path disclosure:

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/39465779-c835-4bb4-b575-53e20fd8a355">
</p>

- intercept and modify the request, so error occurs when parsing it .. for example password[]=bcv&ok=Login fails, because password is not expected to be an array … the app also leaks the error message and prints it to user, from which we can see that name of the user running the script

<p align="center">
<img src="https://github.com/AdamZvara/CTF/assets/36104483/daffda06-16b3-4033-8809-e2fac377fb6d">
</p>
