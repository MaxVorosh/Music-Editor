from PIL import Image

img = Image.open('data\\Sprites\\bass.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[3] != 0:
        newData.append((0, 0, 0, 255))
    else:
        newData.append(item)

img.putdata(newData)
img.save("data\\Sprites\\bass_black.png", "PNG")