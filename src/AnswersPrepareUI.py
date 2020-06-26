import cv2
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
from os import listdir
from os.path import isfile, join
import pandas as pd
import json

class UI():
    ANSWERS = []
    POINTS = []
    SRC = None
    imgFolder = None
    window = None
    answerFile = None
    
    def __init__(self, window, imgFolder, answerFile):
        self.window = window
        self.imgFolder = imgFolder
        self.answerFile = answerFile
        return None
    
    def updatePoint(self, event,x,y,flags,param):
        if event > 0:
            if event == 1:
                self.POINTS.append([x,y])
                self.drawImage()
            if event == 2:
                if len(self.POINTS)> 0:
                    self.POINTS.pop(len(self.POINTS)-1)
                    self.drawImage()

    def drawImage(self):
        image = self.SRC.copy()
        draw = ImageDraw.Draw(image)
        for point in self.POINTS:
            x = point[0]
            y = point[1]
            r = 5
            draw.ellipse((x-r, y-r, x+r, y+r), fill=(0,0,255,0))
        self.displayOnCV2(image)

    def saveSeiling(self, file):
        saved = False
        for row in self.ANSWERS:
            if row['file'] == file:
                saved = True
                row['points'] = self.POINTS
        if saved == False:
            self.ANSWERS.append({
                'file': file,
                'points': self.POINTS
            })
        with open(self.answerFile, 'w') as json_file:
            json.dump(self.ANSWERS, json_file)

    def displayOnCV2(self, image):
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imshow(self.window,image)

    def openImage(self, file):
        self.POINTS = []
        for asw in self.ANSWERS:
            if asw['file'] == file:
                self.POINTS = asw['points']

        path = join(self.imgFolder, file)
        self.SRC = Image.open(path)
        cv2.setMouseCallback(self.window, self.updatePoint)
        self.drawImage()

    def run(self):
        self.SRC = np.zeros((512,512,3), np.uint8)
        IND = 0
        with open(self.answerFile) as json_file:
            self.ANSWERS = json.load(json_file)

        images = [f for f in listdir(self.imgFolder) if isfile(join(self.imgFolder, f))]
        cv2.namedWindow(self.window)

        while True:
            key = cv2.waitKeyEx(0)
            if key == 13: # back
                self.saveSeiling(images[IND])
                IND += 1
                if IND > (len(images)-1):
                    IND = 0
            if key == 2424832: # back
                IND -= 1
                if IND < 0:
                    IND = len(images)-1
            if key == 2555904: # forward
                IND += 1
                if IND > (len(images)-1):
                    IND = 0
            if key == 27: break # 'ESC'
            self.openImage(images[IND])
        cv2.destroyAllWindows()