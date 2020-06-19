from PIL import Image

img = Image.open('data\\Sprites\\old.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[1] == 0:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("data\\Sprites\\old.png", "PNG")