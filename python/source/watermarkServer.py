'''
This program implements the Flask webservice package to establish a small
webserver which composites images together and returns them
@author Harsh Shahi, Cameron Krueger, Sam Vaclavik
@created Nov 9, 2019
'''

import qrcode
from flask import Flask, escape, request
from PIL import Image
import json
import base64
import os, sys
from io import BytesIO
from string import Formatter

def addLogo(baseImg, logoImg):
    '''
    Overlays a logo in the top left of an image
    @param baseImg the image to which a logo should be applied
    @param logoImg the image being applied as a logo
    @return a PIL image based on baseImg, but modified to include the supplied
        logoImg logo image
    '''

    # Overlay logo at top left of image
    baseImg.paste(logoImg, (0,0), logoImg)
    return baseImg


def addQR(baseImg, qrImg):
    '''
    Overlays a QR code in the bottom right corner of an image
    @param baseImg the image to which a QR code should be applied
    @param qrImg the image being applied as a QR code
    @return a PIL image based on baseImg, but modified to include the supplied
        qrImg QR code image
    '''

    # Get dims
    imgSize = baseImg.getbbox()
    qrSize = qrImg.getbbox()
    baseImg.paste(qrImg,(imgSize[2]-qrSize[2],imgSize[3]-qrSize[3]), qrImg)
    return baseImg


def generateQR(contentString):
    '''
    Generates a QR code image from a provided string
    @param contentString the string to be QR encoded
    @return a PIL image containing a QR endoding of the provided string
    '''

    # Create qrcode instance
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )

    # Add data to qrcode object
    qr.add_data(contentString)
    qr.make(fit=True)

    # Create and return a PIL image from the QR Code instance
    return qr.make_image()


# Make Flask app
app = Flask(__name__)

@app.route('/')
def genImage():
    '''
    Generates a composite image consisting of a base image overlayed with a
    logo and a QR code, from data provided in the request
    '''

    # Initialize a dictionary with parsed JSON key/value pairs
    #body = json.loads(request.json())
    body = request.json

    # Get link to be QR encoded from request body
    link = body["link"]

    # Load logo from local
    logoImg = Image.open('artsafe_logo.png')

    # Get image from request body
    baseImg = Image.open(BytesIO(base64.b64decode(body["image"])))

    # A useful comment was supposed to go here,
    #  but it's 4:30 in the morning and the wall to my
    #  left keeps turning into a hallway

    # Generate QR
    qrImg = generateQR(link)

    # Generate base and logo composite image
    baseLogoComp = addLogo(baseImg, logoImg)

    # Generate base and QR composite
    baseQRComp =  addQR(baseLogoComp, qrImg)

    buffered = BytesIO()

    baseQRComp.save(buffered, format='PNG')
    
    retVal = base64.b64encode(buffered.getvalue())

    retString = "{{\"image\": \"{}\"}}".format(retVal.decode('utf-8'))

    return retString

