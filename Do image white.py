from PIL import Image


img = Image.open('data\\Sprites\\rules.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] + item[1] + item[2] >= 700:
        newData.append((255, 255, 255, 0))
    else:
        newData.append((255, 255, 255, 255))

img.putdata(newData)
img.save("data\\Sprites\\rules.png", "PNG")