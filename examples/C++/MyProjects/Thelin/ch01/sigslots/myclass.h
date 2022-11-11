// myclass.h - custom class
#ifndef __MyClass_h__
#define __MyClass_h__

#include <QObject>
#include <QString>
#include <QTextStream>

class MyClass : public QObject {
    Q_OBJECT
  public:
    MyClass(const QString& str, QObject *parent=nullptr);

    const QString& text() const;
    size_t getLengthOfString() const;
    friend QTextStream& operator << (QTextStream& ost, const MyClass& cls);

  public slots:
    void setText(const QString& str);

  signals:
    void textChanged(const QString& str);

  private:
    QString m_string;
};

#endif    // __MyClass_h__
