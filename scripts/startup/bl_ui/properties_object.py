# SPDX-FileCopyrightText: 2009-2023 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from bl_ui.properties_animviz import (
    MotionPathButtonsPanel,
    MotionPathButtonsPanel_display,
)
import bpy
from bpy.types import Panel, Menu
from rna_prop_ui import PropertyPanel
from .space_properties import PropertiesAnimationMixin
from bpy.app.handlers import persistent
from bpy.types import Operator
from bpy.props import BoolProperty


class ObjectButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"


class OBJECT_PT_context_object(ObjectButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        space = context.space_data

        if space.use_pin_id:
            layout.template_ID(space, "pin_id")
        else:
            row = layout.row()
            row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')

class OBJECT_OT_align_x(Operator):
    bl_idname = "object.align_x"
    bl_label = "对齐X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.location.x = active.location.x
        return {'FINISHED'}

class OBJECT_OT_align_y(Operator):
    bl_idname = "object.align_y"
    bl_label = "对齐Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.location.y = active.location.y
        return {'FINISHED'}

class OBJECT_OT_align_z(Operator):
    bl_idname = "object.align_z"
    bl_label = "对齐Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.location.z = active.location.z
        return {'FINISHED'}

class OBJECT_OT_align_rotation_x(Operator):
    bl_idname = "object.align_rotation_x"
    bl_label = "对齐旋转X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.rotation_euler.x = active.rotation_euler.x
        return {'FINISHED'}

class OBJECT_OT_align_rotation_y(Operator):
    bl_idname = "object.align_rotation_y"
    bl_label = "对齐旋转Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.rotation_euler.y = active.rotation_euler.y
        return {'FINISHED'}

class OBJECT_OT_align_rotation_z(Operator):
    bl_idname = "object.align_rotation_z"
    bl_label = "对齐旋转Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.rotation_euler.z = active.rotation_euler.z
        return {'FINISHED'}

class OBJECT_OT_align_scale_x(Operator):
    bl_idname = "object.align_scale_x"
    bl_label = "对齐缩放X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.scale.x = active.scale.x
        return {'FINISHED'}

class OBJECT_OT_align_scale_y(Operator):
    bl_idname = "object.align_scale_y"
    bl_label = "对齐缩放Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.scale.y = active.scale.y
        return {'FINISHED'}

class OBJECT_OT_align_scale_z(Operator):
    bl_idname = "object.align_scale_z"
    bl_label = "对齐缩放Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) < 2:
            self.report({'WARNING'}, "需要选择至少两个物体")
            return {'CANCELLED'}
        active = context.active_object
        for obj in selected:
            if obj != active:
                obj.scale.z = active.scale.z
        return {'FINISHED'}
    

def update_new_location(self, context):
    if context.scene.get("skip_update", False):
        return

    new_loc = context.scene.new_location
    temp_loc = context.scene.temp_new_location
    selected_objects = context.selected_objects
    use_relative = context.scene.use_relative_transform

    for obj in selected_objects:
        if use_relative:
            # 相对变换
            if new_loc.x != temp_loc[0]:
                obj.location.x += new_loc.x - temp_loc[0]
            if new_loc.y != temp_loc[1]:
                obj.location.y += new_loc.y - temp_loc[1]
            if new_loc.z != temp_loc[2]:
                obj.location.z += new_loc.z - temp_loc[2]
        else:
            # 绝对变换（原来的逻辑）
            obj.location.x = new_loc.x if new_loc.x != temp_loc[0] else obj.location.x
            obj.location.y = new_loc.y if new_loc.y != temp_loc[1] else obj.location.y
            obj.location.z = new_loc.z if new_loc.z != temp_loc[2] else obj.location.z

    # 更新临时位置
    context.scene.temp_new_location = new_loc[:]

def update_new_rotation(self, context):
    if context.scene.get("skip_update", False):
        return

    new_rot = context.scene.new_rotation
    temp_rot = context.scene.temp_new_rotation
    selected_objects = context.selected_objects
    use_relative = context.scene.use_relative_transform

    for obj in selected_objects:
        if use_relative:
            # 相对变换
            if new_rot.x != temp_rot.x:
                obj.rotation_euler.x += new_rot.x - temp_rot.x
            if new_rot.y != temp_rot.y:
                obj.rotation_euler.y += new_rot.y - temp_rot.y
            if new_rot.z != temp_rot.z:
                obj.rotation_euler.z += new_rot.z - temp_rot.z
        else:
            # 绝对变换
            obj.rotation_euler.x = new_rot.x if new_rot.x != temp_rot.x else obj.rotation_euler.x
            obj.rotation_euler.y = new_rot.y if new_rot.y != temp_rot.y else obj.rotation_euler.y
            obj.rotation_euler.z = new_rot.z if new_rot.z != temp_rot.z else obj.rotation_euler.z

    # 更新临时旋转
    context.scene.temp_new_rotation = new_rot[:]

def update_new_scale(self, context):
    if context.scene.get("skip_update", False):
        return

    new_scale = context.scene.new_scale
    temp_scale = context.scene.temp_new_scale
    selected_objects = context.selected_objects
    use_relative = context.scene.use_relative_transform

    for obj in selected_objects:
        if use_relative:
            # 相对变换
            if new_scale.x != temp_scale[0]:
                obj.scale.x *= new_scale.x / temp_scale[0]
            if new_scale.y != temp_scale[1]:
                obj.scale.y *= new_scale.y / temp_scale[1]
            if new_scale.z != temp_scale[2]:
                obj.scale.z *= new_scale.z / temp_scale[2]
        else:
            # 绝对变换
            obj.scale.x = new_scale.x if new_scale.x != temp_scale[0] else obj.scale.x
            obj.scale.y = new_scale.y if new_scale.y != temp_scale[1] else obj.scale.y
            obj.scale.z = new_scale.z if new_scale.z != temp_scale[2] else obj.scale.z

    # 更新临时缩放
    context.scene.temp_new_scale = new_scale[:]


def update_selection():
    context = bpy.context
    active_object = context.view_layer.objects.active

    if active_object:
        new_loc = active_object.location
        new_rot = active_object.rotation_euler
        new_scale = active_object.scale
    else:
        new_loc = (0, 0, 0)
        new_rot = (0, 0, 0)
        new_scale = (1, 1, 1)
    
    context.scene["skip_update"] = True
    context.scene.temp_new_location = new_loc
    context.scene.new_location = new_loc
    context.scene.temp_new_rotation = new_rot
    context.scene.new_rotation = new_rot
    context.scene.temp_new_scale = new_scale
    context.scene.new_scale = new_scale
    del context.scene["skip_update"]

# 新位置属性
bpy.types.Scene.new_location = bpy.props.FloatVectorProperty(
    name="New Location",
    description="魔改新位置属性",
    subtype='TRANSLATION',
    default=(0.0, 0.0, 0.0),
    update=update_new_location
)

# 新位置属性Temp，在更新物体选择时，临时存储新位置
bpy.types.Scene.temp_new_location = bpy.props.FloatVectorProperty(
    name="Temp New Location",
    description="新位置属性Temp，在更新物体选择时，临时存储新位置",
    subtype='TRANSLATION',
    default=(0.0, 0.0, 0.0)
)

# 新旋转属性
bpy.types.Scene.new_rotation = bpy.props.FloatVectorProperty(
    name="New Rotation",
    description="魔改新旋转属性",
    subtype='EULER',
    size=3,
    default=(0.0, 0.0, 0.0),
    update=update_new_rotation
)

# 新旋转属性Temp，在更新物体选择时，临时存储新旋转
bpy.types.Scene.temp_new_rotation = bpy.props.FloatVectorProperty(
    name="Temp New Rotation",
    description="新旋转属性Temp，在更新物体选择时，临时存储新旋转",
    subtype='EULER',
    size=3,
    default=(0.0, 0.0, 0.0)
)

# 新缩放属性
bpy.types.Scene.new_scale = bpy.props.FloatVectorProperty(
    name="New Scale",
    description="魔改新缩放属性",
    subtype='XYZ',
    default=(1.0, 1.0, 1.0),
    update=update_new_scale
)

# 新缩放属性Temp，在更新物体选择时，临时存储新缩放
bpy.types.Scene.temp_new_scale = bpy.props.FloatVectorProperty(
    name="Temp New Scale",
    description="新缩放属性Temp，在更新物体选择时，临时存储新缩放",
    subtype='XYZ',
    default=(1.0, 1.0, 1.0)
)

bpy.types.Scene.use_relative_transform = BoolProperty(
    name="使用相对Transform",
    description="启用相对变换模式",
    default=False
)

subscribe_to = [
    (bpy.types.LayerObjects, "active"),
    (bpy.types.LayerObjects, "selected")
]

for key in subscribe_to:
    bpy.msgbus.subscribe_rna(
        key=key,
        owner=object(),
        args=(),
        notify=update_selection
    )

@persistent
def undo_redo_handler(dummy):
    update_selection()

# 在撤销和重做操作后，更新物体选择
bpy.app.handlers.undo_post.append(undo_redo_handler)
bpy.app.handlers.redo_post.append(undo_redo_handler)

class OBJECT_PT_transform(ObjectButtonsPanel, Panel):
    bl_label = "Transform"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        selected_objects = context.selected_objects
        if len(selected_objects) == 1:
            ob = selected_objects[0]
            col = layout.column()
            row = col.row(align=True)
            row.prop(ob, "location")
            row.use_property_decorate = False
            row.prop(ob, "lock_location", text="", emboss=False, icon='DECORATE_UNLOCKED')

            rotation_mode = ob.rotation_mode
            if rotation_mode == 'QUATERNION':
                col = layout.column()
                row = col.row(align=True)
                row.prop(ob, "rotation_quaternion", text="Rotation")
                sub = row.column(align=True)
                sub.use_property_decorate = False
                sub.prop(ob, "lock_rotation_w", text="", emboss=False, icon='DECORATE_UNLOCKED')
                sub.prop(ob, "lock_rotation", text="", emboss=False, icon='DECORATE_UNLOCKED')
            elif rotation_mode == 'AXIS_ANGLE':
                col = layout.column()
                row = col.row(align=True)
                row.prop(ob, "rotation_axis_angle", text="Rotation")

                sub = row.column(align=True)
                sub.use_property_decorate = False
                sub.prop(ob, "lock_rotation_w", text="", emboss=False, icon='DECORATE_UNLOCKED')
                sub.prop(ob, "lock_rotation", text="", emboss=False, icon='DECORATE_UNLOCKED')
            else:
                col = layout.column()
                row = col.row(align=True)
                row.prop(ob, "rotation_euler", text="Rotation")
                row.use_property_decorate = False
                row.prop(ob, "lock_rotation", text="", emboss=False, icon='DECORATE_UNLOCKED')
            row = layout.row(align=True)
            row.prop(ob, "rotation_mode", text="Mode")
            row.label(text="", icon='BLANK1')

            col = layout.column()
            row = col.row(align=True)
            row.prop(ob, "scale")
            row.use_property_decorate = False
            row.prop(ob, "lock_scale", text="", emboss=False, icon='DECORATE_UNLOCKED')
        
        elif len(selected_objects) > 1:
            col = layout.column()
            row = col.row(align=True)
            row.prop(context.scene, "use_relative_transform", text="使用相对Transform")
            
            col = layout.column()
            row = col.row(align=True)
            row.prop(context.scene, "new_location", text="Location")
            
            sub = row.column(align=True)
            sub.scale_x = 0.5
            sub.operator("object.align_x", text="对齐X")
            sub.operator("object.align_y", text="对齐Y")
            sub.operator("object.align_z", text="对齐Z")
            
            col = layout.column()
            row = col.row(align=True)
            row.prop(context.scene, "new_rotation", text="Rotation")
            
            sub = row.column(align=True)
            sub.scale_x = 0.5
            sub.operator("object.align_rotation_x", text="对齐X")
            sub.operator("object.align_rotation_y", text="对齐Y")
            sub.operator("object.align_rotation_z", text="对齐Z")
            
            col = layout.column()
            row = col.row(align=True)
            row.prop(context.scene, "new_scale", text="Scale")
            
            sub = row.column(align=True)
            sub.scale_x = 0.5
            sub.operator("object.align_scale_x", text="对齐X")
            sub.operator("object.align_scale_y", text="对齐Y")
            sub.operator("object.align_scale_z", text="对齐Z")


class OBJECT_PT_delta_transform(ObjectButtonsPanel, Panel):
    bl_label = "Delta Transform"
    bl_parent_id = "OBJECT_PT_transform"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object

        col = layout.column()
        col.prop(ob, "delta_location", text="Location")

        rotation_mode = ob.rotation_mode
        if rotation_mode == 'QUATERNION':
            col.prop(ob, "delta_rotation_quaternion", text="Rotation")
        elif rotation_mode == 'AXIS_ANGLE':
            pass
        else:
            col.prop(ob, "delta_rotation_euler", text="Rotation")

        col.prop(ob, "delta_scale", text="Scale")


class OBJECT_PT_relations(ObjectButtonsPanel, Panel):
    bl_label = "Relations"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object

        col = flow.column()
        col.prop(ob, "parent")
        sub = col.column()
        sub.prop(ob, "parent_type")
        parent = ob.parent
        if parent and ob.parent_type == 'BONE' and parent.type == 'ARMATURE':
            sub.prop_search(ob, "parent_bone", parent.data, "bones")
        sub.active = (parent is not None)
        sub.prop(ob, "use_camera_lock_parent")

        col.separator()

        col = flow.column()

        col.prop(ob, "track_axis", text="Tracking Axis")
        col.prop(ob, "up_axis", text="Up Axis")

        col.separator()

        col = flow.column()

        col.prop(ob, "pass_index")


class COLLECTION_MT_context_menu(Menu):
    bl_label = "Collection Specials"

    def draw(self, _context):
        layout = self.layout

        layout.operator("object.collection_unlink", icon='X')
        layout.operator("object.collection_objects_select")
        layout.operator("object.instance_offset_from_cursor")


class OBJECT_PT_collections(ObjectButtonsPanel, Panel):
    bl_label = "Collections"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row(align=True)
        if bpy.data.collections:
            row.operator("object.collection_link", text="Add to Collection")
        else:
            row.operator("object.collection_add", text="Add to Collection")
        row.operator("object.collection_add", text="", icon='ADD')

        for collection in obj.users_collection:
            col = layout.column(align=True)

            col.context_pointer_set("collection", collection)

            row = col.box().row()
            row.prop(collection, "name", text="")
            row.operator("object.collection_remove", text="", icon='X', emboss=False)
            row.menu("COLLECTION_MT_context_menu", icon='DOWNARROW_HLT', text="")

            row = col.box().row()
            row.prop(collection, "instance_offset", text="")


class OBJECT_PT_display(ObjectButtonsPanel, Panel):
    bl_label = "Viewport Display"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        obj_type = obj.type
        is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'CURVES', 'POINTCLOUD'})
        has_bounds = (is_geometry or obj_type in {'LATTICE', 'ARMATURE'})
        is_wire = (obj_type in {'CAMERA', 'EMPTY'})
        is_empty_image = (obj_type == 'EMPTY' and obj.empty_display_type == 'IMAGE')
        is_dupli = (obj.instance_type != 'NONE')
        is_gpencil = (obj_type == 'GPENCIL')

        col = layout.column(heading="Show")
        col.prop(obj, "show_name", text="Name")
        col.prop(obj, "show_axis", text="Axes")

        # Makes no sense for cameras, armatures, etc.!
        # but these settings do apply to dupli instances
        if is_geometry or is_dupli:
            col.prop(obj, "show_wire", text="Wireframe")
        if obj_type == 'MESH' or is_dupli:
            col.prop(obj, "show_all_edges", text="All Edges")
        if is_geometry:
            col.prop(obj, "show_texture_space", text="Texture Space")
            col.prop(obj.display, "show_shadows", text="Shadow")
        col.prop(obj, "show_in_front", text="In Front")
        # if obj_type == 'MESH' or is_empty_image:
        #    col.prop(obj, "show_transparent", text="Transparency")
        sub = layout.column()
        if is_wire:
            # wire objects only use the max. display type for duplis
            sub.active = is_dupli
        sub.prop(obj, "display_type", text="Display As")

        if is_geometry or is_dupli or is_empty_image or is_gpencil:
            # Only useful with object having faces/materials...
            col.prop(obj, "color")

        if has_bounds:
            col = layout.column(align=False, heading="Bounds")
            col.use_property_decorate = False
            row = col.row(align=True)
            sub = row.row(align=True)
            sub.prop(obj, "show_bounds", text="")
            sub = sub.row(align=True)
            sub.active = obj.show_bounds or (obj.display_type == 'BOUNDS')
            sub.prop(obj, "display_bounds_type", text="")
            row.prop_decorator(obj, "display_bounds_type")


