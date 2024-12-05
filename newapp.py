from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pytesseract
from fpdf import FPDF
import numpy as num

file_path=''
detected=num.zeros((1024,768,3),num.uint8)

class imageProcessing:
    # binarization of image
    def greyscale(self,imge):
        return cv2.cvtColor(imge,cv2.COLOR_BGR2GRAY)

    def noise_removal(self,imge):
        import numpy as num
        # here we take matrix of 1,1 and filled with ones used 
        filled=num.ones((1,1), num.uint8)
        imge=cv2.dilate(imge,filled,iterations=1)
        filled=num.ones((1,1),num.uint8)
        imge=cv2.erode(imge,filled,iterations=1)
        imge=cv2.morphologyEx(imge,cv2.MORPH_CLOSE,filled)
        imge=cv2.medianBlur(imge,3)
        return (imge)
            
    def textToPDF(self,inputText):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf')
        pdf.set_font('DejaVu', size=10)
        pdf.multi_cell(w=0, h=6, text=inputText, align="J")
        pdf.output("Output/Output.pdf")


def select_file():
    filename = filedialog.askopenfilename(title="Select an Image",filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if filename:
        print("File selected:", filename)
        global file_path
        file_path=filename
        load_image(filename)

def load_image(filepath):
    global img, original_image, canvas
    img = Image.open(filepath)
    original_image = img.copy()  # Save the original image for resizing
    display_image()

def display_image():
    global img, original_image, canvas
    # Get the current canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Resize the image while maintaining its aspect ratio
    if original_image:
        img = original_image.copy()
        img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(img)

        # Clear the canvas and display the resized image
        canvas.delete("all")
        canvas.image = new_image  # Store the image reference
        canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=CENTER, image=new_image)
    

def imageToText():

    process=imageProcessing()
    global file_path

    # taking image into object
    imge=cv2.imread(file_path)

    # making inverted and saving it to temp folder
    inverted_image=cv2.bitwise_not(imge)
    cv2.imwrite('temp/first.jpg',inverted_image)

    # converting to greyscale and saving in temp
    grey_image=process.greyscale(imge)
    cv2.imwrite('temp/grey.jpg',grey_image)

    # using threshold method and thresh_binary is which method used for threshholding
    thresh,bw_img=cv2.threshold(grey_image,150,255,cv2.THRESH_BINARY)
    cv2.imwrite('temp/bw_image.jpg',bw_img)

    no_noise=process.noise_removal(bw_img)
    cv2.imwrite('temp/no_noise.jpg',no_noise)

    global detected
    detected=no_noise

    # pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    text=pytesseract.image_to_string(no_noise)
    # print(text)

    textfile=open('Output/output.txt','w')
    textfile.write(text)
    textfile.close()

    process.textToPDF(text)
    print("Both Files Are Ready")

def showDetected():
    global detected
    h, w =detected.shape
    boxes=pytesseract.image_to_boxes(detected)

    for b in boxes.splitlines():
        b=b.split(' ')
        no_noise=cv2.rectangle(detected,(int(b[1]),h-int(b[2])), (int(b[3]), h-int(b[4])), (0,255,0),2)

    cv2.imshow('Character Detected',detected)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showTextFile():
    import os
    imageToText()
    os.startfile('C:/Users/DELL/Desktop/MCA Sem1_project/Project/Output/Output.txt')

def showPDFFile():
    import os
    imageToText()
    os.startfile('C:/Users/DELL/Desktop/MCA Sem1_project/Project/Output/Output.pdf')


# Initialize the main application
if __name__ == '__main__':
    root = Tk()
    root.geometry("750x500")
    root.title('OCR Image To Text Converter')

    # Button to select an image
    select_button = Button(root, text='Select Image', command=select_file)
    select_button.pack()

    label=Label(text='Selected Image',font=('Arial',16,'bold'),foreground='red')
    label.pack()

    # Canvas to display the image
    canvas = Canvas(root, bg='gray')
    canvas.pack(fill=BOTH, expand=True)

    # Bind the window resize event to dynamically update the image
    canvas.bind("<Configure>", lambda event: display_image())

    original_image = None  # To store the original image for resizing
    img = None  # To store the current image being displayed

    detectedCharacters=Button(text='Show Detected Characters',command=showDetected)
    detectedCharacters.pack()

    convert_text=Button(text='Convert To Text',command=showTextFile)
    convert_text.pack()

    convert_pdf=Button(text='Convert To PDF',command=showPDFFile)
    convert_pdf.pack()

    root.mainloop()
