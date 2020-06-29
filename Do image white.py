from PIL import Image


img = Image.open('data\\Sprites\\half.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] + item[1] + item[2] == 765:
        newData.append((255, 255, 255, 0))
    else:
        newData.append((0, 0, 0, 255))

img.putdata(newData)
img.save("data\\Sprites\\half.png", "PNG")