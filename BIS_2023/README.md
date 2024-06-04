# Secrets

- **Tajemstvi_A_f4d1a8a9ea7bee39dc99bfc2a504e53040c65115649ef5caaa3a4ba1b14218bc**
- **Tajemstvi_B_97e4d5bf078112cbb82b59fcc11a3d540c91188b5608235eb285b5ff7455f3c0**
- **Tajemstvi_C_cd9b7eb8c0f73d6d51d97332bfc72064ec418efd2535eb8d3da7845a3a02b722**
- **Tajemstvi_D_5da2df1daa087a1852c70ef3d4026d80fb5eac39777dc159a2140393fd784e5e**
- **Tajemstvi_E_cb474912685a598d9325bd4d4e3b88015e006582297cb0aa6802cb001302980c**
- **Tajemstvi_F_3478c34d69e2579ab175a81621b5e170138a94519a7cbc5bb47e870ba2c5a0c0**
- **Tajemstvi_G_c00233328e2d05243820fbffab8e3a84f4afe8d02b9048638d93321227ea75ef**
- **Tajemstvi_H_fcc185f690980d2ed7e1c7c7e7cb425d6511be7dded8512625bc47c8c50f7d4e**
- **Tajemstvi_I_82bdb89be1e4525da9de6c1f38e996452ab0c6c8842081f477601d15232b14d2**
- **Tajemstvi_J_18520ce28fd10f69f44ad3323e59781f9ee8ecb01ee24cd41519de1028d9fbd8**

# Solution

## Scanning

- after connecting to initial login server, there is only .ssh directory with some config and key - ssh to another server (60) using the key
- found another server in .ssh/config with user jimmy (server 19 2.168.122.60)
    - scanning for other servers within range `nmap 192.168.122.1-254` since nmap was not availiable from the login server

    ```jsx
    Nmap scan report for 192.168.122.21
    PORT     STATE SERVICE
    22/tcp   open  ssh
    111/tcp  open  rpcbind
    2049/tcp open  nfs

    Nmap scan report for 192.168.122.134
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

    Nmap scan report for 192.168.122.164
    PORT   STATE SERVICE
    21/tcp open  ftp
    22/tcp open  ssh

    Nmap scan report for 192.168.122.249
    PORT     STATE SERVICE
    22/tcp   open  ssh
    9418/tcp open  git

    OTHERS
    192.168.122.27 (???)
    192.168.122.38 (???)
    192.168.122.43 (???)
    192.168.122.60 (jimmy)
    20048/tcp mountd (nfs) - probably left from other students
    192.168.122.84 (???)
    192.168.122.131 (???)
    192.168.122.216 (bob)
    ```


### 192.168.122.60 - jimmy

- a lot of garbage files … student not cleaning after themselves makes this a little bit harder
- found /logs directory, which is updated by root every 5 minutes … so it is probably not from students
- download the file and inspect in wireshark - contains comunication on telnet between 2 servers … user *bob* is trying to log in into his account on server 216 … we can sniff out the password
    - password: MegaSuperHeslo123NikdoHoNezjisti
    - then he tries to run file ohno.exe ? not found and logs out
- there is also similiar folder /trash which contains 4 hidden invoice files and 1 picture (also updated by root every 5 minutes)
- file contents:
    - .3691_2023_08_25.invoice - Coffee ... $5 to Yummy stuff company
    - .3712_2023_04_13.invoice - Donuts ... $10 to Sweet torus
    - .3789_2023_09_07.invoice - **Tajemstvi_A_f4d1a8a9ea7bee39dc99bfc2a504e53040c65115649ef5caaa3a4ba1b14218bc**
    - .3854_2023_09_30.invoice - Some software things ... $20 to Megahard
    - and also some .jpeg file - download it and inspect it
- trying to look for secret `find / 2>/dev/null | grep secret` only reveals some files in `/dev/shm/...` which were created by user jimmy .. so I am assuming that another student left those in there … but it contains some hints
    - public.key and private.key - probably contain gpg keys for another user (found later)
    - /ftp contains files probably gathered from ftp server: images, secret.txt and text.txt

### 192.168.122.134 - http server

