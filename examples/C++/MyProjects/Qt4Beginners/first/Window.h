#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
class QPushButton;
class QLabel;
class QSlider;

class Window : public QWidget {
    Q_OBJECT
public:
    explicit Window(QWidget* parent = nullptr);

private:
    QSlider* m_slider;
    QLabel* m_label;
    QPushButton* m_btn;

signals:
public slots:
};

#endif // WINDOW_H
