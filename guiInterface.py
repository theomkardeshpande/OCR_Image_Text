from tkinter import *     # from tkinter import Tk for Python 3.x
from tkinter import filedialog
from PIL import ImageTk,Image

def selectFile():
    filename=filedialog.askopenfilename() 
    print("File is Selected")
    return filename

# def selectFile():
#     root=Tk()
#     root.withdraw() # we don't want a full GUI, so keep the root window from appearing
#     root.title("Select Fil")
#     filename = askopenfilename() 
#     # show an "Open" dialog box and return the path to the selected file
#     # print(filename)
#     print("File is Selected")


# def selectFile(root):
#     root.withdraw()
#     root.title('Selection Window')
#     filename=askopenfilename()
#     print(filename)
#     print("File is Selected")
# global filepath

root=Tk()
root.title("OCR Image To Text Converter")
select_button=Button(text='Select Image',command=selectFile)
select_button.pack()
filepath=select_button.invoke()

img=Image.open(filepath)
width,height=img.size
resized=img.resize(height,width)

image=ImageTk.PhotoImage(resized)
img_label=Label(root,image=image)
img_label.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()



