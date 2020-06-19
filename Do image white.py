from PIL import Image

img = Image.open('data\\Sprites\\bass.jpg')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[3] != 0:
        newData.append((255, 255, 255, 255))
    else:
        newData.append(item)

img.putdata(newData)
img.save("data\\Sprites\\bass.png", "PNG")