#ifndef __SysMets_h__
#define __SysMets_h__

#include <windows.h>
#include <QString>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wmissing-braces"

// clang-format off
struct {
   int iIndex;
   const QString szLabel;
   const QString szDesc;
   //const TCHAR *szLabel;
   //const TCHAR *szDesc;
} 
sysmetrics[] = {
   SM_CXSCREEN, QString{"SM_CXSCREEN"}, QString{"Screen width in pixels"},
   SM_CYSCREEN, QString{"SM_CYSCREEN"}, QString{"Screen height in pixels"},
   SM_CXVSCROLL, QString{"SM_CXVSCROLL"}, QString{"Vertical scroll width"},
   SM_CYHSCROLL, QString{"SM_CYHSCROLL"}, QString{"Horizontal scroll height"},
   SM_CYCAPTION, QString{"SM_CYCAPTION"}, QString{"Caption bar height"},
   SM_CXBORDER, QString{"SM_CXBORDER"}, QString{"Window border width"},
   SM_CYBORDER, QString{"SM_CYBORDER"}, QString{"Window border height"},
   SM_CXFIXEDFRAME, QString{"SM_CXFIXEDFRAME"}, QString{"Dialog window frame width"},
   SM_CYFIXEDFRAME, QString{"SM_CYFIXEDFRAME"}, QString{"Dialog window frame height"},
   SM_CYVTHUMB, QString{"SM_CYVTHUMB"}, QString{"Vertical scroll thumb height"},
   SM_CXHTHUMB, QString{"SM_CXHTHUMB"}, QString{"Horizontal scroll thumb width"},
   SM_CXICON, QString{"SM_CXICON"}, QString{"Icon width"},
   SM_CYICON, QString{"SM_CYICON"}, QString{"Icon height"},
   SM_CXCURSOR, QString{"SM_CXCURSOR"}, QString{"Cursor width"},
   SM_CYCURSOR, QString{"SM_CYCURSOR"}, QString{"Cursor height"},
   SM_CYMENU, QString{"SM_CYMENU"}, QString{"Menu bar height"},
   SM_CXFULLSCREEN, QString{"SM_CXFULLSCREEN"}, QString{"Full screen client area width"},
   SM_CYFULLSCREEN, QString{"SM_CYFULLSCREEN"}, QString{"Full screen client area height"},
   SM_CYKANJIWINDOW, QString{"SM_CYKANJIWINDOW"}, QString{"Kanji window height"},
   SM_MOUSEPRESENT, QString{"SM_MOUSEPRESENT"}, QString{"Mouse present flag"},
   SM_CYVSCROLL, QString{"SM_CYVSCROLL"}, QString{"Vertical scroll arrow height"},
   SM_CXHSCROLL, QString{"SM_CXHSCROLL"}, QString{"Horizontal scroll arrow width"},
   SM_DEBUG, QString{"SM_DEBUG"}, QString{"Debug version flag"},
   SM_SWAPBUTTON, QString{"SM_SWAPBUTTON"}, QString{"Mouse buttons swapped flag"},
   SM_CXMIN, QString{"SM_CXMIN"}, QString{"Minimum window width"},
   SM_CYMIN, QString{"SM_CYMIN"}, QString{"Minimum window height"},
   SM_CXSIZE, QString{"SM_CXSIZE"}, QString{"Min/Max/Close button width"},
   SM_CYSIZE, QString{"SM_CYSIZE"}, QString{"Min/Max/Close button height"},
   SM_CXSIZEFRAME, QString{"SM_CXSIZEFRAME"}, QString{"Window sizing frame width"},
   SM_CYSIZEFRAME, QString{"SM_CYSIZEFRAME"}, QString{"Window sizing frame height"},
   SM_CXMINTRACK, QString{"SM_CXMINTRACK"}, QString{"Minimum window tracking width"},
   SM_CYMINTRACK, QString{"SM_CYMINTRACK"}, QString{"Minimum window tracking height"},
   SM_CXDOUBLECLK, QString{"SM_CXDOUBLECLK"}, QString{"Double click x tolerance"},
   SM_CYDOUBLECLK, QString{"SM_CYDOUBLECLK"}, QString{"Double click y tolerance"},
   SM_CXICONSPACING, QString{"SM_CXICONSPACING"}, QString{"Horizontal icon spacing"},
   SM_CYICONSPACING, QString{"SM_CYICONSPACING"}, QString{"Vertical icon spacing"},
   SM_MENUDROPALIGNMENT, QString{"SM_MENUDROPALIGNMENT"}, QString{"Left or right menu drop"},
   SM_PENWINDOWS, QString{"SM_PENWINDOWS"}, QString{"Pen extensions installed"},
   SM_DBCSENABLED, QString{"SM_DBCSENABLED"}, QString{"Double-Byte Char Set enabled"},
   SM_CMOUSEBUTTONS, QString{"SM_CMOUSEBUTTONS"}, QString{"Number of mouse buttons"},
   SM_SECURE, QString{"SM_SECURE"}, QString{"Security present flag"},
   SM_CXEDGE, QString{"SM_CXEDGE"}, QString{"3-D border width"},
   SM_CYEDGE, QString{"SM_CYEDGE"}, QString{"3-D border height"},
   SM_CXMINSPACING, QString{"SM_CXMINSPACING"}, QString{"Minimized window spacing width"},
   SM_CYMINSPACING, QString{"SM_CYMINSPACING"}, QString{"Minimized window spacing height"},
   SM_CXSMICON, QString{"SM_CXSMICON"}, QString{"Small icon width"},
   SM_CYSMICON, QString{"SM_CYSMICON"}, QString{"Small icon height"},
   SM_CYSMCAPTION, QString{"SM_CYSMCAPTION"}, QString{"Small caption height"},
   SM_CXSMSIZE, QString{"SM_CXSMSIZE"}, QString{"Small caption button width"},
   SM_CYSMSIZE, QString{"SM_CYSMSIZE"}, QString{"Small caption button height"},
   SM_CXMENUSIZE, QString{"SM_CXMENUSIZE"}, QString{"Menu bar button width"},
   SM_CYMENUSIZE, QString{"SM_CYMENUSIZE"}, QString{"Menu bar button height"},
   SM_ARRANGE, QString{"SM_ARRANGE"}, QString{"How minimized windows arranged"},
   SM_CXMINIMIZED, QString{"SM_CXMINIMIZED"}, QString{"Minimized window width"},
   SM_CYMINIMIZED, QString{"SM_CYMINIMIZED"}, QString{"Minimized window height"},
   SM_CXMAXTRACK, QString{"SM_CXMAXTRACK"}, QString{"Maximum draggable width"},
   SM_CYMAXTRACK, QString{"SM_CYMAXTRACK"}, QString{"Maximum draggable height"},
   SM_CXMAXIMIZED, QString{"SM_CXMAXIMIZED"}, QString{"Width of maximized window"},
   SM_CYMAXIMIZED, QString{"SM_CYMAXIMIZED"}, QString{"Height of maximized window"},
   SM_NETWORK, QString{"SM_NETWORK"}, QString{"Network present flag"},
   SM_CLEANBOOT, QString{"SM_CLEANBOOT"}, QString{"How system was booted"},
   SM_CXDRAG, QString{"SM_CXDRAG"}, QString{"Avoid drag x tolerance"},
   SM_CYDRAG, QString{"SM_CYDRAG"}, QString{"Avoid drag y tolerance"},
   SM_SHOWSOUNDS, QString{"SM_SHOWSOUNDS"}, QString{"Present sounds visually"},
   SM_CXMENUCHECK, QString{"SM_CXMENUCHECK"}, QString{"Menu check-mark width"},
   SM_CYMENUCHECK, QString{"SM_CYMENUCHECK"}, QString{"Menu check-mark height"},
   SM_SLOWMACHINE, QString{"SM_SLOWMACHINE"}, QString{"Slow processor flag"},
   SM_MIDEASTENABLED, QString{"SM_MIDEASTENABLED"}, QString{"Hebrew and Arabic enabled flag"},
   SM_MOUSEWHEELPRESENT, QString{"SM_MOUSEWHEELPRESENT"}, QString{"Mouse wheel present flag"},
   SM_XVIRTUALSCREEN, QString{"SM_XVIRTUALSCREEN"}, QString{"Virtual screen x origin"},
   SM_YVIRTUALSCREEN, QString{"SM_YVIRTUALSCREEN"}, QString{"Virtual screen y origin"},
   SM_CXVIRTUALSCREEN, QString{"SM_CXVIRTUALSCREEN"}, QString{"Virtual screen width"},
   SM_CYVIRTUALSCREEN, QString{"SM_CYVIRTUALSCREEN"}, QString{"Virtual screen height"},
   SM_CMONITORS, QString{"SM_CMONITORS"}, QString{"Number of monitors"},
   SM_SAMEDISPLAYFORMAT, QString{"SM_SAMEDISPLAYFORMAT"}, QString{"Same color format flag"}
};
// clang-format on
#define NUMLINES ((int) (sizeof sysmetrics / sizeof sysmetrics[0]))

#pragma clang diagnostic pop

#endif // __SysMets_h__
