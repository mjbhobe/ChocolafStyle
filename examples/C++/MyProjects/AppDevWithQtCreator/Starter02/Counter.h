// Counter.h - counter class to illustrate signals & slots
//

#ifndef __Counter_h__
#define __Counter_h__

#include <QObject>

class Counter : public QObject {
    Q_OBJECT
  public:
    explicit Counter(QObject *parent = nullptr)
      : QObject(parent), m_value{0} {
    }
  public slots:
    void setValue(int newValue);
    void increment();
    void decrement();

  signals:
    void valueChanged(int value);
  private:
    int m_value;
};

#endif // __Counter_h__
