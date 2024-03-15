import pya
import numpy as np
import time
import tqdm
import copy
import json

class Layout_Class:

	layout=pya.Layout()

	def dbu():
		return Layout_Class.layout.dbu
	
	cell_params={"cell_name":"","cell_shape":np.array([20_000,20_000]),"pattern_shape":np.array([15_000,15_000]),"cell_coor":np.array([10_000,10_000]),"pattern_shift":np.array([2500,2500])}

def rotation_func(original_coor,old_coor,angle:float):
	if angle==0:
		return old_coor
	else:
		old_coor=np.array(old_coor)
		original_coor=np.array(original_coor)
		angle_rad=angle*np.pi/180
		rotational_matrix=np.array([[np.cos(angle_rad),np.sin(angle_rad)],[-np.sin(angle_rad),np.cos(angle_rad)]])
		return (old_coor-original_coor).dot(rotational_matrix)+original_coor

def rectangle(align_x:float=0,align_y:float=0,cd_x:float=0,cd_y:float=0,rotation:float=0,cell:pya.Cell=None,cell_params:dict=None,align:str="c",layer:list=[0,0],cell_Shapes_Library:pya.Shapes=None,shift=True,draw=True,*args,**kwargs):

	if cell_params==None:
		cell_params=Layout_Class.cell_params.copy()

	if not shift:
		cell_params["pattern_shift"]=np.array([0,0])

	if cell_Shapes_Library!= None:
		layout=cell_Shapes_Library.layout()
		cell=cell_Shapes_Library.cell()
	elif cell!=None:
		layout=cell.layout()
		layout_DBU=1000*layout.dbu
		layout_layer=layout.layer(*layer)
		cell_Shapes_Library=cell.shapes(layout_layer)
	else:
		layout=Layout_Class.layout
		layout_DBU=1000*layout.dbu
		layout_layer=layout.layer(*layer)
		if layout.has_cell(cell_params["cell_name"]):
			cell=layout.cell(cell_params["cell_name"])
		else:
			cell=layout.create_cell(cell_params["cell_name"])
		cell_Shapes_Library=cell.shapes(layout_layer)
		
	pattern_coor=cell_params["cell_coor"]+cell_params["pattern_shift"]
	center_x=align_x+pattern_coor[0]
	center_y=align_y+pattern_coor[1]
	if "w" in align:
		center_x+=cd_x/2
	if "e" in align:
		center_x-=cd_x/2
	if "s" in align:
		center_y+=cd_y/2
	if "n" in align:
		center_y-=cd_y/2

	lower_left_coor=np.array([center_x-cd_x/2,center_y-cd_y/2])
	upper_right_coor=lower_left_coor+np.array([cd_x,cd_y])
	if rotation==0:
		llc_dbu=np.round(lower_left_coor/layout_DBU)
		urc_dbu=np.round(upper_right_coor/layout_DBU)
		rectangle_return=pya.Box(*llc_dbu,*urc_dbu)
	elif rotation%90==0:
		llc_dbu=np.round(rotation_func(pattern_coor,lower_left_coor,rotation)/layout_DBU)
		urc_dbu=np.round(rotation_func(pattern_coor,upper_right_coor,rotation)/layout_DBU)
		rectangle_return=pya.Box(*llc_dbu,*urc_dbu)
	else:
		lower_right_coor=lower_left_coor+np.array([cd_x,0])
		upper_left_coor =lower_left_coor+np.array([0,cd_y])
		llc_dbu=pya.Point(*np.round(rotation_func(pattern_coor,lower_left_coor,rotation)/layout_DBU))
		urc_dbu=pya.Point(*np.round(rotation_func(pattern_coor,upper_right_coor,rotation)/layout_DBU))
		lrc_dbu=pya.Point(*np.round(rotation_func(pattern_coor,lower_right_coor,rotation)/layout_DBU))
		ulc_dbu=pya.Point(*np.round(rotation_func(pattern_coor,upper_left_coor,rotation)/layout_DBU))
		rectangle_return=pya.Polygon([llc_dbu,lrc_dbu,urc_dbu,ulc_dbu])
	if draw:
		cell_Shapes_Library.insert(rectangle_return)
	return rectangle_return

def polygon(points:list=[],rotation:float=0,cell:pya.Cell=None,cell_params:dict=None,layer:list=[0,0],cell_Shapes_Library:pya.Shapes=None,shift=True,draw=True,*args,**kwargs):

	if cell_params==None:
		cell_params=Layout_Class.cell_params.copy()

	if not shift:
		cell_params["pattern_shift"]=np.array([0,0])

	if cell_Shapes_Library!= None:
		layout=cell_Shapes_Library.layout()
		cell=cell_Shapes_Library.cell()
	elif cell!=None:
		layout=cell.layout()
		layout_DBU=1000*layout.dbu
		layout_layer=layout.layer(*layer)
		cell_Shapes_Library=cell.shapes(layout_layer)
	else:
		layout=Layout_Class.layout
		layout_DBU=1000*layout.dbu
		layout_layer=layout.layer(*layer)
		if layout.has_cell(cell_params["cell_name"]):
			cell=layout.cell(cell_params["cell_name"])
		else:
			cell=layout.create_cell(cell_params["cell_name"])
		cell_Shapes_Library=cell.shapes(layout_layer)

	points=np.array(points)
	pattern_coor=cell_params["cell_coor"]+cell_params["pattern_shift"]
	pattern_coor=cell_params["cell_coor"]+cell_params["pattern_shift"]
	if len(points.shape)==2:
		point_num=len(points)
		point_list=list(np.zeros(point_num))
		for i in range(point_num):
			point_list[i]=pya.Point(*np.round((rotation_func([0,0],points[i],rotation)+pattern_coor)/layout_DBU))
		polygon_return=pya.Polygon(point_list)
	else:
		polygon_return=pya.Region()
		for pointGroup in points:
			point_num=len(pointGroup)
			point_list=list(np.zeros(point_num))
			for i in range(point_num):
				point_list[i]=pya.Point(*np.round((rotation_func([0,0],pointGroup[i],rotation)+pattern_coor)/layout_DBU))
			polygon_return+=pya.Region(pya.Polygon(point_list))
	if draw:
		cell_Shapes_Library.insert(polygon_return)
	return polygon_return