class OBJECT_PT_instancing(ObjectButtonsPanel, Panel):
    bl_label = "Instancing"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        # FONT objects need (vertex) instancing for the "Object Font" feature.
        return (ob.type in {'MESH', 'EMPTY', 'FONT'})

    def draw(self, context):
        layout = self.layout

        ob = context.object

        row = layout.row()
        row.prop(ob, "instance_type", expand=True)

        layout.use_property_split = True

        if ob.instance_type == 'VERTS':
            layout.prop(ob, "use_instance_vertices_rotation", text="Align to Vertex Normal")

        elif ob.instance_type == 'COLLECTION':
            col = layout.column()
            col.prop(ob, "instance_collection", text="Collection")

        if ob.instance_type != 'NONE' or ob.particle_systems:
            col = layout.column(heading="Show Instancer", align=True)
            col.prop(ob, "show_instancer_for_viewport", text="Viewport")
            col.prop(ob, "show_instancer_for_render", text="Render")


class OBJECT_PT_instancing_size(ObjectButtonsPanel, Panel):
    bl_label = "Scale by Face Size"
    bl_parent_id = "OBJECT_PT_instancing"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob is not None) and (ob.instance_type == 'FACES')

    def draw_header(self, context):

        ob = context.object
        self.layout.prop(ob, "use_instance_faces_scale", text="")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        layout.use_property_split = True

        layout.active = ob.use_instance_faces_scale
        layout.prop(ob, "instance_faces_scale", text="Factor")


