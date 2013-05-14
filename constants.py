###################
## Constants Module
###################

##Hue/Intensity Gesture Skin Detector Constants
class SkinCons(object):
    HUE_LT = 3
    HUE_UT = 50
    INTENSITY_LT = 15
    INTENSITY_UT = 250

##Three Gesture Constants - Depth Lowerbound/UppperBound; Area Lowerbound/UppperBound
class GesConsAttributes(object):
    pass

class GesCons(object):

#   27 - 29, 0.16 - 0.18
    FIST = GesConsAttributes()
    FIST.DEPTH_L = 27.0
    FIST.DEPTH_U = 38.0
    FIST.AREA_L = 0.185
    FIST.AREA_U = 0.242

#   14.5 - 26.8, 0.11 - 0.14 
    SCISSORS = GesConsAttributes()
    SCISSORS.DEPTH_L = 14.5
    SCISSORS.DEPTH_U = 26.8
    SCISSORS.AREA_L = 0.11
    SCISSORS.AREA_U = 0.14

#   0.247 - 0.634
    PALM = GesConsAttributes()
    PALM.DEPTH_L = 45.0
    PALM.DEPTH_U = 67.0
    PALM.AREA_L = 0.141
    PALM.AREA_U = 0.182
