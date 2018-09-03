'''
Hank Moss 2018

Create Random Instances is a tool that allows you to create and randomly place duplicate instances of a pre-existing object in your Maya scene.

Usage:
Copy and paste entire code into Python Script Editor in Maya

'''

import maya.cmds as cmds
import random
from random import gauss
from random import randint
import functools

def create_rand_instances():
    
    windowID = 'buttonUI'
    # Test to make sure that UI isn't already active
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, title="Create Random Instances", sizeable=False, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1,210), (2,80)], columnOffset = [(1,"left",3)])
    
    cmds.separator(h=5, style = "none")
    cmds.separator(h=5, style = "none")
    
    cmds.text(label = "General Information:")
    cmds.separator(h=10, style = "none")
    
    cmds.separator(h=5, style = "none")
    cmds.separator(h=5, style = "none")
    
    #name of object
    cmds.text(label = "Name of object")
    name_of_object_input = cmds.textField()
    
    #number of copies
    cmds.text(label = "Number of copies")
    number_of_copies_input = cmds.intField()
    
    cmds.separator(h=10, style = "none")
    cmds.separator(h=10, style = "none")
    
    cmds.text(label = "Random Generation by Range:")
    cmds.separator(h=10, style = "none")
    
    cmds.separator(h=5, style = "none")
    cmds.separator(h=5, style = "none")
    
    #x range
    cmds.text(label = "X range around origin")
    x_range_input = cmds.intField()
    
    #z range
    cmds.text(label = "Z range around origin")
    z_range_input = cmds.intField()
    
    cmds.separator(h=10, style = "none")
    cmds.separator(h=10, style = "none")
    
    cmds.text(label = "Generation by Gaussian Distribution:")
    cmds.separator(h=10, style = "none")
    
    cmds.separator(h=5, style = "none")
    cmds.separator(h=5, style = "none")
    
    #standard deviation
    cmds.text(label = "Standard Deviation around object")
    sd_input = cmds.intField()
    
    cmds.separator(h=10, style = "none")
    cmds.separator(h=10, style = "none")
    
    cmds.text(label = "Random Rotation:")
    cmds.separator(h=10, style = "none")
    
    cmds.separator(h=5, style = "none")
    cmds.separator(h=5, style = "none")
    
    #rotation degree
    cmds.text(label = "Range of Y Rotation (1-360°)")
    rotation_range_input = cmds.intField()
    
    cmds.button(label='Generate', command = functools.partial(generate, name_of_object_input, number_of_copies_input, x_range_input, z_range_input, sd_input, rotation_range_input))
    
    #Cancel button
    def cancelGenerate(*pArgs):
        if cmds.window(windowID, exists = True):
            cmds.deleteUI(windowID)
            
    cmds.button(label = "Cancel", command=cancelGenerate)
        
    cmds.showWindow()
    
#Generate button
def generate(pName_of_object_input, pNumber_of_copies_input, pX_range_input, pZ_range_input, pSd_input, pRotation_range_input, *pArgs):
    
    name_of_object_input = cmds.textField(pName_of_object_input, query=True, text=True)
    number_of_copies_input = cmds.intField(pNumber_of_copies_input, query=True, value=True)
    x_range_input = cmds.intField(pX_range_input, query=True, value=True)
    z_range_input = cmds.intField(pZ_range_input, query=True, value=True)
    sd_input = cmds.intField(pSd_input, query=True, value=True)
    rotation_range_input = cmds.intField(pRotation_range_input, query=True, value=True)
    gauss_option = 0
    
    print("")
    
    #checking that inputs are valid
    if number_of_copies_input < 1:
        print "Number of copies must be greater than 0"
        return
    
    if sd_input > 0:
        gauss_option = 1
    if sd_input < 0:
        print "Standard Deviation must be greater than 0"
        return
        
    if 0 <= rotation_range_input <= 360:
        calcLocation(name_of_object_input, number_of_copies_input, x_range_input, z_range_input, rotation_range_input, gauss_option, sd_input)
    else:
        print("Please enter a valid rotation amount")
    


def calcLocation(name, number, range_x, range_z, rotate_option, gauss_option, gauss_SD):   
    for x in range(0, number):
        
        #select and duplicate the original object
        try:
            cmds.select(name)
        except:
            print "Please enter a valid Name of object in your scene"
            return
        new_obj_name = cmds.duplicate()
        
        #Random locations by Gaussian
        if gauss_option == 1:
            gauss_obj(name, gauss_SD, new_obj_name)
        #Creates a random location based on range
        else:
            rand_loc_obj(new_obj_name, range_x, range_z)
            
        if rotate_option > 0:
            rand_rotate(new_obj_name, rotate_option) 
    
    #closing statement
    if number == 1:
        print "Success!", number, "instance of", name, "randomly generated."
    else: 
        print "Success!", number, "instances of", name, "randomly generated."          


#puts object in a new location based on gaussian distribution  
def gauss_obj(name, gauss_SD, new_obj_name):
    
    cmds.select(name)
    curr_x = cmds.getAttr(name + ".tx")
    curr_z = cmds.getAttr(name + ".tz")
    loc_x = gauss(curr_x, gauss_SD) 
    loc_z = gauss(curr_z, gauss_SD)
    cmds.setAttr(new_obj_name[0] + ".tx", loc_x)
    cmds.setAttr(new_obj_name[0] + ".tz", loc_z)

#Puts obejct in new location based on range    
def rand_loc_obj(new_obj_name, range_x, range_z):
    x_is_neg = randint(0,1)
    z_is_neg = randint(0,1)
    
    loc_x = random.random() * range_x;
    loc_z = random.random() * range_z;
    
    if x_is_neg == 1:
        loc_x *= -1
        
    if z_is_neg == 1:
        loc_z *= -1

    cmds.setAttr(new_obj_name[0] + ".tx", loc_x)
    cmds.setAttr(new_obj_name[0] + ".tz", loc_z)

#rotates object and random amount of degrees   
def rand_rotate(new_obj_name, degree):
    rot_y = random.random() * degree
    y_is_neg = randint(0,1)
    if y_is_neg == 1:
        rot_y *= -1
    cmds.setAttr(new_obj_name[0] + ".ry", rot_y)
    
#--------------------------------------------------

create_rand_instances()
