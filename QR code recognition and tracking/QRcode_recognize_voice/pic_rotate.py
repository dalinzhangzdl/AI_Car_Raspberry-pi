import cv2

img = cv2.imread('qrcode.jpg',0)

rows, cols = img.shape

M = cv2.getRotationMatrix2D((cols/2, rows/2), 120, 1)

dst = cv2.warpAffine(img, M, (cols, rows))

cv2.imwrite('dst.jpg', dst)

cv2.imshow('image', img)
cv2.imshow('dst', dst)
cv2.waitKey(0)
