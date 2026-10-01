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

# Sem budeme ukládat naše vlastní ikonky psa
custom_icons = None

class OBJECT_OT_najdi_negativni_scale(bpy.types.Operator):
    bl_idname = "object.najdi_negativni_scale" 
    bl_label = "Vypustit Fíka!"
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        # 1. Odznačíme všechno ve scéně, ať máme čistý stůl pro nový výběr
        bpy.ops.object.select_all(action='DESELECT')
        pocet_chyb = 0
        
        # 2. Projdeme všechny objekty ve scéně jeden po druhém
        for objekt in context.scene.objects:
            # Zajímá nás jen 3D geometrie (Mesh), u světel nebo kamer scale tolik nevadí
            if objekt.type == 'MESH':
                # Zkontrolujeme, jestli je nějaká osa převrácená (menší než nula)
                if objekt.scale.x < 0 or objekt.scale.y < 0 or objekt.scale.z < 0:
                    objekt.select_set(True) # Fík objekt chytí (označí)
                    pocet_chyb += 1         # Zapíšeme si další chybu do bloku
        
        # 3. Uložíme výsledky pátrání do paměti scény, aby si je mohl panel přečíst
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
        
        # Hlavní tlačítko pátrače
        layout.operator("object.najdi_negativni_scale", icon='VIEWZOOM')
        
        # Zobrazit výsledky pouze pokud už proběhlo hledání
        if context.scene.fik_hledal:
            global custom_icons
            box = layout.box()
            pocet = context.scene.fik_pocet_chyb
            
            if pocet > 0:
                # Našli jsme chyby - zobrazíme varování a rozzlobeného psa
                box.label(text=f"Fík našel {pocet} rozbitých objektů!", icon='ERROR')
                box.label(text="Oprav je pomocí: Ctrl + A -> Scale", icon='INFO')
                
                if custom_icons and "hlavni_pes" in custom_icons:
                    box.template_icon(icon_value=custom_icons["hlavni_pes"].icon_id, scale=8.0)
            else:
                # Vše je v pořádku - zobrazíme radost
                box.label(text="Vše čisté! Fík má radost.", icon='CHECKMARK')
                
                if custom_icons and "stastny_pes" in custom_icons:
                    box.template_icon(icon_value=custom_icons["stastny_pes"].icon_id, scale=8.0)


def register():
    # Vytvoření proměnných přímo ve scéně, aby nezmizely
    bpy.types.Scene.fik_pocet_chyb = bpy.props.IntProperty(default=0)
    bpy.types.Scene.fik_hledal = bpy.props.BoolProperty(default=False)
    
    # Příprava na načtení ikonek z disku
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    
    # Zjistíme, kde přesně je tento Python soubor uložen na disku
    cesta_k_slozce = os.path.dirname(__file__)
    cesta_k_obrazku_chyba = os.path.join(cesta_k_slozce, "maxipes_fik.png")
    cesta_k_obrazku_cisto = os.path.join(cesta_k_slozce, "stastny_fik.png") 
    
    # Pokud obrázky fyzicky existují, načteme je do paměti Blenderu
    if os.path.exists(cesta_k_obrazku_chyba):
        custom_icons.load("hlavni_pes", cesta_k_obrazku_chyba, 'IMAGE')
    if os.path.exists(cesta_k_obrazku_cisto):
        custom_icons.load("stastny_pes", cesta_k_obrazku_cisto, 'IMAGE')
    
    # Zaregistrujeme třídy do systému
    bpy.utils.register_class(OBJECT_OT_najdi_negativni_scale)
    bpy.utils.register_class(VIEW3D_PT_muj_detektiv)

def unregister():
    global custom_icons
    if custom_icons:
        bpy.utils.previews.remove(custom_icons)
    
    # Poctivý úklid - smažeme po sobě proměnné, když se doplněk vypne
    del bpy.types.Scene.fik_pocet_chyb
    del bpy.types.Scene.fik_hledal
    
    bpy.utils.unregister_class(OBJECT_OT_najdi_negativni_scale)
    bpy.utils.unregister_class(VIEW3D_PT_muj_detektiv)

if __name__ == "__main__":
    register()
