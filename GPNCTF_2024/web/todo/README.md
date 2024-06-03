# Description

I made a JS API! Sadly I had no time to finish it :(

# Solution

`server.js` and `script.js` are the most important parts of this challenge, so let's take a look at them.

### server.js

The first endpoint of the server is the `/chal`, which enables you to run whatever code you provide it 
(although I did not use this part of web to solve the challenge).
```javascript
app.post('/chal', (req, res) => {
    const { html } = req.body;
    res.setHeader("Content-Security-Policy", "default-src 'none'; script-src 'self' 'unsafe-inline';");
    res.send(`
        <script src="/script.js"></script>
        ${html}
    `);
});
```

Another endpoint is at `/admin`, which is a little bit more interesting. It uses puppeteer to launch a new browser, 
creates a new cookie with randomBytes (will be useful later), then runs whatever code you give it and takes a screenshot of 
the result.
```javascript
app.post('/admin', async (req, res) => {
    try {
        const { html } = req.body;
        const browser = await puppeteer.launch({ executablePath: process.env.BROWSER, args: ['--no-sandbox'] });
        const page = await browser.newPage();
        page.setCookie({ name: 'flag', value: randomBytes, domain: 'localhost', path: '/', httpOnly: true });
        await page.goto('http://localhost:1337/');
        await page.type('input[name="html"]', html);
        await page.click('button[type="submit"]');
        await new Promise(resolve => setTimeout(resolve, 2000));
        const screenshot = await page.screenshot({ encoding: 'base64' });
        await browser.close();
        res.send(`<img src="data:image/png;base64,${screenshot}" />`);
    } catch(e) {console.error(e); res.send("internal error :( pls report to admins")}
});
```

And lastly we have the `/script.js` endpoint, which returns the contents of the `script.js` file and if cookie value
is randomBytes (the same value is set in `/admin`!), it replaces the fake flag with the real one (in `script.js`).
```
app.get('/script.js', (req, res) => {
    res.type('.js');
    let response = script;
    if ((req.get("cookie") || "").includes(randomBytes)) response = response.replace(/GPNCTF\{.*\}/, flag)
    res.send(response);
});
```

For completeness' sake here is the contents of the `/script.js`:
```javascript
class FlagAPI {
    constructor() {
        throw new Error("Not implemented yet!")
    }

    static valueOf() {
        return new FlagAPI()
    }

    static toString() {
        return "<FlagAPI>"
    }

    // TODO: Make sure that this is secure before deploying
    // getFlag() {
    //     return "GPNCTF{FAKE_FLAG_ADMINBOT_WILL_REPLACE_ME}"
    // }
}
```

So the goal is to pass some code into the `/admin` endpoint to also access the `/scipt.js` file:
1. one way how to do it to use the `Function.prototype.toString` of javascript to print the source code of
   `script.js`. We can for example set the `FlagAPI.valueOf = Function.prototype.toString` and then call `FlagAPI.valueOf()`.
   So the overall payload is
   ```javascript
   <script>
     FlagAPI.valueOf = Function.prototype.toString;
	   document.write(FlagAPI.valueOf());
   </script>
   ```
2. another way to solve it is to redirect to the `/script.js` directly with `document.location.replace('/script.js

Anyways, we get the flag:

<img width="383" alt="Untitled (1)" src="https://github.com/AdamZvara/CTF/assets/36104483/51566556-a62f-4ceb-8fc0-0201ecf375f0">
