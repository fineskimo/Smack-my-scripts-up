import bpy
import mathutils

context = bpy.context
parent = context.active_object
target = parent.name
selected = context.selected_objects
mesh = parent.data
size = len(mesh.vertices)

#note to self : add context check here

con_name = ("ChildOf %s")%parent.name
con_type = 'CHILD_OF'
    

def get_closest_vert(child_loc, parent):

    verts = parent.data.vertices
    closest = 0
    wLoc = parent.matrix_world @ verts[closest].co
    d = (child_loc - wLoc).magnitude
    for i in range(1, len(verts)):
        vLoc = verts[i].co
        wLoc = parent.matrix_world @ vLoc
        d2 = (child_loc - wLoc).magnitude
        if d2<d:
            closest = i
            d = d2
    return closest, vLoc

    
for ob in selected:

    if ob.name != parent.name:
        #note to self : check for exisiting vgroup here 
        grp_name = ("Parent_Vertex_%s")%ob.name
        child_loc = ob.location        
        index, vLoc = get_closest_vert(child_loc, parent)       
        print(index)
        ob.location = (0, 0, 0)
        vg = parent.vertex_groups.new(name = grp_name)
        vg.add([index], 1.0, 'REPLACE') 
        con = ob.constraints.new(type=con_type)
        #note to self : check for exisiting constraint here and override
        con.name = con_name
        con.target = parent
        con.subtarget = grp_name
        
        #these are optional
        con.use_scale_x= False
        con.use_scale_y= False
        con.use_scale_z= False
