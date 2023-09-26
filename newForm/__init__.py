from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL import Image
import pytesseract
import webbrowser
import sys
import os
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from .adjustMapForm import AdjustMapImageForm
from .rotationForm import RotationImageForm
from .blurForm import AverblurImageForm, RectblurImageForm, MedblurImageForm, GaussionblurImageForm
from .contrastForm import ContrastImageForm


