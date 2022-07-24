import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#### 1 - Preprocessing Image
def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)  # APPLY ADAPTIVE THRESHOLD
    return imgThreshold


#### 2 - Reorder points for Warp Perspective
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


#### 3 - FINDING THE BIGGEST COUNTOUR ASSUING THAT IS THE SUDUKO PUZZLE
def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area


#### 4 - TO SPLIT THE IMAGE INTO 81 DIFFRENT IMAGES
def splitBoxes(img):
    rows = np.vsplit(img,9)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,9)
        for box in cols:
            boxes.append(box)
    return boxes


#### 4 - GET PREDECTIONS ON ALL IMAGES
def getPredection(boxes):
    result = []
    for image in boxes:
        image = image[4:image.shape[0]-4, 4:image.shape[1]-4]
        thr = cv2.threshold(src=image, thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        text = pytesseract.image_to_string(thr, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').rstrip()
        if text == '':
            result.append('-')
        else:
            result.append(text.rstrip())
    return result