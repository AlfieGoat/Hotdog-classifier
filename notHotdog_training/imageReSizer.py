from PIL import Image
import os
def resizeImage(path, numberOfImages):
    for i in range(0,numberOfImages+1):
        try:
            img = Image.open(f"{path}{i}.jpg")
            new_img = img.resize((250,250))
            new_img.save(f"{path}{i}.jpg","JPEG")
            
        except:
            try:
                print(f"{i}.jpg failed")
                os.remove(path+str(i)+".jpg")
            except:
                pass
resizeImage("C:/Users/alfre/Desktop/notHotdog/nothotdog/",1350)