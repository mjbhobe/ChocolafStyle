# -*- coding: utf-8 -*-
"""
* icons.py - collects all standard icons into 1 class, so all GUI apps can be
*   standardised to a consistent L&F. Provides most commonly used icons.
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

# from PyQt5.QtGui import QColor, qRgb
from qtpy.QtCore import QObject
import qtawesome as qta


class _ChocolafIconsCache(QObject):
    def __init__(self):
        super(_ChocolafIconsCache, self).__init__()
        self.icons_map = {}
        # file menu standard SVG icons from Material theme
        self.File_New_Icon = qta.icon("mdi6.file-document-outline")
        self.File_Open_Icon = qta.icon("mdi6.folder-open")
        self.File_Save_Icon = qta.icon("mdi6.content-save-outline")
        self.File_SaveAs_Icon = qta.icon("mdi6.content-save-edit-outline")
        self.File_SaveAll_Icon = qta.icon("mdi6.content-save-all-outline")
        self.File_Print_Icon = qta.icon("mdi6.printer")
        self.icons_map["File_New"] = self.File_New_Icon
        self.icons_map["File_Open"] = self.File_Open_Icon
        self.icons_map["File_Save"] = self.File_Save_Icon
        self.icons_map["File_SaveAs"] = self.File_SaveAs_Icon
        self.icons_map["File_SaveAll"] = self.File_SaveAll_Icon
        self.icons_map["File_Print"] = self.File_Print_Icon

        # edit menu standard SVG icons from Material theme
        self.Edit_Undo_Icon = qta.icon("mdi6.undo")
        self.Edit_Redo_Icon = qta.icon("mdi6.redo")
        self.Edit_Cut_Icon = qta.icon("mdi6.content-cut")
        self.Edit_Copy_Icon = qta.icon("mdi6.content-copy")
        self.Edit_Paste_Icon = qta.icon("mdi6.content-paste")
        self.Edit_Delete_Icon = qta.icon("mdi6.trash-can-outline")
        self.Edit_SelectAll_Icon = qta.icon("mdi6.select-all")
        self.icons_map["Edit_Undo"] = self.Edit_Undo_Icon
        self.icons_map["Edit_Redo"] = self.Edit_Redo_Icon
        self.icons_map["Edit_Cut"] = self.Edit_Cut_Icon
        self.icons_map["Edit_Copy"] = self.Edit_Copy_Icon
        self.icons_map["Edit_Paste"] = self.Edit_Paste_Icon
        self.icons_map["Edit_Delete"] = self.Edit_Delete_Icon
        self.icons_map["Edit_SelectAll"] = self.Edit_SelectAll_Icon

        self.Ok_Icon = qta.icon("fa5s.check")
        self.Cancel_Icon = qta.icon("mdi6.close-thick")
        self.Exclamation_Icon = qta.icon("fa5s.exclamation")
        self.Information_Icon = qta.icon("fa5s.question")
        self.icons_map["Ok"] = self.Ok_Icon
        self.icons_map["Cancel"] = self.Cancel_Icon
        self.icons_map["Exclamation"] = self.Exclamation_Icon
        self.icons_map["Information"] = self.Information_Icon

        # alignment
        self.Align_Left_Icon = qta.icon("mdi6.align-horizontal-left")
        self.Align_Right_Icon = qta.icon("mdi6.align-horizontal-right")
        self.Align_Top_Icon = qta.icon("mdi6.align-vertical-top")
        self.Align_Bottom_Icon = qta.icon("mdi6.align-vertical-bottom")
        self.Align_HCenter_Icon = qta.icon("mdi6.align-horizontal-center")
        self.Align_VCenter_Icon = qta.icon("mdi6.align-vertical-center")
        self.Align_HDistribute_Icon = qta.icon("mdi6.distribute-horizontal-center")
        self.Align_VDistribute_Icon = qta.icon("mdi6.distribute-vertical-center")
        self.icons_map["Align_Left"] = self.Align_Left_Icon
        self.icons_map["Align_Right"] = self.Align_Right_Icon
        self.icons_map["Align_Top"] = self.Align_Top_Icon
        self.icons_map["Align_Bottom"] = self.Align_Bottom_Icon
        self.icons_map["Align_HCenter"] = self.Align_HCenter_Icon
        self.icons_map["Align_VCenter"] = self.Align_VCenter_Icon
        self.icons_map["Align_HDistribute"] = self.Align_HDistribute_Icon
        self.icons_map["Align_VDistrubute"] = self.Align_VDistribute_Icon

        self.Format_AlignLeft_Icon = qta.icon("mdi6.format-align-left")
        self.Format_AlignCenter_Icon = qta.icon("mdi6.format-align-center")
        self.Format_AlignRight_Icon = qta.icon("mdi6.format-align-right")
        self.Format_AlignJustify_Icon = qta.icon("mdi6.format-align-justify")
        self.icons_map["Format_AlignLeft"] = self.Format_AlignLeft_Icon
        self.icons_map["Format_AlignCenter"] = self.Format_AlignCenter_Icon
        self.icons_map["Format_AlignRight"] = self.Format_AlignRight_Icon
        self.icons_map["Format_AlignJustify"] = self.Format_AlignJustify_Icon

        # search
        self.Search_Find_Icon = qta.icon("mdi6.magnify")
        self.Search_FindFile_Icon = qta.icon("mdi6.file-find-outline")
        self.Search_Replace_Icon = qta.icon("mdi6.find-replace")
        self.icons_map["Search_Find"] = self.Search_Find_Icon
        self.icons_map["Search_FindFile"] = self.Search_FindFile_Icon
        self.icons_map["Search_Replace"] = self.Search_Replace_Icon

        # zoom
        self.Zoom_In_Icon = qta.icon("mdi6.magnify-plus-outline")
        self.Zoom_Out_Icon = qta.icon("mdi6.magnify-minus-outline")
        self.Zoom_FitWindow_Icon = qta.icon("mdi6.fit-to-screen-outline")
        self.Zoom_ExpandLeft_Icon = qta.icon("mdi6.arrow-expand-left")
        self.Zoom_ExpandUp_Icon = qta.icon("mdi6.arrow-expand-up")
        self.Zoom_ExpandRight_Icon = qta.icon("mdi6.arrow-expand-right")
        self.Zoom_ExpandDown_Icon = qta.icon("mdi6.arrow-expand-down")
        self.Zoom_ExpandAll_Icon = qta.icon("mdi6.arrow-expand-all")
        self.Zoom_CollapseAll_Icon = qta.icon("mdi6.arrow-collapse-all")
        self.icons_map["Zoom_In"] = self.Zoom_In_Icon
        self.icons_map["Zoom_Out"] = self.Zoom_Out_Icon
        self.icons_map["Zoom_FitWindow"] = self.Zoom_FitWindow_Icon
        self.icons_map["Zoom_ExpandLeft"] = self.Zoom_ExpandLeft_Icon
        self.icons_map["Zoom_ExpandUp"] = self.Zoom_ExpandUp_Icon
        self.icons_map["Zoom_ExpandRight"] = self.Zoom_ExpandRight_Icon
        self.icons_map["Zoom_ExpandDown"] = self.Zoom_ExpandDown_Icon
        self.icons_map["Zoom_ExpandAll"] = self.Zoom_ExpandAll_Icon
        self.icons_map["Zoom_CollapseAll"] = self.Zoom_CollapseAll_Icon

        # navigation
        self.Navig_ArrowLeft_Icon = qta.icon("mdi6.arrow-left")
        self.Navig_ArrowUp_Icon = qta.icon("mdi6.arrow-up")
        self.Navig_ArrowRight_Icon = qta.icon("mdi6.arrow-right")
        self.Navig_ArrowDown_Icon = qta.icon("mdi6.arrow-down")
        self.icons_map["Arrow_Left"] = self.Navig_ArrowLeft_Icon
        self.icons_map["Arrow_Up"] = self.Navig_ArrowUp_Icon
        self.icons_map["Arrow_Right"] = self.Navig_ArrowRight_Icon
        self.icons_map["Arrow_Down"] = self.Navig_ArrowDown_Icon

        self.Navig_ChevronLeft_Icon = qta.icon("mdi6.chevron-left")
        self.Navig_ChevronDoubleLeft_Icon = qta.icon("mdi6.chevron-double-left")
        self.Navig_ChevronUp_Icon = qta.icon("mdi6.chevron-up")
        self.Navig_ChevronDoubleUp_Icon = qta.icon("mdi6.chevron-double-up")
        self.Navig_ChevronRight_Icon = qta.icon("mdi6.chevron-right")
        self.Navig_ChevronDoubleRight_Icon = qta.icon("mdi6.chevron-double-right")
        self.Navig_ChevronDown_Icon = qta.icon("mdi6.chevron-down")
        self.Navig_ChevronDoubleDown_Icon = qta.icon("mdi6.chevron-double-down")
        # self.Navig_ChevronPageFirst_Icon = qta.icon("mdi6.page-first")
        # self.Navig_ChevronPageLast_Icon = qta.icon("mdi6.page-last")
        self.icons_map["Chevron_Left"] = self.Navig_ChevronLeft_Icon
        self.icons_map["ChevronDouble_Left"] = self.Navig_ChevronDoubleLeft_Icon
        self.icons_map["Chevron_Up"] = self.Navig_ChevronUp_Icon
        self.icons_map["ChevronDouble_Up"] = self.Navig_ChevronDoubleUp_Icon
        self.icons_map["Chevron_Right"] = self.Navig_ChevronRight_Icon
        self.icons_map["ChevronDouble_Right"] = self.Navig_ChevronDoubleRight_Icon
        self.icons_map["Chevron_Down"] = self.Navig_ChevronDown_Icon
        self.icons_map["ChevronDouble_Down"] = self.Navig_ChevronDoubleDown_Icon

        # rotation
        self.Rotate_Left_Icon = qta.icon("mdi6.rotate-left")
        self.Rotate_Right_Icon = qta.icon("mdi6.rotate-right")
        self.Flip_Left_Icon = qta.icon("mdi6.rotate-left-variant")
        self.Flip_Right_Icon = qta.icon("mdi6.rotate-right-variant")
        self.icons_map["Rotate_Left"] = self.Rotate_Left_Icon
        self.icons_map["Rotate_Right"] = self.Rotate_Right_Icon
        self.icons_map["Flip_Left"] = self.Flip_Left_Icon
        self.icons_map["Flip_Right"] = self.Flip_Right_Icon

    def get_icon(self, icon_key: str) -> qta.icon:
        if icon_key not in self.icons_map.keys():
            raise ValueError("FATAL: {icon_key} is not a valid key!")
        else:
            return self.icons_map[icon_key]


# Global instance of icons class
class ChocolafIconsCacheInstance:
    _iconsCache: _ChocolafIconsCache = None


def get_icon(name: str) -> qta.icon:
    if ChocolafIconsCacheInstance._iconsCache is None:
        ChocolafIconsCacheInstance._iconsCache = _ChocolafIconsCache()
    return ChocolafIconsCacheInstance._iconsCache.get_icon(name)


def get_icon_names() -> list:
    if ChocolafIconsCacheInstance._iconsCache is None:
        ChocolafIconsCacheInstance._iconsCache = _ChocolafIconsCache()
    return list(ChocolafIconsCacheInstance._iconsCache.icons_map.keys())
