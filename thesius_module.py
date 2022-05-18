import cv2
import  mediapipe as mp#21 landmarks for a hand/palm
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,model_complexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.model_complexity=model_complexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,frame,draw=True):
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRGB)
        
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self,frame,handNo=0,draw=True):

        lmList=[]
        if self.result.multi_hand_landmarks:
            myHand=self.result.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),6,(0,0,0),cv2.FILLED)

        return lmList



def main():
    cap=cv2.VideoCapture(0)
    detector=handDetector()
    
    pTime=0
    cTime=0

    while True:
        ok,frame=cap.read()
        frame=detector.findHands(frame)

        lmList=detector.findPosition(frame)
        if len(lmList)!=0:
            print(lmList[4])

       
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(frame,str(int(fps)),(18,78),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)


        cv2.imshow('Hand',frame)
        key=cv2.waitKey(1)
        if key==ord('q'):
            break
        
if __name__=='__main__':
    main()
    
