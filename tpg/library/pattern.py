import tpg
import numpy as np
import pya

def lineSpace(cd:float,pitch:float,extension:float=0,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	lineSpace_cell=tpg.Layout_Class.layout.create_cell(f"LS_{cd}P{pitch}_{rotation}")
	cell.insert_hierarchy(lineSpace_cell)
	pattern_width,pattern_height=np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	tpg.rectangle(0,0,cd,pattern_height,rotation,cell=lineSpace_cell,layer=layer,*args,**kwargs)
	position=pitch
	while position<(pattern_width-cd)/2:
		tpg.rectangle(position,0,cd,pattern_height-2*extension,rotation,cell=lineSpace_cell,layer=layer,*args,**kwargs)
		tpg.rectangle(-position,0,cd,pattern_height-2*extension,rotation,cell=lineSpace_cell,layer=layer,*args,**kwargs)
		position+=pitch

def linspace_hierarchy(cd:float,pitch:float,extension:float=0,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	lineSpace_cell=tpg.Layout_Class.layout.create_cell(f"LS_{cd}P{pitch}_{rotation}")
	#scell.insert(pya.CellInstArray(lineSpace_cell,pya.Trans()))
	cell.insert_hierarchy(lineSpace_cell)
	pattern_width,pattern_height =np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	lineSpace_subcell=tpg.Layout_Class.layout.create_cell(f"LS_{cd}P{pitch}_{rotation}_subcell")
	num=abs((pattern_width/2-cd)//pitch)
	tpg.rectangle(-num*pitch,0,cd,pattern_height-2*extension,rotation,cell=lineSpace_subcell,layer=layer,*args,**kwargs)
	lineSpace_cell.insert_hierarchy(lineSpace_subcell,[0,0],tpg.rotation_func([0,0],[pitch,0],rotation),[0,0],2*num+1,1)
	tpg.rectangle(0,pattern_height/2,cd,extension,rotation,layer=layer,cell=lineSpace_cell,align="n",*args,**kwargs)
	tpg.rectangle(0,-pattern_height/2,cd,extension,rotation,layer=layer,cell=lineSpace_cell,align="s",*args,**kwargs)

def spaceLine(cd:float,pitch:float,extension:float=0,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	temp_cell=cell.layout().create_cell(f"SL_{cd}P{pitch}_{rotation}_temp")
	pattern_width,pattern_height=np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	bbox=pya.Region(tpg.rectangle(0,0,pattern_width,pattern_height,cell=temp_cell,layer=layer,draw=False))
	lineSpace(cd,pitch,extension,rotation,layer,cell=temp_cell,*args,**kwargs)
	temp_cell.flatten(True)
	r=pya.Region(temp_cell.shapes(cell.layout().layer(*layer)))
	cell.shapes(cell.layout().layer(*layer)).insert((bbox-r).decompose_convex())
	temp_cell.delete()



def shortbar_array(cd_x:float,pitch_x:float,cd_y,pitch_y,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	sub_cell=tpg.Layout_Class.layout.create_cell(f"sb_{cd_x}_{cd_y}_P{pitch_x}_{pitch_y}_r{rotation}")
	pattern_width,pattern_height =np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	num_x=abs((pattern_width/2-cd_x)//pitch_x)
	num_y=abs((pattern_height/2-cd_y)//pitch_y)
	tpg.rectangle(-num_x*pitch_x,-num_y*pitch_y,cd_x,cd_y,rotation,layer=layer,cell=sub_cell)
	cell.insert_hierarchy(sub_cell,[0,0],tpg.rotation_func([0,0],[pitch_x,0],rotation),tpg.rotation_func([0,0],[0,pitch_y],rotation),2*num_x+1,2*num_y+1)
	
def lineEnd_HH(cd:float,pitch:float,gap:float,ext_w:float=0,ext_h:float=0,extension=0,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	lineEnd_cell=tpg.Layout_Class.layout.create_cell(f"LE_{cd}_P{pitch}_r{rotation}")
	pattern_width,pattern_height =np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	num=abs((pattern_width/2-cd)//pitch)
	cell.insert_hierarchy(lineEnd_cell)
	lineEnd_subcell=tpg.Layout_Class.layout.create_cell(f"LE_{cd}P{pitch}_{rotation}_subcell")
	tpg.rectangle(-num*pitch,pattern_height/2-extension,cd,(pattern_height-gap)/2-extension,rotation,cell=lineEnd_subcell,layer=layer,align="n",*args,**kwargs)
	tpg.rectangle(-num*pitch,-pattern_height/2+extension,cd,(pattern_height-gap)/2-extension,rotation,cell=lineEnd_subcell,layer=layer,align="s",*args,**kwargs)
	tpg.rectangle(-num*pitch,gap/2,2*ext_w+cd,ext_h,rotation,cell=lineEnd_subcell,layer=layer,align="s",*args,**kwargs)
	tpg.rectangle(-num*pitch,-gap/2,2*ext_w+cd,ext_h,rotation,cell=lineEnd_subcell,layer=layer,align="n",*args,**kwargs)
	lineEnd_cell.insert_hierarchy(lineEnd_subcell,[0,0],tpg.rotation_func([0,0],[pitch,0],rotation),[0,0],2*num+1,1)
	tpg.rectangle(0,pattern_height/2,cd,extension,rotation,layer=layer,cell=lineEnd_cell,align="n",*args,**kwargs)
	tpg.rectangle(0,-pattern_height/2,cd,extension,rotation,layer=layer,cell=lineEnd_cell,align="s",*args,**kwargs)
	
def spaceEnd_HH(cd:float,pitch:float,gap:float,ext_w:float=0,ext_h:float=0,extension=0,rotation:float=0,layer:list=[0,0],cell:pya.Cell=None,*args,**kwargs):
	if cell==None:
		cell=tpg.Layout_Class.layout.top_cell()
	temp_cell=cell.layout().create_cell(f"SE_{cd}P{pitch}_{rotation}_temp")
	pattern_width,pattern_height=np.abs(tpg.Layout_Class.cell_params["pattern_shape"])
	bbox=pya.Region(tpg.rectangle(0,0,pattern_width,pattern_height,cell=temp_cell,layer=layer,draw=False))
	lineEnd_HH(cd,pitch,gap,ext_w,ext_h,extension,rotation,layer,cell=temp_cell,*args,**kwargs)
	temp_cell.flatten(True)
	r=pya.Region(temp_cell.shapes(cell.layout().layer(*layer)))
	cell.shapes(cell.layout().layer(*layer)).insert((bbox-r).decompose_convex())
	temp_cell.delete()