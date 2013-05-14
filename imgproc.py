##########################
## Image Processing Module
##########################


import numpy
import cv

##Color Class
class Color(object):
    pass

color=Color()
color.RED=(0,0,255,0)
color.GREEN=(0,255,0,0)
color.BLUE=(255,0,0,0)

##Font Class
class Font(object):
    pass

font = Font()
font.default = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1.0, 1.0, thickness=2)


##Functions For Image Processing
def cvimg2numpy(cvimg):
  return numpy.asarray(cv.GetMat(cvimg))
  
def bgr2hsv(cvimg):
  size = (cvimg.width, cvimg.height)
  depth = cvimg.depth
  channels = cvimg.nChannels
  hsvimg = cv.CreateImage(size, depth, channels)
  cv.CvtColor(cvimg, hsvimg, cv.CV_BGR2HSV)
  return hsvimg
  
def bgr2gray(cvimg):
  size = (cvimg.width, cvimg.height)
  depth = cvimg.depth
  channels = cvimg.nChannels
  grayimg = cv.CreateImage(size, depth, 1)
  cv.CvtColor(cvimg, grayimg, cv.CV_BGR2GRAY)
  return grayimg
  
def bgr2rgb(cvimg):
  size = (cvimg.width, cvimg.height)
  depth = cvimg.depth
  channels = cvimg.nChannels
  rgbimg = cv.CreateImage(size, depth, channels)
  cv.CvtColor(cvimg, rgbimg, cv.CV_BGR2RGB)
  return rgbimg

def rgb2bgr(cvimg):
  size = (cvimg.width, cvimg.height)
  depth = cvimg.depth
  channels = cvimg.nChannels
  bgrimg = cv.CreateImage(size, depth, channels)
  cv.CvtColor(cvimg, bgrimg, cv.CV_RGB2BGR)
  return bgrimg

def split3(cvimg):
  size = (cvimg.width, cvimg.height)
  c1 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
  c2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)  
  c3 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
  cv.Split(cvimg, c1, c2, c3, None)
  return c1,c2,c3

def merge3(b,g,r):
  size = (r.width, r.height)
  img = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
  cv.Merge(b,g,r,None,img)
  return img

##Function returns the size of an image.
def size(cvimg):
  return (cvimg.width, cvimg.height)

##Function finds the contours.
def find_contours(im):
    try:
      storage = cv.CreateMemStorage(0)
      contours = cv.FindContours(im, 
                               storage,
                               cv.CV_RETR_TREE,
                               cv.CV_CHAIN_APPROX_SIMPLE)
      if len(contours) != 0:
        contours = cv.ApproxPoly(contours,
                             storage,
                             cv.CV_POLY_APPROX_DP, 3, 1)
        return contours
    except:
      pass

##Function find the convex hull.
def find_convex_hull(cvseq):
    try:
      storage = cv.CreateMemStorage(0)
      hull = cv.ConvexHull2(cvseq, storage, cv.CV_CLOCKWISE, 0)
      return hull
    except:
      pass

##Function find the defects.
def find_convex_defects(contour, hull):
    storage = cv.CreateMemStorage(0)
    return cv.ConvexityDefects(contour, hull, storage)

##Function finds the maximum area.
def max_area(contours):
    max_area = 0
    max_contours = contours
    try:
      while True:
          area = cv.ContourArea(contours)
          if area > max_area:
              max_area = area
              max_contours = contours
          contours = contours.h_next()
    except:
      pass
    return max_area, max_contours

##Function finds the maximum rectangle.
def find_max_rectangle(contours):
    max_a, contours = max_area(contours)
    left, top, w, h = cv.BoundingRect(contours)
    right = left + w
    bottom = top + h
    center_x = left + w/2
    center_y = top + h/2 
    return left, top, right, bottom # isCenter

##Plot Functions
def plot_contours(contours, shape):
    img = cv.CreateImage(shape, 8, 3)
    cv.NamedWindow('Controus', 1)
    cv.SetZero(img)
    cv.DrawContours(img, contours, color.RED, color.GREEN, 1)
    cv.ShowImage('Controus', img)