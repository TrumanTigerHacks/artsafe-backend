from PIL import Image
from io import BytesIO
import base64


im = Image.open("ggg.png")

buffered = BytesIO()

im.save(buffered, format="PNG")

img_str = base64.b64encode(buffered.getvalue())

file = open("testb64", "w")
file.write(img_str.decode('utf-8'))
file.flush()
file.close()
