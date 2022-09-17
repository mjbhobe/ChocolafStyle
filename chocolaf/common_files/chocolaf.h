// ---------------------------------------------------------------------
// chocolaf.h - declare helper ChocolafApp & ChocolafPalette classes
// @author: Manish Bhobe
//
// Chocolaf - dark chocolate custom stylesheet for Qt/PyQt applications
// ---------------------------------------------------------------------
#ifndef __Chocolaf_Style_h__
#define __Chocolaf_Style_h__

#include <QApplication>
#include <QColor>
#include <QPalette>
#include <QString>

namespace Chocolaf {

   namespace ChocolafPalette {
      // default background color for all widgets
      const QColor Window_Color = QColor(qRgb(42, 42, 42));
      // default foreground color for text
      const QColor WindowText_Color = QColor(qRgb(220, 220, 220));
      // background for text entry widgets
      const QColor Base_Color = QColor(qRgb(52, 52, 52));
      // foreground color to use with Base
      const QColor Text_Color = QColor(qRgb(220, 220, 220));
      // background color for views with alternating lors
      const QColor AlternateBase_Color = QColor(qRgb(62, 62, 62));
      // background color for tooltips
      const QColor ToolTipBase_Color = QColor(qRgb(224, 227, 176));
      // text color for tooltips
      const QColor ToolTipText_Color = QColor(qRgb(0, 0, 0));
      // pushbutton background color
      const QColor Button_Color = QColor(qRgb(62, 62, 62));
      // button text color
      const QColor ButtonText_Color = QColor(qRgb(220, 220, 220));
      // HTML link color
      const QColor Link_Color = QColor(qRgb(0, 0, 255));
      // visited link color
      const QColor LinkVisited_Color = QColor(qRgb(255, 0, 255));
      // background color of highlight (or selected) text or item
      const QColor Highlight_Color = QColor(qRgb(0, 114, 198));
      // foreground color of highlight (or selected) text or item
      const QColor HighlightedText_Color = QColor(qRgb(220, 220, 220));
      // disabled text foreground color
      const QColor Disabled_Text_Color = QColor(qRgb(127, 127, 127));
      // disabled pushbutton foreground color
      const QColor Disabled_ButtonText_Color = QColor(qRgb(127, 127, 127));
      // disabled window text color
      const QColor Disabled_WindowText_Color = QColor(qRgb(127, 127, 127));
      // faded text color (used for grid line color)
      const QColor Disabled_Light_Color = QColor(qRgb(102, 102, 102));
   } // namespace ChocolafPalette

   // extern const struct __ChocolafPalette ChocolafPalette;
   extern const QString __version__;
   extern const QString __author__;

   QPalette *getPalette();
   void setStyleSheet(QApplication &app);

   /* NOTE:
      deriving a custom application class from QApplication does not
      seem to be working on my instance of Manjaro Linux - could be a Qt plugin issue,
      which I am unable to debug and resolve
      Hence I have resorted to global functions in the Chocolaf namespace as a
      workaround
    */

   /*
   class ChocolafApp : public QApplication
   {
    public:
      ChocolafApp(int argc, char *argv[]);
      ~ChocolafApp();

      // valid options are Chocolaf, Fusion, windowsvista and Windows
      void setStyle(const QString &styleName);

    protected:
      QPalette *_palette;
      QString _styleSheet;

      QString loadStyleSheet();
      // in this version, we'll keep it simple & assume only Chocolaf style.
      // In later versions, we can add more styles
      QPalette *getPalette(/ *const QString &key = "Chocolaf"* /);
      // QPalette *getStylesheet(/ *const QString &key = "Chocolaf"* /);
    };
    */

} // namespace Chocolaf

#endif // __Chocolaf_Style_h__