- on this server there is a http service running - we can try to get some initial information with `curl 192.168.122.134`
- we can see `/user.php?id=0` to get user account, `/upload/index.php` to upload an image and admin page
- we can also work with elinks - command line internet browser which I have noticed on jimmy’s server
    - printing out `cat .elinks/globhist` (i am not sure if this was left here intended or not) we can see after accessing [`http://192.168.122.134/secret/`](http://192.168.122.134/secret/) there is a valid connection to secret company stuff
    - after accessing /secret/ we can find another flag **Tajemstvi_G_c00233328e2d05243820fbffab8e3a84f4afe8d02b9048638d93321227ea75ef**
- since when uploading files there is a vulnerability if the server does not check the file type properly, we can try and attack the server by uploading some kind of modified files (php script as we know from secret on git server)
    - trying to upload valid jpeg file to see what happens - from the file script `/upload_file.php` is called and image is passed as a post parameter (multipart/form-data)
    `curl 192.168.122.134/upload/upload_file.php -F "image_file=@/trash/i217642.jpeg"`
    works fine and server replies with
    *File uploaded. Nothing happened.*
    - if we try to upload empty file with .php extension, we get
    *File is not an image.inode/x-empty*
    - from the response ending *inode/x-empty* we can guess that the php server uses some kind of php finfo_file() function to check the file information
    - if we try to upload text file with .php ending, we get subtly different error
    *File is not an image.text/plain*
    - if we try to put some magic numbers from another jpeg file, we get the flag
    `head -n 1 /trash/i217642.jpeg > abc.php; curl 192.168.122.134/upload/upload_file.php -F "image_file=@/home/jimmy/tmp/abc.php"`
    **Tajemstvi_I_82bdb89be1e4525da9de6c1f38e996452ab0c6c8842081f477601d15232b14d2**
- lastly we can see that the `/user.php?id=0` expects user id from get parameter and then probably fetches some users from database (we can see 4 valid users with ids from 0 to 3)
    - we can try to do a simple SQL OR injection - if the first part of query looks for the id, we can force it true with `OR 1=1` query
    - `curl 192.168.122.134/user.php?id=4'+OR+1=1'` (+ is url-encoded space)
    **Tajemstvi_H_fcc185f690980d2ed7e1c7c7e7cb425d6511be7dded8512625bc47c8c50f7d4e**

### 192.168.122.216 - bob

- password: MegaSuperHeslo123NikdoHoNezjisti
- `project/` directory contains some kind of binary file
    - the secret is hard-coded into the file
    - run `strings company_software | grep Tajemstvi`
    - **Tajemstvi_C_cd9b7eb8c0f73d6d51d97332bfc72064ec418efd2535eb8d3da7845a3a02b722**
- bunch of files but only file `mail.exported.txt` is being regularly updated by root every 5 minutes, so I assume I should do something about that file
    - is a GPG encrypted file so I need some kind of key to decrypt it .. maybe some other parts will help me later
    - printing out public-keys with GPG I found user `gpg --list-public-keys` so it is most likely from him and I need to find some kind of private key

    ```jsx
    pub   4096R/7C1568D6 2023-10-02
    uid                  John Seanah (My very SECRET key for my important SECRET stuff)
    sub   4096R/DEC00CBD 2023-10-02
    ```


### 192.168.122.249 - git

- tried to do git clone on that address with different project names
- found one using `git clone git://192.168.122.249/secret`
- contains single file: main.c with not much info but 2 suspicious looking variables
    - `const char *name_of_my_dog = "misbebeslosamocontodomicorazon";`
    - `const char *my_debit_card_pin = "4242";`
    - might be usefull later .. as I remeber someone from http having something about dogs in their profile (John Seanah)
    - the file was updated by Nobody [empty@empty.empty](mailto:empty@empty.empty)
- I tried to look for changes in each git commit using `git show COMMIT_ID`
    - +1) change my FTP password.. apparently "commonly used password" doesnt mean "safe password"
    +2) fix image upload - John managed to upload php script??? - reference to the HTTP server
    +3) done
    +4) clean the old pcap traffic files
    - `const char *login = "bob";`
    `const char *password = "iloveyou";`
    - **Tajemstvi_F_3478c34d69e2579ab175a81621b5e170138a94519a7cbc5bb47e870ba2c5a0c0**

### 192.168.122.164 - ftp

- installed ftp client on login server
- try to connect to ftp server .. only usernames root and admin are prompted for password
- after running `nmap -p 21 -A 192.168.122.164` I can see that there is no anonymous option
- write about how I found possible usernames by trying out different things like admin, root, nobody - each one returned password required after trying to log in at ftp
    - admin
    root
    nobody
- possible passwords were gathered from hints at git server
    - buster
    4242
    bebeslosamocontodomicorazon
    commonly used password
    safe password
    misbebeslosamocontodomicorazon
    iloveyou
- ran nmap script with ftp-brute to try different possibilites
    - `nmap --script ftp-brute --script-args userdb=usernames,passdb=passwords -p 21 192.168.122.164`
    - one username and password matches = admin:buster
- connected to ftp found secret Dktowcdfs_N_5nk2np1nkk087k1852m70op3n4026n80pl5okm39777nm159k2140393pn784o5o
    - since I know the secret is in form `Tajemstvi_…` I noticed it is encrypted using caesar cipher with offset 16 - decoded secret
    - used online site do decrypt message
    **Tajemstvi_D_5da2df1daa087a1852c70ef3d4026d80fb5eac39777dc159a2140393fd784e5e**
- also found 3 pictures of ducks which I have downloaded locally and inspected to try to find some more clues
    - trying out different pages … https://www.aperisolve.com/ found secret in duck-1.jpg image in Outguess section
    **Tajemstvi_E_cb474912685a598d9325bd4d4e3b88015e006582297cb0aa6802cb001302980c**

### 192.168.122.21 - nfs

- find mount point `showmount -e 192.168.122.21` show mountpoint `/shared 192.168.122.0/24`
- can not mount directly with sudo on login account … permissions denied
- create ssh tunnel to NFS server through jimmy
`ssh -fN -L 2080:192.168.122.21:2049 jimmy@192.168.122.60`
- then try to mount using this tunnnel
`sudo mount -t nfs -vvvv 127.0.0.1:/shared ./mnt/ -o nolock,port=2080`
- mount successfull - found many images … basic steganography with `strings *.jpg | grep Tajemstvi` and found secret
**Tajemstvi_J_18520ce28fd10f69f44ad3323e59781f9ee8ecb01ee24cd41519de1028d9fbd8**
- also found pairs of private and public keys to GPG (to the mail I found on bob server)
    - import private key using `gpg --import private.key`
    - decode message from bob server `gpg -d mail.exported.txt`
    **Tajemstvi_B_97e4d5bf078112cbb82b59fcc11a3d540c91188b5608235eb285b5ff7455f3c0**