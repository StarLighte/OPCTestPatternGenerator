import pya 
import tpg
from library.pattern import *

cdL=range(50,100,5)
pitchL=range(200,300,5)

#title="ABCDEFGHIJKLMN\nOPQRSTUVWXYZ\n1234567890+-*/!"
title="1D LINE SPACE"
#func=lambda P,cd,cell:shortbar_array(cd_x=cd,cd_y=3*cd,pitch_x=P,pitch_y=3*cd+100,extension=100,rotation=720,layer=[0,1,"main"],cell=cell)
func=lambda P,cd,cell,*arg,**kwargs:spaceEnd_HH(cd,P,gap=100,ext_w=0.1*cd,ext_h=cd,extension=100,rotation=0,cell=cell,*arg,**kwargs)
tpg.drawLayout(func,pitchL,cdL,title=title,output_filename="spaceline")
