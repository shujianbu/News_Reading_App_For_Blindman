##########################################################################
## Visual News Interface Main Program
# Description:
#               This visual interface solves a journalistic problem.
#               It assists audiences with disabilities to better access
#               audiable news articles.
# References:   BeautifulSoup and Python OpenCV
# Author:
#               Pucong Han (ph2369)
#               Shujian Bu (sb3331)
##########################################################################

import subprocess
import os, signal
import sys
from os import system
import cv
import numpy
# Import imgproc.py, skin.py, gesture.py and news.py
import imgproc, skin, gesture, news

# Subprocess memory list storing the current running process.
process_list = []

##Setting grammers for hand gestures.
class Grammar(object):
    def __init__(self, initGrammar=[]):
        self.grammar = initGrammar
        self.repeat_count = 0
        self.not_sure_count = 0
        self.long_threshold = 8
        self.last_ges = gesture.Gesture('Uncertain')
        self.start_ges = gesture.Gesture('Palm')

    def __repr__(self):
        return repr(self.grammar)

    def __eq__(self, obj):
        return self.grammar == obj.grammar

    def instantGes(self, ges):
        if ges.hasMeaning():
            self.not_sure_count = 0
            last = self.last_ges
            if last.type_ == ges.type_:
                self.repeat_count += 1
            else:
                self.repeat_count = 0

            if self.repeat_count >= self.long_threshold:
                ges.timing = 'Fist'

            if self.grammar:
                if last.type_ == ges.type_:
                    self.grammar[-1] = ges
                else:
                    self.grammar.append(ges)
            else:
                if ges == self.start_ges:
                    self.grammar.append(ges)
            self.last_ges = ges
        else:
            self.not_sure_count += 1
            if self.not_sure_count >= self.long_threshold:
                self.grammar = []
                self.repeat_count = 0
        return self.grammar

##Image processor function computing skin and countours.
class ImageProcessSession(object):
  def __init__(self, skin_detector):
    self.skin_detector = skin_detector
  # Computing skins and find contours for an input image.
  def process(self, bgrimg):
    img = self.skin_detector.detectSkin(bgrimg)
    contours = imgproc.find_contours(img)
    return contours

##Main function of this visual news interface.
def mainFunction():
  interface_trigger = False
  # Set up the window objects and environment.
  proc_win_name = "Processing window"
  proc_win = cv.NamedWindow(proc_win_name, 1)
  # Initialize the real time camera.
  cam = cv.CaptureFromCAM(0)
  # Initialize the skin detector. the skin detector is defined in skin.py
  skin_detector = skin.SkinDetector()
  # Initialize delay, hue threshold and intensity threshold.
  msdelay = 3
  initHueThreshold = 42
  initIntensityThreshold = 191
  skin_detector.setHueThreshold(initHueThreshold)
  skin_detector.setIntensityThreshold(initIntensityThreshold)
  # Initialize the image processor.
  session = ImageProcessSession(skin_detector)
  ga = gesture.GestureAnalyzer()

  while True:
    k = cv.WaitKey(msdelay)
    k = chr(k) if k > 0 else 0
    # Get the current frame from the video camera.
    bgrimg = cv.QueryFrame(cam)
    # Flip the image.
    cv.Flip(bgrimg, None, 1)
    # Computing the skin and contour for the frame image.
    contours = session.process(bgrimg)
    # Create an image for displaying on the screen.
    img = cv.CreateImage((bgrimg.width, bgrimg.height), 8, 3)

    if interface_trigger:
      # If the contours is not null, the system will launch the gesture analysis
      if contours is not None:
          ges, area, depth = ga.recognize(contours)
          x, y, r, b = imgproc.find_max_rectangle(contours)
          # Drawing a green rectange around the contours on the image.
          cv.Rectangle(img, (x,y), (r, b), imgproc.color.GREEN, thickness=2)
          # Drawing contour points on the image.
          cv.DrawContours(img, contours, imgproc.color.RED, imgproc.color.GREEN, 1, thickness=3)

          #Read national news if palm is detected.
          if str(ges) == 'Palm':
            if len(process_list) == 0:
              # If no current running sub process, the program will create a new sub process to filter and read national news. The process ID will be stored in the process list.
              system("say Palm detected. national news selected")
              process_list.append(subprocess.Popen("say " + news.readNationalNews(), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))
          
          #Read international news if scissors is detected.
          elif str(ges) == 'Scissors':
            if len(process_list) == 0:
              # If no current running sub process, the program will create a new sub process to filter and read international news. The process ID will be stored in the process list.
              system("say Scissor detected. international news selected")
              process_list.append(subprocess.Popen("say " + news.readInternationalNews(), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))

          # Exit interface if fist is selected. All processes in the process list will be terminated.
          elif str(ges) == 'Fist':
            if len(process_list) != 0:
              # If there exist current running sub process, the program will send a signal to terminate all running processes.
              for item in process_list:
                os.killpg(item.pid, signal.SIGTERM)
                process_list.remove(item)
            system("say Fist detected. Exit Visual News Interface")
            sys.exit()
    
    # Exit interface by pressing EXIT button.
    if cv.WaitKey(1) == 27:
      if len(process_list) != 0:
        # If there exist current running sub process, the program will send a signal to terminate all running processes.
        for item in process_list:
          os.killpg(item.pid, signal.SIGTERM)
          process_list.remove(item)
      system("say Exit Visual News Interface")
      sys.exit()
    
    # Terminate all reading processes in the process list by pressing SPACE.
    if cv.WaitKey(1) == 32:
      if len(process_list) != 0:
        for item in process_list:
          # If there exist current running sub process, the program will send a signal to terminate all running processes.
          os.killpg(item.pid, signal.SIGTERM)
          process_list.remove(item)
        system("say Exit Reading")
      else:
        system("say no current reading news")

	# Turn on and off the hand gesture detector by pressing ENTER.
    if cv.WaitKey(1) == 13:
      if interface_trigger == False:
        system("say Hand gesture detector started.")
        interface_trigger = True
      else:
        system("say Hand gesture detector closed")
        interface_trigger = False

	# Reading national news by pressing the 'n' button.
    if cv.WaitKey(1) == 110:
      if len(process_list) == 0:
        # If no current running sub process, the program will create a new sub process to filter and read national news. The process ID will be stored in the process list.
        system("say National news selected")
        process_list.append(subprocess.Popen("say " + news.readNationalNews(), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))

	# Reading international news by pressing the 'i' button.
    if cv.WaitKey(1) == 105:
      if len(process_list) == 0:
        # If no current running sub process, the program will create a new sub process to filter and read international news. The process ID will be stored in the process list.
        system("say International news selected")
        process_list.append(subprocess.Popen("say " + news.readInternationalNews(), stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))
    cv.ShowImage(proc_win_name, img)

# Running the main function
if __name__=='__main__':
  mainFunction()
