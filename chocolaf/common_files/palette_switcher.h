#ifndef __Palette_Switcher_h__
#define __Palette_Switcher_h__

#include <QApplication>
#include <QColor>
#include <QPalette>


#ifdef Q_OS_WINDOWS

class PaletteSwitcher : public QObject
{
   Q_OBJECT
 protected:
   QApplication *_appInstance;
   QPalette *_darkPalette, *_lightPalette;
   bool darkPaletteInUse;

   void initializePalettes();

 public:
   PaletteSwitcher(QApplication *appInstance, QObject *parent = nullptr);
   ~PaletteSwitcher();

   void setDarkPalette()
   {
      Q_ASSERT(_darkPalette != nullptr);
      Q_ASSERT(_appInstance != nullptr);
      // WARNING: this does not appear to refresh all colors immediately
      _appInstance->setPalette(*_darkPalette);
      darkPaletteInUse = true;
   }

   void setLightPalette()
   {
      Q_ASSERT(_lightPalette != nullptr);
      Q_ASSERT(_appInstance != nullptr);
      // WARNING: this does not appear to refresh all colors immediately
      _appInstance->setPalette(*_lightPalette);
      darkPaletteInUse = false;
   }
   bool isDarkPaletteInUse() const { return darkPaletteInUse; }
   void swapPalettes();
};

#else

/**** on non-Windows platform, do nothing!! ****/

// dummy class for non Windows platforms - does nothing!!
class PaletteSwitcher : public QObject
{
   Q_OBJECT
 protected:
   QPalette *_darkPalette, *_lightPalette;
   bool darkPaletteInUse;
   QApplication *_appInstance;
   void initializePalettes() {}

 public:
   PaletteSwitcher(QApplication *appInstance, QObject *parent = nullptr) : QObject(parent)
   {
      _appInstance = appInstance;
      qDebug() << "Warning: this is a do-nothing class on non-Windows platforms!";
   }
   ~PaletteSwitcher() {}

   void setDarkPalette()
   {
      // do nothing
   }

   void setLightPalette()
   {
      // do nothing
   }
   void swapPalettes()
   {
      // do nothing
   }
};

#endif // Q_OS_WINDOWS


#endif   // __Palette_Switcher_h__
