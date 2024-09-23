# Description

I bet you can't access my notes on giraffes!

http://chal.competitivecyber.club:8081

Flag format: CACI{.*}

# Solution

We are given `index.php` of the target website. In the first few lines, a `$allowed` variable is set,
which renders the flag. In order to set the attribute, the `HTTP_X_FORWARDED_FOR` HTTP attribute must be set.
Intercept the request, add `X-Forwarded_For: 127.0.0.1` header and get the flag.

