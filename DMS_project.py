import cv2
import numpy as np

cnt = 0
PI = 3.142
ix = 0
iy = 0
drawing = False
z = 1
relation = []
SET = []
list1 = []
list2 = []
c = 0
reflexive = False
antisymmetric = True
transitive = True

windowName = 'Drawing'
img = np.zeros((700, 700, 3), np.uint8)
cv2.namedWindow(windowName)

def find(x, y):
    for i in range(len(list1)):
        if list1[i] == x and list2[i] == y:
            return True
    return False

def search(x, y):
    for i in range(0, len(relation), 2):
        a=relation[i]-x
        b=relation[i+1]-y
        if (a*a + b*b) <= 1600:
            return (i+2)//2

def check_posset():
    global reflexive, transitive
    if(c == len(SET)):
        reflexive = True
        
    for i in range(0,len(list1)):
        for j in range(0,len(list2)):
            if (list2[i] == list1[j]):
                if(not find(list1[i], list2[j])):
                    transitive = False
                    break
        if transitive == False:
            break
    
    if reflexive == True and antisymmetric == True and transitive == True:
        return True
    return False

def create_node():
    cv2.setMouseCallback(windowName, draw_circle)
    
def creating_relation():
    cv2.setMouseCallback(windowName, draw_line)
    
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global z
        cv2.circle(img, (x, y), 30, (255, 0, 0), -1)
        relation.append(x)
        relation.append(y)
        cv2.putText(img,str(z), (x-20, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        z = z + 1
     
def draw_line(event, x, y, flags, param):   
    global cnt, PI, ix, iy, drawing, antisymmetric, c
    
    if event == cv2.EVENT_LBUTTONDOWN:
        a = search(x,y)
        cnt = cnt + 1
        global x1, y1
        if (cnt % 2) == 0:
            list2.append(a)
            cv2.arrowedLine(img,(x1,y1),(x,y),(255,255,255),2)
        else:
            x1, y1 = x, y
            list1.append(a)
            
    if event == cv2.EVENT_RBUTTONDOWN:
        antisymmetric = False
        a = search(x,y)
        cnt = cnt + 1
        if (cnt % 2) == 0:
            list2.append(a)
            list2.append(list1[len(list1)-1])
            list1.append(a)
            cv2.arrowedLine(img,(x1,y1),(x,y),(255,255,255),2)
            cv2.arrowedLine(img,(x,y),(x1,y1),(255,255,255),2)
        else:
            x1, y1 = x, y
            list1.append(a)
        
    if event == cv2.EVENT_MBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

    elif event == cv2.EVENT_MBUTTONUP:
        a = search(x,y)
        list1.append(a)
        list2.append(a)
        c = c + 1
        drawing = False
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)


def main():
    
    create_node() 
    
    while(True):
        cv2.imshow(windowName, img)
        if cv2.waitKey(20) == ord('s'):
            break
       
    for i in range(0, len(relation), 2):
        SET.append((i+2)//2)
    
    print("SET A = {" ,end = "")
    
    for i in range(len(SET)):
        if i == 0:
            print(SET[i], end = "")
        else:
            print(",", end = " ")
            print(SET[i], end = "")

    print("}")    
        
    creating_relation()

    while(True):
        cv2.imshow(windowName, img)
        if cv2.waitKey(20) == ord('q'):
            break
       
    print("R = {" ,end = "")
    for i in range(len(list1)):
        if i == 0:
            print("(" + str(list1[i]) + "," +str(list2[i]) + ")" ,end = "")
        else:
            print(" (" + str(list1[i]) + "," +str(list2[i]) + ")" ,end = "")
    
    print("}")
    
    if check_posset():
        print("R is a Partial Order(Posset)")
    else:
        print("R is not a Partial Order(not Posset)")
        
    while(True):
        cv2.imshow(windowName, img)
        if cv2.waitKey(20) == 27:
            break
        
    cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
