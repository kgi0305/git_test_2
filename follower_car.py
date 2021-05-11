import cv2
import dc_motor as motor

# Set the color recognition range
# If you want a different color, change it.(Blue)
Color_Lower = (36,130,46)
Color_Upper = (113, 255, 255)

# Camera Frame Range and Setting
Frame_Width  = 320
Frame_Height = 240
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,  Frame_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Frame_Height)

try:
    while True:
        (_, frame) = camera.read()
        frame = cv2.GaussianBlur(frame,(11,11),1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, Color_Lower, Color_Upper)
        _, contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                if radius < 25 and radius > 5 :
                    if center[0] > Frame_Width/2 + 55 :
                        motor.turnRight()
                        
                    elif center[0] < Frame_Width/2 -55 :
                        motor.turnLeft()
                    else:
                        motor.forward_2()
                elif radius < 45 and radius > 25 :
                    if center[0] > Frame_Width/2 + 55 :
                        motor.turnRight()
                    elif center[0] < Frame_Width/2 -55 :
                        motor.turnLeft()
                    else:
                        motor.forward_1()
                elif radius > 65:
                    motor.Reverse()
                else:
                    motor.brake()
                    
            except:
                pass
        else:
            motor.stop()
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("q"):
                break
      

finally:
    motor.cleanup()
    camera.release()
    cv2.destroyAllWindows()


