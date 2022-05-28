# CPS3320_Aurora-Melantha
Before running the program, you need to change the parameter range in the range function in line 80 and the location of the image data set in line 81 according to the license plate image to be processed in the computer.
In the unchanged state, the default image dataset location is D:\Finalpython\image, each image is named test plus its own number, such as test1, test2, etc., and the image format is in png format. At the same time, there are 10 images in the image folder, named from 1 to 10.
Before running the program, it is also necessary to change the txt file location where line 83 is not deleted and used to store the image recognition results during query operations, and the txt file location where line 105 is deleted and used to re-store the results after query operations.
In the unmodified state, the image recognition result is stored in D:/Finalpython/car_plate_recognization.txt by default. After deletion, the result of the query operation is stored in D:/Finalpython/new_car_plate_recognization.txt.

Delete, query operation: The user can exit the system only when entering 0, otherwise the delete (which is 1) or search (which is 2) operation will continue to be performed on the image recognition result according to the user's input. When entering a number other than 0, 1, or 2, the system will display an input error and require the user to re-enter until the value is 0, 1, or 2.
