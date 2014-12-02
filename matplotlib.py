import cv
import cv2


if __name__ == '__main__':
    
    
    
    img1 = cv2.imread('cph.png')
    img2 = cv2.imread('cph.png')
    
    (h,w) = img1.shape[:2]
    
    center = (w/2,h/2)
    
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    
    rotated = cv2.warpAffine(img1, M, (w,h))
    cv2.imshow('rotated', rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    #cv2.imshow('dst',dst)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()