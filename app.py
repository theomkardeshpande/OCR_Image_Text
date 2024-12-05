import cv2
import pytesseract
from fpdf import FPDF
# import os
# import guiInterface


# guiInterface.selectFile()
# image file path
file_path='Testing/typewritten.jpeg'

# taking image into object
img=cv2.imread('Testing/typewritten.jpeg')

# making inverted and saving it to temp folder
inverted_image=cv2.bitwise_not(img)
cv2.imwrite('temp/first.jpg',inverted_image)

# binarization of image
def greyscale(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# converting to greyscale and saving in temp
grey_image=greyscale(img)
cv2.imwrite('temp/grey.jpg',grey_image)

# using threshold method and thresh_binary is which method used for threshholding
thresh,bw_img=cv2.threshold(grey_image,150,255,cv2.THRESH_BINARY)
cv2.imwrite('temp/bw_image.jpg',bw_img)


def noise_removal(img):
    import numpy as num
    # here we take matrix of 1,1 and filled with ones used 
    filled=num.ones((1,1), num.uint8)
    img=cv2.dilate(img,filled,iterations=1)
    filled=num.ones((1,1),num.uint8)
    img=cv2.erode(img,filled,iterations=1)
    img=cv2.morphologyEx(img,cv2.MORPH_CLOSE,filled)
    img=cv2.medianBlur(img,3)
    return (img)

no_noise=noise_removal(bw_img)
cv2.imwrite('temp/no_noise.jpg',no_noise)

# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
text=pytesseract.image_to_string(no_noise)
print(text)

textfile=open('Output/output.txt','w')
textfile.write(text)
textfile.close()

def textToPDF(inputText):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
    pdf.set_font('DejaVu', size=10)
    pdf.multi_cell(w=0, h=6, text=inputText, align="J")
    pdf.output("Output/Output.pdf")
textToPDF(text)