class OBJECT_PT_lineart(ObjectButtonsPanel, Panel):
    bl_label = "Line Art"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob.type in {'MESH', 'FONT', 'CURVE', 'SURFACE'})

    def draw(self, context):
        layout = self.layout
        ob = context.object
        lineart = ob.lineart

        layout.use_property_split = True

        layout.prop(lineart, "usage")
        layout.use_property_split = True

        row = layout.row(heading="Override Crease")
        row.prop(lineart, "use_crease_override", text="")
        subrow = row.row()
        subrow.active = lineart.use_crease_override
        subrow.prop(lineart, "crease_threshold", slider=True, text="")

        row = layout.row(heading="Intersection Priority")
        row.prop(lineart, "use_intersection_priority_override", text="")
        subrow = row.row()
        subrow.active = lineart.use_intersection_priority_override
        subrow.prop(lineart, "intersection_priority", text="")


class OBJECT_PT_motion_paths(MotionPathButtonsPanel, Panel):
    # bl_label = "Object Motion Paths"
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object)

    def draw(self, context):
        # layout = self.layout

        ob = context.object
        avs = ob.animation_visualization
        mpath = ob.motion_path

        self.draw_settings(context, avs, mpath)


class OBJECT_PT_motion_paths_display(MotionPathButtonsPanel_display, Panel):
    # bl_label = "Object Motion Paths"
    bl_context = "object"
    bl_parent_id = "OBJECT_PT_motion_paths"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object)

    def draw(self, context):
        # layout = self.layout

        ob = context.object
        avs = ob.animation_visualization
        mpath = ob.motion_path

        self.draw_settings(context, avs, mpath)


