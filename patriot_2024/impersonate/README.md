# Description

One may not be the one they claim to be.

http://chal.competitivecyber.club:9999/

# Solution

We are given a source code of the server app. The first thing we see is that the server uses flask
and generates secret key based on the timestamp of when the server was started. The app has several
endpoints:

- `/` has login form (with some filters on the username and stuff), redirects to `user/{id}` after logging in
- `/user/<uid>` displays user page, disables `is_admin` session flag
- `/admin` if the user is admin, print the flag
- `/status` print uptime

The app uses flask session cookies to store information about the user so the goal is pretty simple:

1. get the secret key (from the `/status` endpoint)
2. use the key to sign newly created cookie as administrator
3. visit `/admin` to get the page

Use `forge.py` to generate the session cookie (remember to change the `server_start_str` variable).