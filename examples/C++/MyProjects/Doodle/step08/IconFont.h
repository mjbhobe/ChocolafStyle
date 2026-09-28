//
// Created by mjbhobe on 27-Sept-26.
//

#ifndef __ICONFONT_H__
#define __ICONFONT_H__

#include <QApplication>
#include <QFontDatabase>
#include <QIcon>
#include <QPainter>
#include <QPalette>
#include <QString>
#include <QDebug>

namespace IconFont {
  // Material Symbol Codepoints we'll be using (char32_t / UTF-32 hex)
  namespace Icons {
    inline constexpr char32_t FileNew = 0xe873;    // description / file
    inline constexpr char32_t FileOpen = 0xe2c8;   // folder_open
    inline constexpr char32_t FileSave = 0xe161;   // save
    inline constexpr char32_t FileSaveAs = 0xe173; // save_as
    inline constexpr char32_t ColorLens = 0xe3b7;  // color_lens
    inline constexpr char32_t Palette = 0xe40a;    // palette
    inline constexpr char32_t LineWeight = 0xe91a; //0xe22b; // line_weight / pen width
    inline constexpr char32_t Clear = 0xe14c;      // clear
    inline constexpr char32_t Undo = 0xe166;       // undo
    inline constexpr char32_t Redo = 0xe15a;       // redo
    inline constexpr char32_t Close = 0xe5cd;      // close
    inline constexpr char32_t Settings = 0xe8b8;   // settings
    inline constexpr char32_t Info = 0xe88e;       // info
  }

  inline QString s_fontFamily;

  inline bool initFont()
  {
    int fontId = QFontDatabase::addApplicationFont(":/fonts/material_icons.ttf");
    if (fontId == -1) {
      qWarning() << "IconFont::initFont() - Could not load :/fonts/material_icons.ttf";
      return false;
    }

    const QStringList families = QFontDatabase::applicationFontFamilies(fontId);
    if (families.isEmpty()) {
      qWarning() << "IconFont::initFont() - No font families identified in loaded font file.";
      return false;
    }

    s_fontFamily = families.first();
    return true;
  }

  // Builds a multi-resolution, theme-aware QIcon
  inline QIcon getIcon(char32_t codePoint, int baseSize = 24)
  {
    QIcon icon;
    if (s_fontFamily.isEmpty()) {
      qWarning() << "IconFont::getIcon() called before initFont() succeeded.";
      return icon;
    }

    const int renderSizes[] = {baseSize, baseSize * 2};
    const QColor activeColor = QApplication::palette().color(QPalette::WindowText);
    const QColor disabledColor = QApplication::palette().color(
      QPalette::Disabled, QPalette::WindowText
    );
    const QString glyph = QString::fromUcs4(&codePoint, 1);

    for (int size : renderSizes) {
      // Normal state pixmap
      {
        QPixmap pix(size, size);
        pix.fill(Qt::transparent);

        QPainter painter(&pix);
        painter.setRenderHint(QPainter::Antialiasing);
        painter.setRenderHint(QPainter::TextAntialiasing);

        QFont font(s_fontFamily);
        font.setPixelSize(static_cast<int>(size * 0.85));
        painter.setFont(font);
        painter.setPen(activeColor);

        painter.drawText(pix.rect(), Qt::AlignCenter, glyph);
        icon.addPixmap(pix, QIcon::Normal, QIcon::Off);
      }

      // Disabled state pixmap
      {
        QPixmap disabledPix(size, size);
        disabledPix.fill(Qt::transparent);

        QPainter painter(&disabledPix);
        painter.setRenderHint(QPainter::Antialiasing);
        painter.setRenderHint(QPainter::TextAntialiasing);

        QFont font(s_fontFamily);
        font.setPixelSize(static_cast<int>(size * 0.85));
        painter.setFont(font);
        painter.setPen(disabledColor);

        painter.drawText(disabledPix.rect(), Qt::AlignCenter, glyph);
        icon.addPixmap(disabledPix, QIcon::Disabled, QIcon::Off);
      }
    }

    return icon;
  }

  // Computes a comfortable toolbar icon size based on screen scaling & DPI
  inline QSize getRecommendedToolbarIconSize(QWidget* window = nullptr)
  {
    QScreen* screen = nullptr;
    if (window && window->windowHandle()) {
      screen = window->windowHandle()->screen();
    }
    if (!screen) {
      screen = QGuiApplication::primaryScreen();
    }

    // Baseline size for normal 96-DPI 1080p screens
    int baseSize = 28;

    if (screen) {
      qreal dpi = screen->logicalDotsPerInch();
      // Standard non-HiDPI desktop DPI is 96.0
      qreal scaleFactor = dpi / 96.0;

      qDebug() << "NOTE: screen dpi -> " << dpi << " scaleFactor -> " << scaleFactor;

      // If running on a 2K/4K high-density screen or fractionally scaled Plasma
      if (scaleFactor > 1.25) {
        baseSize = static_cast<int>(baseSize * (scaleFactor > 2.0 ? 1.5 : 1.25));
      }
    }

    return QSize(baseSize, baseSize);
  }
} // namespace IconFont

#endif //__ICONFONT_H__
