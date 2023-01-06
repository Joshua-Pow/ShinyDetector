from re import T
import cv2
import numpy as np
import time
import keyboard

def configCamera(x, y):
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        frame[y-2:y+2, x] = [255, 0, 0]
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
    cam.release()
    cv2.destroyAllWindows()

#set cam as the opencv_frame_0.png
#frame = cv2.imread('test2.png')
#configCamera(637, 295)
cam = cv2.VideoCapture(0)

#cam.set(15, -2.0)

#Pixels of pokemon to check on spawn
pokemonPixel_X = 242
pokemonPixel_Y = 260

#pixel to check to see if on battle screen
rightScreenPixel_X = 637
rightScreenPixel_Y = 295

lower_pink = np.array([130, 100, 50])
upper_pink = np.array([185, 255, 255])

# lower_red1 = np.array([120, 100, 50])
# upper_red1 = np.array([179, 255, 255])
lower_red2 = np.array([0, 130, 111])
upper_red2 = np.array([11, 255, 255])
cv2.namedWindow("test")
# cv2.namedWindow("test2")
# cv2.namedWindow("test3")

img_counter = 0
done = False

while True:
    ret, frame = cam.read()
    #frame = cv2.imread('spawn_649.png')

    frame = cv2.GaussianBlur(frame, (1,3), 0) #might not need

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2) #+ cv2.inRange(hsv, lower_red1, upper_red1)
    frameClean = frame #dupe of frame without pixels on it

    #draw a pixel line where we look for the shiny colour
    #frame[pokemonPixel_Y, pokemonPixel_X-5:pokemonPixel_X+5] = [255, 0, 0]

    #Result of where the red button is and where the shiny is
    res = cv2.bitwise_and(frame, frame, mask=mask) #Shiny
    res2 = cv2.bitwise_and(frame, frame, mask=mask2) #Red button

    #displays everything
    cv2.imshow("test", frame) #original frame
    cv2.imshow("test2", res) #shiny colours
    cv2.imshow("BattleButton", mask2) #The mask for battle button
    #cv2.imshow("ShinyWindow", mask) #The mask for shiny

    #were on battle screen because the pink battle button is on the screen
    if np.all(mask2[rightScreenPixel_Y-2:rightScreenPixel_Y+2, rightScreenPixel_X] != 0):
        #save the frame as a png and apply a frame for the colours
        cv2.imwrite("spawn.png", frameClean)
        shinyFrame = cv2.imread('spawn.png')
        shinyFrame = cv2.GaussianBlur(shinyFrame, (1,3), 0) #might not need
        hsv = cv2.cvtColor(shinyFrame, cv2.COLOR_BGR2HSV)
        shinyMask = cv2.inRange(hsv, lower_pink, upper_pink)
        cv2.imshow("ShinyWindow", shinyMask) #Show the mask for the shiny
        cv2.imwrite("shinyMask.png", shinyMask) #Save the shiny frame

        for i in range(-4, 4):
            print("Mask value: " + str(shinyMask[pokemonPixel_Y, pokemonPixel_X+i]))
            if shinyMask[pokemonPixel_Y, pokemonPixel_X+i] != 0:
                print("shiny pokemon!")
                done = True
                break

        if not done:
            img_counter += 1
            print("Attempts: " + str(img_counter))
            #print the current time
            print("time: " + time.strftime("%H:%M:%S"))
            img_name = "spawn_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            keyboard.write("sudo nxbt macro -c \"restart.txt\" -r")
            keyboard.press_and_release('enter')
            time.sleep(14)
            keyboard.write("sudo nxbt macro -c \"commands.txt\" -r")
            keyboard.press_and_release('enter')
            time.sleep(120)
        if done:
            break
                    

    # k = cv2.waitKey(1)
    # if k%256 == 27:
    #     # ESC pressed
    #     print("Escape hit, closing...")
    #     break
    # elif k%256 == 32:
    #     # SPACE pressed
    #     img_name = "opencv_frame_{}.png".format(img_counter)
    #     cv2.imwrite(img_name, frame)
    #     print("{} written!".format(img_name))
    #     img_counter += 1

cam.release()

cv2.destroyAllWindows()


    