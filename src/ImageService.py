import numpy as np
from PIL import Image
from pathlib import Path
from os import listdir
from os.path import isfile, isdir, join, exists
import json


class ImageService():
    width = 0
    height = 0
    sourceFolder = None
    targetFolder = None
    
    def __init__(self):
        return None
    
    def normalize(self, arr):
        #Linear normalization http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
        arr = arr.astype('float')
        # Do not touch the alpha channel
        for i in range(3):
            minval = arr[...,i].min()
            maxval = arr[...,i].max()
            if minval != maxval:
                arr[...,i] -= minval
                arr[...,i] *= (255.0/(maxval-minval))
        return arr
    
    def parseAnswer(self, dataFile):
        data = None
        res = []
        with open(dataFile) as f:
            data = json.load(f)
            for ind in data['_via_img_metadata']:
                row = data['_via_img_metadata'][ind]
                obj = {
                        'file': row['filename'],
                        'points': []
                    }
                for region in row['regions']:
                    x = 0
                    y = 0
                    for i, x in enumerate(region['shape_attributes']['all_points_x']):
                        x = x
                        y = region['shape_attributes']['all_points_y'][i]
                        obj['points'].append([x, y])
                res.append(obj)
        return res
        
    def answers(self, saveToFile):
        dirs = [f for f in listdir(self.sourceFolder) if isdir(join(self.sourceFolder, f))]
        res = {
            'list':[],
            'width': self.width,
            'height': self.height
        }
        for dir in dirs:
            dataFile = join(self.sourceFolder, dir, "data.json")
            if exists(dataFile):
                arr = self.parseAnswer(dataFile)
                res['list'].append(arr)
        with open(saveToFile, 'w') as json_file:
            json.dump(res, json_file)
            
        return self
        
        
    def resizeTo(self, sourceFolder, targetFolder):
        self.sourceFolder = sourceFolder
        self.targetFolder = targetFolder
        
        dirs = [f for f in listdir(self.sourceFolder) if isdir(join(self.sourceFolder, f))]
        for dir in dirs:
            dataFile = join(self.sourceFolder, dir, "data.json")
            if exists(dataFile):
                files = [f for f in listdir(join(self.sourceFolder, dir)) if isfile(join(self.sourceFolder, dir, f))]
                for file in files:
                    pathFrom = join(self.sourceFolder, dir, file)
                    pathTo = join(self.targetFolder, file)
                    if pathFrom == dataFile:
                        continue
                    if Path(pathTo).is_file():
                        continue
                    else:
                        img = Image.open(pathFrom).convert('RGB')
                        new_img = Image.fromarray(new_img.astype('uint8'))
                        width, height = img.size
                        if width>self.width:
                            self.width = width
                        if height>self.height:
                            self.height = height
                        new_img.save(pathTo)
        return self