class OBJECT_PT_visibility(ObjectButtonsPanel, Panel):
    bl_label = "Visibility"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        return (context.object) and (context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        layout = self.layout
        ob = context.object

        layout.prop(ob, "hide_select", text="Selectable", toggle=False, invert_checkbox=True)

        col = layout.column(heading="Show In")
        col.prop(ob, "hide_viewport", text="Viewports", toggle=False, invert_checkbox=True)
        col.prop(ob, "hide_render", text="Renders", toggle=False, invert_checkbox=True)

        if context.engine == 'BLENDER_EEVEE_NEXT':
            if ob.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'CURVES', 'POINTCLOUD', 'VOLUME'}:
                layout.separator()
                col = layout.column(heading="Ray Visibility")
                col.prop(ob, "visible_camera", text="Camera", toggle=False)
                col.prop(ob, "visible_shadow", text="Shadow", toggle=False)

            if ob.type in {'LIGHT'}:
                layout.separator()
                col = layout.column(heading="Ray Visibility")
                col.prop(ob, "visible_diffuse", text="Diffuse", toggle=False)
                col.prop(ob, "visible_glossy", text="Glossy", toggle=False)
                col.prop(ob, "visible_transmission", text="Transmission", toggle=False)
                col.prop(ob, "visible_volume_scatter", text="Volume Scatter", toggle=False)

            if ob.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'CURVES', 'POINTCLOUD', 'VOLUME'}:
                layout.separator()
                col = layout.column(heading="Light Probes")
                col.prop(ob, "hide_probe_volume", text="Volume", toggle=False, invert_checkbox=True)
                col.prop(ob, "hide_probe_sphere", text="Sphere", toggle=False, invert_checkbox=True)
                col.prop(ob, "hide_probe_plane", text="Plane", toggle=False, invert_checkbox=True)

        if ob.type in {'GPENCIL', 'GREASEPENCIL'}:
            col = layout.column(heading="Grease Pencil")
            col.prop(ob, "use_grease_pencil_lights", toggle=False)

        layout.separator()
        col = layout.column(heading="Mask")
        col.prop(ob, "is_holdout")


