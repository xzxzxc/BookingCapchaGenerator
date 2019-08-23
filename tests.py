from PIL import Image

img = Image.open("captcha.gif")
rgb_im = img.convert('RGB')

arr = []
arr3 = []
dist = []

for x in range(0, rgb_im.size[0]):
    arr2= []
    for y in range(0, rgb_im.size[1]):
        r, g, b = rgb_im.getpixel((x, y))
        arr2.append((r, g, b))
        arr3.append(arr2[-1])
        if not r in dist:
            dist.append(r)
        if not g in dist:
            dist.append(g)
        if not b in dist:
            dist.append(b)
    arr.append(arr2)


if True:
    pass