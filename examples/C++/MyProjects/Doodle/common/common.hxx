// common.hxx : helper function declarations
#ifndef __common_hxx__
#define __common_hxx__

#include <QApplication>
#include <QTextStream>
#include <QColor>
#include <QPalette>
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream &operator<<(QTextStream &ost, const mpz_class &c);
QColor getPaletteColor(QPalette::ColorRole colorRole, QPalette::ColorGroup colorGroup = QPalette::Active);

#ifdef Q_OS_WINDOWS
// some common functions
bool windowsDarkThemeAvailable();
bool windowsIsInDarkTheme();
void setWinDarkPalette(QApplication *app);
#endif // Q_OS_WINDOWS

#endif // __common_hxx__