class OBJECT_PT_animation(ObjectButtonsPanel, PropertiesAnimationMixin, PropertyPanel, Panel):
    _animated_id_context_property = 'object'


class OBJECT_PT_custom_props(ObjectButtonsPanel, PropertyPanel, Panel):
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    _context_path = "object"
    _property_type = bpy.types.Object


classes = (
    OBJECT_PT_context_object,
    OBJECT_PT_transform,
    OBJECT_OT_align_x,
    OBJECT_OT_align_y,
    OBJECT_OT_align_z,
    OBJECT_OT_align_rotation_x,
    OBJECT_OT_align_rotation_y,
    OBJECT_OT_align_rotation_z,
    OBJECT_OT_align_scale_x,
    OBJECT_OT_align_scale_y,
    OBJECT_OT_align_scale_z,
    OBJECT_PT_delta_transform,
    OBJECT_PT_relations,
    COLLECTION_MT_context_menu,
    OBJECT_PT_collections,
    OBJECT_PT_instancing,
    OBJECT_PT_instancing_size,
    OBJECT_PT_motion_paths,
    OBJECT_PT_motion_paths_display,
    OBJECT_PT_display,
    OBJECT_PT_visibility,
    OBJECT_PT_lineart,
    OBJECT_PT_animation,
    OBJECT_PT_custom_props,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
