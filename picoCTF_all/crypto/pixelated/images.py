from PIL import Image
import numpy

i1 = Image.open('scrambled1.png')
i2 = Image.open('scrambled2.png')

res = []
for ((x1, x2, x3), (y1, y2, y3)) in zip(i1.getdata(), i2.getdata()):
    res.append((x1 ^ y1, x2 ^ y2, x3 ^ y3))

resc = []
for i in res:
    if i != (255, 255, 255):
        resc.append((0, 0, 0))
    else:
        resc.append((255, 255, 255))

res2 = numpy.array(resc).reshape(i1.size[1], i1.size[0], 3).astype(numpy.uint8)
i3 = Image.fromarray(res2)
i3.save('output.png')