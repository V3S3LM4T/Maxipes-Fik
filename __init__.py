bl_info = {
    "name": "MaxipesFik",
    "description": "Najde objekty s negativním měřítkem a nahlásí v panelu.",
    "author": "V3S3LM4T",
    "version": (5, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N-Panel > MaxipesFik",
    "category": "Object",
}

import bpy
import bpy.utils.previews
import os

custom_icons = None

class OBJECT_OT_najdi_negativni_scale(bpy.types.Operator):
    bl_idname = "object.najdi_negativni_scale" 
    bl_label = "Vypustit Fíka!"
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.name.startswith("Detektiv_Majak"):
                bpy.data.objects.remove(obj, do_unlink=True)
                
        bpy.ops.object.select_all(action='DESELECT')
        pocet_chyb = 0
        
        for objekt in context.scene.objects:
            if objekt.type == 'MESH':
                if objekt.scale.x < 0 or objekt.scale.y < 0 or objekt.scale.z < 0:
                    objekt.select_set(True)
                    pocet_chyb += 1
        
        context.scene.fik_pocet_chyb = pocet_chyb
        context.scene.fik_hledal = True
        
        return {'FINISHED'} 


class VIEW3D_PT_muj_detektiv(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Inspektor Fík"
    bl_label = "Maxipes Fik"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.najdi_negativni_scale", icon='VIEWZOOM')
        
        if context.scene.fik_hledal:
            global custom_icons
            box = layout.box()
            pocet = context.scene.fik_pocet_chyb
            
            if pocet > 0:
                # Blok pro chybový stav
                box.label(text=f"Fík našel {pocet} rozbitých objektů!", icon='ERROR')
                box.label(text="Oprav je pomocí: Ctrl + A -> Scale", icon='INFO')
                
                if "hlavni_pes" in custom_icons:
                    box.template_icon(icon_value=custom_icons["hlavni_pes"].icon_id, scale=8.0)
            else:
                # Blok pro čistý stav
                box.label(text="Vše čisté! Fík má radost.", icon='CHECKMARK')
                
                if "stastny_pes" in custom_icons:
                    box.template_icon(icon_value=custom_icons["stastny_pes"].icon_id, scale=8.0)


def register():
    bpy.types.Scene.fik_pocet_chyb = bpy.props.IntProperty(default=0)
    bpy.types.Scene.fik_hledal = bpy.props.BoolProperty(default=False)
    
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    
    cesta_k_slozce = os.path.dirname(__file__)
    cesta_k_obrazku_chyba = os.path.join(cesta_k_slozce, "maxipes_fik.png")
    # Zde je tvůj placeholder pro druhý obrázek:
    cesta_k_obrazku_cisto = os.path.join(cesta_k_slozce, "stastny_fik.png") 
    
    if os.path.exists(cesta_k_obrazku_chyba):
        custom_icons.load("hlavni_pes", cesta_k_obrazku_chyba, 'IMAGE')
        
    if os.path.exists(cesta_k_obrazku_cisto):
        custom_icons.load("stastny_pes", cesta_k_obrazku_cisto, 'IMAGE')
    
    bpy.utils.register_class(OBJECT_OT_najdi_negativni_scale)
    bpy.utils.register_class(VIEW3D_PT_muj_detektiv)

def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    
    del bpy.types.Scene.fik_pocet_chyb
    del bpy.types.Scene.fik_hledal
    
    bpy.utils.unregister_class(OBJECT_OT_najdi_negativni_scale)
    bpy.utils.unregister_class(VIEW3D_PT_muj_detektiv)

if __name__ == "__main__":
    register()
