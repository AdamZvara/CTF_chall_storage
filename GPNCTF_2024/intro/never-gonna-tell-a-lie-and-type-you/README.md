# Description

todo

# Solution
We are given 2 files, `Dockerfile` and `index.php`. I assume that the only purpose of the Dockerfile is to find the 
flag more easily … we can see that the flag is at `/flag.txt`. Let’s check out the index.php file:
```php
function securePassword($user_secret){
    if ($user_secret < 10000){
        die("nope don't cheat");
    }
    $o = (integer) (substr(hexdec(md5(strval($user_secret))),0,7)*123981337);
    return $user_secret * $o ;

}
//this weird http parameter handling is old we use json
$user_input = json_decode($_POST["data"]);
//attention handling user data is dangerous

if ($_SERVER['HTTP_USER_AGENT'] != "friendlyHuman"){
    die("we don't tolerate toxicity");
}
    if($user_input->{'user'} === "admin🤠") {
        if ($user_input->{'password'} == securePassword($user_input->{'password'})  ){
            echo " hail admin what can I get you ". system($user_input->{"command"});
        }
        else {
            die("Skill issue? Maybe you just try  again?");
        }}
```
Okay so there are 4 main things to pay attention to
    1. the parameters are accessed via POST request, in which the “data” variable holds a json, which has variables “user” and “password”
    2. first, the user agent is check if it matches “friendlyHuman”
    3. then, the user variable is checked against “admin” with smiley cowboy emoji
    4. lastly, the password is checked agains `securePassword` function

We can bypass the first 3 points easily with burp, the last point might give us a headache
    - the secure function takes the password (checks if it is bigger than 10000), then takes 8B from the MD5 hash, multiplies it by some big value and multiplies the result with the original password
    - from this we can probably guess that the password must be an integer (otherwise we get an error when trying to multiply string with number)
- first, we can notice that the password condition only uses loose comparison (== instead of ===), which can perhaps lead to type juggling
    - so maybe something like: if `password = 0e` … then the result of the securePassword function would also be 0 and the condition would be true
    - however we can’t do that because of the condition that the number must be larger than 10000
- then I thought about putting some reaaally big number as password … php must have some kind of limit on integer size, right?
    - i’ve made this neat print out to check the intermediate results of the securePassword function
    - first, let’s try with 10000 (I’ve also done the user by copying and pasting the username directly from sourcecode and set the user agent so we can get to the last condition)
 
<img width="401" alt="Untitled (4)" src="https://github.com/AdamZvara/CTF/assets/36104483/8f5e4ef4-5ef4-4e70-8881-33dd5eaf40dc">

- let’s try bigger number
  
<img width="466" alt="Untitled (5)" src="https://github.com/AdamZvara/CTF/assets/36104483/ae6a78a2-4c1c-4735-b5ad-58e262cf81aa">

- let’s try number with 10000 digits
 
<img width="170" alt="Untitled (6)" src="https://github.com/AdamZvara/CTF/assets/36104483/d5bde3ba-aca2-4898-b66f-28eeae483313">

Okay so we can see that the integer is too big and it returned INF … what is not shown in the screenshot is also an error 
which comes from not specifying the `command` parameter, as we completed the last condition (yay!). Now just run on the real 
server and supply the command with `cat /flag.txt`:

<img width="278" alt="Untitled (7)" src="https://github.com/AdamZvara/CTF/assets/36104483/dd5df668-2256-4ea6-8335-caeec26be042">
