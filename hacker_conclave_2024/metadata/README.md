# Description

In this challenge, the flag has been hidden inside one of the images on the website. Will you be able to find it?

# Solution

Look around the website, which displays 4 images when loaded. After refreshing the website we can see, that
there is probably an image database, from which 4 images are randomly picked. After fuzzing for the number of images I managed
to find that there are 20 images in total.

Use simple bash script to download all the images:
```bash
for p in {1..20}; do
    wget http://ctf.thehackerconclave.es:20002/images/$p.jpg
done
```

Use `strings` to find the flag in the images:
```bash
strings * | grep conclave
```

which returns `conclave{b89279bf984e1d6dde9823a8edea6600}`