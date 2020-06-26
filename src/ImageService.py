import numpy as np
from PIL import Image
from pathlib import Path
from os import listdir
from os.path import isfile, join


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
        
    def resizeTo(self, sourceFolder, targetFolder, width, height):
        self.sourceFolder = sourceFolder
        self.targetFolder = targetFolder
        self.width = width
        self.height = height
        
        onlyfiles = [f for f in listdir(self.sourceFolder) if isfile(join(self.sourceFolder, f))]
        for file in onlyfiles:
            pathFrom = join(self.sourceFolder, file)
            pathTo = join(self.targetFolder, file)
            if Path(pathTo).is_file():
                continue
            else:
                img = Image.open(pathFrom).convert('RGB')
                new_img = self.normalize(np.array(img))
                new_img = Image.fromarray(new_img.astype('uint8'))
                new_img = new_img.resize((self.width, self.height), Image.ANTIALIAS)
                new_img.save(pathTo)