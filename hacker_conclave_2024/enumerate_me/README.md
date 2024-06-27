# Description

In this challenge, the flag has been hidden inside one of the website files.
The files to enumerate is one of the listed into test.txt wordlist in Discovery directory of this repo (link to seclists github repository)
Will you be able to find it?

# Solution

Find the test.txt wordlist in seclists:
```bash
find /usr/share/seclists/Discovery | grep test
```
which found 2 files:
```
/usr/share/seclists/Discovery/Web-Content/SVNDigger/context/test.txt
/usr/share/seclists/Discovery/Web-Content/tests.txt
```

Next, use ffuf to fuzz the endpoint. I have tried the first file, which did not work, but got a result when using the second file:
```bash
ffuf -u http://ctf.thehackerconclave.es:20002/images/FUZZ.jpg -w /usr/share/seclists/Discovery/Web-Content/tests.txt
```

The flag could be found at `http://ctf.thehackerconclave.es:20002/images/prova2`