with open("./library/font.json","r") as f:font_file=json.load(f)

def drawText(string:str,align_x:float,align_y:float,cd:float,space:float,layer:list,align="c",font:dict=font_file,cell:pya.Cell=None,reverse=False,*args,**kwargs):

	if cell==None:
		cell=Layout_Class.layout.top_cell()
	position_y=align_y
	label_cell=cell.layout().create_cell(f"label_{cell.name}")
	counter=0
	for lines in string.split("\n"):
		counter+=1
		line_height=0
		label_line_cell=cell.layout().create_cell(f"label_{cell.name}_{counter}")
		position_x=align_x
		for c in lines:
			shiftVector=np.array([position_x,position_y])
			if c==" ":
				position_x+=space
			else:
				plgn=polygon((np.array(font.get(c,[[[-3,5],[3,5],[3,-5],[-3,-5]]]))-np.array([min(np.array(font.get(c,[[[-3,5],[3,5],[3,-5],[-3,-5]]]))[:,:,0].flatten()),0]))*font.get("grid",1)*cd+shiftVector,layer=layer,cell=label_line_cell,*args,**kwargs)
				position_x+=plgn.bbox().width()*1000*cell.layout().dbu+space

		line_width_dbu=label_line_cell.bbox().width()
		line_height_dbu=label_line_cell.bbox().height()
		line_height=line_height_dbu*1000*cell.layout().dbu+space
		position_y-=line_height
		shift_x=-line_width_dbu/2
		shift_y=0
		if "w" in align:
			shift_x+=line_width_dbu/2
		if "e" in align:
			shift_x-=line_width_dbu/2
		if "s" in align:
			shift_y+=line_height_dbu/2
		if "n" in align:
			shift_y-=line_height_dbu/2
		label_cell.insert(pya.CellInstArray(label_line_cell,pya.Vector(shift_x,shift_y)))
	if reverse:
		label_cell.flatten(True)
		region=pya.Region(label_cell.shapes(cell.layout().layer(*layer)))
		region_bbox=pya.Region(region.bbox().enlarged(round(space/1000/label_cell.layout().dbu)))
		r=(region_bbox-region).decompose_convex()
		label_cell.clear()
		label_cell.shapes(cell.layout().layer(*layer)).insert(r)
	cell.insert(pya.CellInstArray(label_cell,pya.Vector()))
	
def func_insert_hierarchy(self:pya.Cell,cell:pya.Cell=None,shift:list=[0,0],vec_a:list=[0,0],vec_b:list=[0,0],na:int=1,nb:int=1):
	layout=self.layout()
	dbu=layout.dbu*1000
	shift=pya.Vector(*np.round(np.array(shift)/dbu))
	vec_a=pya.Vector(*np.round(np.array(vec_a)/dbu))
	vec_b=pya.Vector(*np.round(np.array(vec_b)/dbu))
	self.insert(pya.CellInstArray(cell,shift,vec_a,vec_b,na,nb))

pya.Cell.insert_hierarchy=func_insert_hierarchy

def drawLayout(function,param_x,param_y,title="",output_folder="./",output_filename="output"):
	Layout_Class.layout=pya.Layout()
	Layout_Class.layout.dbu=0.0001
	topcell=Layout_Class.layout.create_cell("TOP")
	origin_coor=1*Layout_Class.cell_params["cell_coor"]
	for param2 in param_y:
		for param1 in param_x:
			cell=Layout_Class.layout.create_cell(f"{title}_{param1}_{param2}_cell")
			topcell.insert(pya.CellInstArray(cell,pya.Vector()))
			function(param1,param2,cell,layer=[0,0,"main"])
			rectangle(0,0,*Layout_Class.cell_params["cell_shape"],cell=cell,layer=[1000,0],shift=False)
			rectangle(0,0,*Layout_Class.cell_params["pattern_shape"],cell=cell,layer=[1000,1],shift=True)
		
			drawText(f"{param1}   {param2}",-Layout_Class.cell_params["pattern_shape"][0]/2+500,-Layout_Class.cell_params["cell_shape"][1]/2,align="w",cd=500,space=500,layer=[10,1,"label"],cell=cell,reverse=True)
			drawText(f"+",-Layout_Class.cell_params["cell_shape"][0]/2,0,align="c",cd=500,space=500,layer=[10,2,"marker"],cell=cell,reverse=False)

			#drawText(f"{param1}\n{param2}",0,0,align="w",cd=200,space=200,layer=[10,0])

			Layout_Class.cell_params["cell_coor"]+=np.array([1,0])*Layout_Class.cell_params["cell_shape"]
		Layout_Class.cell_params["cell_coor"][0]=origin_coor[0]
		Layout_Class.cell_params["cell_coor"]+=np.array([0,1])*Layout_Class.cell_params["cell_shape"]
	drawText(title,*(np.array([-1/2,0.5])*Layout_Class.cell_params["cell_shape"]),1000,2000,[10,0,"title"],align="nw",shift=False,reverse=False,cell=topcell)
	Layout_Class.cell_params["cell_coor"][1]=origin_coor[1]
	Layout_Class.layout.write(f"{output_folder}{output_filename}.oas")