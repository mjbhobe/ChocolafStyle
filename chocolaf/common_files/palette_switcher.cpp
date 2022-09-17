#include <QApplication>
#include <QColor>
#include <QPalette>

#include "palette_switcher.h"

#ifdef Q_OS_WINDOWS

// --------------------------------------------------------------------------------------------
// PaletteSwitcher class
//

PaletteSwitcher::PaletteSwitcher(QApplication *appInstance, QObject *parent /*=nullptr*/)
   : QObject(parent), _appInstance{appInstance}, _darkPalette{new QPalette()}, _lightPalette{new QPalette()},
     darkPaletteInUse{false}
{
   Q_ASSERT(appInstance != nullptr);
   initializePalettes();
   darkPaletteInUse = (windowsDarkThemeAvailable() && windowsIsInDarkTheme());
   if (darkPaletteInUse)
      _appInstance->setPalette(*_darkPalette);
   else
      _appInstance->setPalette(*_lightPalette);
}

PaletteSwitcher::~PaletteSwitcher()
{
   delete _lightPalette;
   delete _darkPalette;
}

void PaletteSwitcher::swapPalettes()
{
   if (darkPaletteInUse)
      _appInstance->setPalette(*_lightPalette);
   else
      _appInstance->setPalette(*_darkPalette);
   darkPaletteInUse = !darkPaletteInUse;
}

void PaletteSwitcher::initializePalettes()
{
   Q_ASSERT(_darkPalette != nullptr);
   _darkPalette->setColor(QPalette::Window, QColor(53, 53, 53));
   _darkPalette->setColor(QPalette::WindowText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::WindowText, QColor(127, 127, 127));
   _darkPalette->setColor(QPalette::Base, QColor(42, 42, 42));
   _darkPalette->setColor(QPalette::AlternateBase, QColor(66, 66, 66));
   _darkPalette->setColor(QPalette::ToolTipBase, Qt::white);
   _darkPalette->setColor(QPalette::ToolTipText, QColor(53, 53, 53));
   _darkPalette->setColor(QPalette::Text, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::Text, QColor(127, 127, 127));
   _darkPalette->setColor(QPalette::Dark, QColor(35, 35, 35));
   _darkPalette->setColor(QPalette::Shadow, QColor(20, 20, 20));
   _darkPalette->setColor(QPalette::Button, QColor(53, 53, 53));
   _darkPalette->setColor(QPalette::ButtonText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::ButtonText, QColor(127, 127, 127));
   _darkPalette->setColor(QPalette::BrightText, Qt::red);
   _darkPalette->setColor(QPalette::Link, QColor(42, 130, 218));
   _darkPalette->setColor(QPalette::Highlight, QColor(42, 130, 218));
   _darkPalette->setColor(QPalette::Disabled, QPalette::Highlight, QColor(80, 80, 80));
   _darkPalette->setColor(QPalette::HighlightedText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(127, 127, 127));

   Q_ASSERT(_lightPalette != nullptr);
   _lightPalette->setColor(QPalette::Window, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::WindowText, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::WindowText, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::Base, Qt::white);
   _lightPalette->setColor(QPalette::AlternateBase, QColor(233, 231, 227));
   _lightPalette->setColor(QPalette::ToolTipBase, QColor(255, 255, 220));
   _lightPalette->setColor(QPalette::ToolTipText, Qt::black);
   _lightPalette->setColor(QPalette::Text, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::Text, QColor(120, 120, 120));
   _lightPalette->setColor(QPalette::Dark, QColor(160, 160, 160));
   _lightPalette->setColor(QPalette::Shadow, QColor(105, 105, 105));
   _lightPalette->setColor(QPalette::Button, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::ButtonText, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::ButtonText, QColor(78, 78, 78));
   _lightPalette->setColor(QPalette::BrightText, Qt::white);
   _lightPalette->setColor(QPalette::Link, QColor(0, 0, 255));
   _lightPalette->setColor(QPalette::Highlight, QColor(0, 120, 215));
   _lightPalette->setColor(QPalette::Disabled, QPalette::Highlight, QColor(0, 120, 215));
   _lightPalette->setColor(QPalette::HighlightedText, Qt::white);
   _lightPalette->setColor(QPalette::Disabled, QPalette::HighlightedText, Qt::white);
}

#endif
