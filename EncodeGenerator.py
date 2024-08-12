import os
import pickle

import cv2
import face_recognition

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://facedetectionrealtime-da3fb-default-rtdb.firebaseio.com/",
                                    "storageBucket":"facedetectionrealtime-da3fb.appspot.com"})



pathImg='Images'
modePathList=os.listdir(pathImg)
imagesList=[]
#print(modePathList)
studentIds=[]
for path in modePathList:
    imagesList.append(cv2.imread(os.path.join(pathImg,path)))
    studentIds.append(os.path.splitext(path)[0])


    fileName = f'{pathImg}/{path}'
    print(fileName)
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)
#print(studentIds)



def findEncodings(imagesList):
    encodingList = []
    for img in imagesList:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)
        encodingList.extend(encode)
    return encodingList

print("Encoding Started...")
encodeListKnown=findEncodings(imagesList)
print(encodeListKnown)
encodeListWithIds=[encodeListKnown,studentIds]
print("Encoding complete....")

file=open("EncodedFile.p","wb")
pickle.dump(encodeListWithIds,file)
file.close()
print("Encoded file saved")


