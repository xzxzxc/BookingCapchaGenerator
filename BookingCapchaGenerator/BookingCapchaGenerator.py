from captcha.image import ImageCaptcha

image = ImageCaptcha(fonts=['NEON GLOW.otf'], width=140, height=60)
image.create_noise_dots = lambda x, a, b = None, c = None: x
image.create_noise_curve = lambda x, a: x


#data = image.generate('1234')
for i in range(0, 10):
    image.write('1234', str(i) + '.png')