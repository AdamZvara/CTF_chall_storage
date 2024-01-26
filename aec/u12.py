import requests
from bs4 import BeautifulSoup

# Function to extract captcha value from the site
def get_captcha_value(url, cookie):
    response = requests.get(url, cookies=cookie)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        captcha_element = soup.find("span",id='cid')
        if captcha_element:
            return captcha_element.text
    return None

# URL and parameters
base_url = "https://safeweb.aec.cz"  # Replace with the actual base URL
post_url = f"{base_url}/level12.php"
captcha_parameter = "captcha"
ok_parameter = "ok"
ok_value = "Send"
cookie = {"PHPSESSID": "2fa8mpjr73v8kjsdgnte5fn7f1"}

for i in range(500):
    # Get captcha value
    captcha_value = get_captcha_value(post_url, cookie)

    # Make POST request
    if captcha_value:
        data = {captcha_parameter: captcha_value, ok_parameter: ok_value}
        response = requests.post(post_url, data=data, cookies=cookie)
    else:
        print("Failed to get captcha value.")
