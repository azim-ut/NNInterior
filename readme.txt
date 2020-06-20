# NNInterior
1. Step1GreyScale.ipynd - take all pictures from the imgSrc/ folder (JPG should be) as greyscale, resize images to 300x300 and save to /img folder
2. Step2SetPointsUI - run an UI to draw markers ot the ceiling on the images and save all changes to the answers.json file
    Controls:
      MouseClickRight - set point
      MouseClickLeft - remove last point
      Keys:
        arrows left/right: images pager
        Enter: save points
        Esc: exit
3. Step3Teaching - learning module. Take all images as an array, get the points arrays from answers.json and try to teach the NN. Based on https://www.youtube.com/watch?v=kft1AJ9WVDk
