import bpy.utils.previews
from pathlib import Path


_icons = {}


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    icons_dir = Path(__file__).parent / "images"
    _icons.load(
        name="selected", 
        path=str(icons_dir / "icon_selected.png"), 
        path_type="IMAGE")
    _icons.load(
        name="switch", 
        path=str(icons_dir / "icon_switch.png"), 
        path_type="IMAGE")
    _icons.load(
        name="unmuted", 
        path=str(icons_dir / "icon_unmuted.png"), 
        path_type="IMAGE")
    _icons.load(
        name="addon", 
        path=str(icons_dir / "icon_addon.png"), 
        path_type="IMAGE")


def unregister():
    bpy.utils.previews.remove(_icons)


def get_selected_id():
    return _icons["selected"].icon_id


def get_switch_id():
    return _icons["switch"].icon_id


def get_unmuted_id():
    return _icons["unmuted"].icon_id


def get_addon_id():
    return _icons["addon"].icon_id