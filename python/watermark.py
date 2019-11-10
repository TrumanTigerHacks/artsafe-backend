# Import QR Code library
import qrcode

# Create qr code instance
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)

# The data that you want to store
data = "truman.edu"

# Add data
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img3 = qr.make_image()

# Save it somewhere, change the extension as needed:
# img.save("image.png")
# img.save("image.bmp")
# img.save("image.jpeg")
img3.save("image1.jpg")

from PIL import Image
#import Qrcode


def main():
    try:
        #Relative Path
        #Image on which we want to paste
        img = Image.open("265.png")

        #Relative Path
        #Image which we want to paste
        img2 = Image.open("Logo2.png")
        img.paste(img2, (0,0), img2)

        #QR Code
        imgSize = img.getbbox()
        qrSize = img3.getbbox()

       # print(imgSize[0]+",")
       # print(imgSize[1]+",")
       # print(imgSize[2]+",")
        #print(imgSize[3]+",")

        img.paste(img3,(imgSize[2]-qrSize[2],imgSize[3]-qrSize[3]), img3)

        #Saved in the same relative location
        img.save("pasted_picture.png")


    except IOError:
        pass

if __name__ == "__main__":
    main()

##An additional argument for an optional image mask image is also available.

