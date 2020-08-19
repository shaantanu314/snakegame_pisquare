from PIL import Image

im = Image.open("apple.png")
resized_im = im.resize(( int(round(im.size[0]*0.3)), int(round(im.size[1]*0.3)) ))
resized_im.save('apple.png')
