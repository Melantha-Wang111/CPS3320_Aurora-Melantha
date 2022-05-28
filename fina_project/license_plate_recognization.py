import json
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Answer to the question list:

# Q3: if the part begins with "# Personally written", it means this part is coded by ourselves and others are imported from other resources.

# Q4: Data Preprocessing
#       Before we put the image into the program, we select images of the licence plate, which has normal shape as a rectangle. Hence, we randomly select 10 iamges from the google image abd sent to the program to get the recognization result. 

# Q5: list of websites used in coding：
#       Usage for cv2 function: https://www.geeksforgeeks.org/python-opencv-cv2-imshow-method/
#       Find cooordinates of contours using opencv: https://www.geeksforgeeks.org/find-co-ordinates-of-contours-using-opencv-python/
#       Usage for pytesseract function: https://nanonets.com/blog/ocr-with-tesseract/

# Q6: Accuracy: Based on the accuracy of each image after recognition, we calculated an average accuracy of the dataset is 72.89%

def det_recog(path):
    # PART1: Licence Plate Detection
    # STEP1: Adjust image size and grayscale operation
    pic = cv2.imread(path)   #read image from corresponding path
    pic = cv2.resize(pic, (620,480)) 
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

    # STEP2: Bilateral filtering denoising
# Personally written
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    # STEP3: Border detection
# Personally written
    edged = cv2.Canny(gray, 30, 200) 

    # STEP4: Look for the license plate outline
    contours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find and return countours
    contours = imutils.grab_contours(contours) #return countours, used with findContours()
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10] #Sort by area size from smallest to largest, considering only the first 10 results
    screenCnt = None

    for c in contours:
        # approximate the contour
        peri = cv2.arcLength(c, True) # Calculated the length of contour; sec para: point out whether the curve is closed
        approx = cv2.approxPolyDP(c, 0.018 * peri, True) # Approximates polygonal curves with the specified precision
        
        # if the approximated contour has four points, then it's possible to assume that the screen is found
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print ("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(pic, [screenCnt], -1, (0, 0, 255), 3) # draw new counters; originImg, counter; pythonList; counterIndex

    # STEP5: Using mask method to get only the License plate part
    mask = np.zeros(gray.shape,np.uint8) #Returns an array of zeros with the given shape and type
    pic_mask = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    pic_mask = cv2.bitwise_and(pic,pic,mask=mask)# Implement bitwise AND operations

    # PART2: Split License Plates and Identify
    # STEP1: Get position
    (x, y) = np.where(mask == 255) # when counter == 255, return each(x,y) coordinates as tuple
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    # STEP2: Gray processing + positioning edge
    pic_tailor = gray[topx:bottomx+1, topy:bottomy+1]

    # # PART3: Character Recognition
    text = pytesseract.image_to_string(pic_tailor, config='--psm 11') # Extracts characters from the picture
    result = text[:-1]
    return result

# store the result of recognization into dictionary
# Personally written
result = {}
try:
    position = str(input("Please input the position of image files: "))
except:
    print("Invalid position, which should be string")
    
for i in range(1,11):
    path = r'' + position + str(i) + ".png"
    result[i] = det_recog(path)
    f = open('D:/Finalpython/car_plate_recognization.txt','a')
    f.write(str(i) + ": " + result[i])
    f.close()
print("Finish Recognization! Please check the file.")

# delete & search function
# Personally written
operation = int(input("Any operation? 1 for delete, 2 for search, 0 for exit: "))
new_result = {}
while(operation != None):
    # delete function
    if operation == 1:
        order_number = int(input("Enter the order number that you want to delete: "))
        new_result = result
        new_result.pop(order_number)
        print("The content now is ")
        print(new_result)
        print("Would you like to restore the result again")
        restore = int(input("1 for yes, 2 for no: "))
        while(restore != None):
            # restore the result
            if restore == 1:
                f = open('D:/Finalpython/new_car_plate_recognization.txt','a')
                f.write(json.dumps(new_result) + "\n")
                print("Finish Storing. Please check the new file")
                f.close()
                break
            # not to restore
            elif restore == 2:
                break
            else:
                restore = int(input("Invalid input. Input again"))
                continue
        operation = int(input("Any operation? 1 for delete, 2 for search, 0 for exist: "))
        continue
    # search function
    elif operation == 2:
        new_result = {v : k for k, v in result.items()}
        search = str(input("Enter the content you want to search: "))
        print(new_result.get(search))
        new_result = {v : k for k, v in new_result.items()}
        operation = int(input("Any operation? 1 for delete, 2 for search, 0 for exit: "))
        continue
    # exsit the system
    elif operation == 0:
        print("See you~")
        break
    # wrong input
    else:
        operation = int(input("Invalid input. Input again: "))
        continue

print("System closed")

