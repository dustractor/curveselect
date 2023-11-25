bl_info = {
    "name":"curve select",
    "author":"dustractor",
    "blender":(2,80,0),
    "category":"Curve"
}


import bpy

def _(c=None,r=[]):
    if c:
        r.append(c)
        return c
    else:
        return r


@_
class CS_curve_select_by_n(bpy.types.Operator):
    bl_idname = "curve.select_by_n"
    bl_label = "select by n"
    bl_options =  {"REGISTER","UNDO"}
    n: bpy.props.IntProperty(default=2,min=2)
    offset: bpy.props.IntProperty(default=0,min=0)
    def execute(self,context):
        N = self.n
        O = self.offset
        for ob in filter(
                lambda _:_.type == "CURVE",context.selected_editable_objects):
            for s in ob.data.splines:
                for n,p in enumerate(s.points):
                    p.select = (O+n) % N == 0
        return {"FINISHED"}


@_
class CS_curve_select_cyclic(bpy.types.Operator):
    bl_idname = "curve.select_cyclic"
    bl_label = "select cyclic"
    bl_options =  {"REGISTER","UNDO"}
    def execute(self,context):
        for ob in filter(
                lambda _:_.type == "CURVE",context.selected_editable_objects):
            for s in ob.data.splines:
                q = s.use_cyclic_u
                for p in s.points:
                    p.select = q
        return {"FINISHED"}


@_
class CS_curve_select_by_length(bpy.types.Operator):
    bl_idname = "curve.select_by_length"
    bl_label = "select by length"
    bl_options =  {"REGISTER","UNDO"}
    minlength: bpy.props.IntProperty(default=2,min=2)
    maxlength: bpy.props.IntProperty(default=2,min=2)
    def invoke(self,context,event):
        minL = 2
        maxL = 2
        for ob in filter(
                lambda _:_.type == "CURVE",context.selected_editable_objects):
            for s in ob.data.splines:
                L = len(s.points)
                minL = min(minL,L)
                maxL = max(maxL,L)
        self.minlength = minL
        self.maxlength = maxL
        return self.execute(context)
    def execute(self,context):
        n1,n2 = self.minlength,self.maxlength
        for ob in filter(
                lambda _:_.type == "CURVE",context.selected_editable_objects):
            for s in ob.data.splines:
                L = len(s.points)
                q = (L>=n1) and (L<=n2)
                for p in s.points:
                    p.select = q
        return {"FINISHED"}


@_
class CS_curve_select_longest(bpy.types.Operator):
    bl_idname = "curve.select_longest"
    bl_label = "select longest"
    bl_options =  {"REGISTER","UNDO"}
    def execute(self,context):
        for ob in context.selected_editable_objects:
            if ob.type == "CURVE":
                L = 0
                for s in ob.data.splines:
                    L = max(L,len(s.points))
                for s in ob.data.splines:
                    if len(s.points) == L:
                        for p in s.points:
                            p.select = True
        return {"FINISHED"}


@_
class CS_curve_select_shortest(bpy.types.Operator):
    bl_idname = "curve.select_shortest"
    bl_label = "select shortest"
    bl_options =  {"REGISTER","UNDO"}
    def execute(self,context):
        m = __import__("sys").maxsize
        for ob in context.selected_editable_objects:
            if ob.type == "CURVE":
                L = m
                for s in ob.data.splines:
                    L = min(L,len(s.points))
                for s in ob.data.splines:
                    if len(s.points) == L:
                        for p in s.points:
                            p.select = True
        return {"FINISHED"}


def menu_draw(self,context):
    for c in _():
        self.layout.operator(c.bl_idname)

def register():
    list(map(bpy.utils.register_class,_()))
    bpy.types.VIEW3D_MT_select_edit_curve.append(menu_draw)
def unregister():
    bpy.types.VIEW3D_MT_select_edit_curve.remove(menu_draw)
    list(map(bpy.utils.unregister_class,_()))

