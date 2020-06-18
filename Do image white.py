from PIL import Image

img = Image.open('data\\Sprites\\add.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == item[1] == item[2] and item[0] < 100:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("data\\Sprites\\add_1.png", "PNG")