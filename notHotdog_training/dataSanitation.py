from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
from scipy.ndimage import imread
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D,Flatten
from os import rename, listdir
from keras.models import model_from_json

numberOfImages = 1000 
hotdogPath = "./hotdog/"
notHotdogPath = "./nothotdog/"
predictionPath = "./predictions/"
WIDTH = 250
HEIGHT = 250
mu = 0
std = 0
corruptHotDogImages = []


def resizeImage(path, numberOfImages):
    for i in range(0,numberOfImages+1):
        try:
            img = Image.open(f"{path}{i}.jpg")
            new_img = img.resize((WIDTH,HEIGHT))
            new_img.save(f"{path}{i}.jpg","JPEG")
            
        except:
            try:
                print(f"{i}.jpg failed")
                os.remove(path+str(i)+".jpg")
            except:
                pass

def reName(path):
    counter=0
    fname = listdir(path)
    print(fname)
    for j in fname:
        if(".jpg" not in j):
            os.remove(path+j)
    fname = listdir(path)
    for i in fname:
        while True:
            try:
                rename((path+str(i)),(path+str(counter)+".jpg"))
                counter+=1
                break
            except:
                counter+=1
    return counter



def createPredictionData():
    numberOfImages = reName(predictionPath)
    resizeImage(predictionPath, numberOfImages-1)
    print(numberOfImages)
    predictionImages = []
    for i in range(0,numberOfImages):
        try:
            img = img_to_array(load_img(predictionPath+f"{i}"+".jpg"))
            predictionImages.append(img)
        except:
            pass
    predictionImages = np.array(predictionImages)
    predictionImages = normalize(predictionImages)

    print(model.predict_classes(predictionImages))

def createTrainingAndTestingData():
    hotdogImages = []
    for i in range(0,numberOfImages):
        try:
            img = img_to_array(load_img(hotdogPath+f"{i}"+".jpg"))

            hotdogImages.append(img)
        except:
            corruptHotDogImages.append(i)
            print(f"{i}.jpg could not be read")
    hotdogImages = np.array(hotdogImages)
    corruptNotHotDogImages = []
    
    notHotdogImages = []

    for i in range(0,numberOfImages):
        try:
            img = img_to_array(load_img(notHotdogPath+f"{i}"+".jpg"))
            
            notHotdogImages.append(img)
        except:
            corruptNotHotDogImages.append(i)
            print(f"{i}.jpg could not be read")
    
    notHotdogImages = np.array(notHotdogImages)
 
    

    print("notHotdogImages len:",len(notHotdogImages),"  notHotdogImages shape:",np.shape(notHotdogImages))
    print("hotdogImages len",len(hotdogImages),"  hotdogImages shape:",np.shape(hotdogImages))
    hotdogImagesLabels=np.array([])
    print("hotdog image shape",np.shape(hotdogImages))
    hotdogImagesLabels = np.ones((993,1))
    notHotdogImagesLabels = np.zeros((998,1))
    images = normalize(np.concatenate((hotdogImages,notHotdogImages),axis=0))
    labels = np.concatenate((hotdogImagesLabels,notHotdogImagesLabels),axis=None)
    print("images shape",np.shape(images))
    images_train = images[90:]
    labels_train = labels[90:]
    images_test = images[0:90]
    labels_test = labels[0:90]
    print("len(images_train)",len(images_train))
    print("len(images_test)",len(images_test))
    return images_train, labels_train, images_test, labels_test

    


def normalize(x_train):
    #try:
    #    x_train_normalized = (x_train - mu) / std
    #except:
    #    mu = np.mean(x_train, axis=0)
    #    std = np.std(x_train, axis=0)
    #    x_train_normalized = (x_train - mu) / std
    x_train_normalized = x_train/255
    #mu = np.mean(x_train, axis=0)
    #std = np.std(x_train, axis=0)
    #x_train_normalized = (x_train - mu) / std
    #print("mu,std:",mu,std)
    return x_train_normalized
    


def createModel():
    model = Sequential()
    model.add(Conv2D(32,(3,3), input_shape=(250,250,3),activation='relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(32, 3, 3, activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Flatten())
    model.add(Dense(units = 128, activation = 'relu'))
    model.add(Dense(units = 1, activation = 'sigmoid'))
    model.compile(optimizer = 'adam',
    loss = 'binary_crossentropy',
    metrics = ['accuracy'])
    return model

def fitModel():
    model.fit(images_train, labels_train,batch_size=64, epochs=7, verbose=1)
    print(model.evaluate(images_test,labels_test, verbose=1, batch_size = 32))

def saveModel():
    json_file = open("model.json","w")
    json_file.write(model.to_json())
    model.save_weights("model.h5")
    json_file.close()

def openModel():
    jsonFile = open("model.json","r")
    model = model_from_json(jsonFile.read())
    model.load_weights("model.h5")
    jsonFile.close()
    return model

images_train, labels_train, images_test, labels_test = createTrainingAndTestingData()
model = createModel()

fitModel()
#saveModel()

#model = openModel()

createPredictionData()