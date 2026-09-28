#ifndef __constants_h__
#define __constants_h__

// defining global constant
#include <QString>

inline const QString AppTitle("Qt Scribble");
inline const QString WindowTitle = QString(
  "Qt %1 Doodle - Step08: Adding Actions + Menus + Handlers"
).arg(QT_VERSION_STR);

#endif // __constants_h__
