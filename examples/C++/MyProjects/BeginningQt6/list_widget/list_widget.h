#ifndef LIST_WIDGET_H
#define LIST_WIDGET_H

#include <QAction>
#include <QListWidget>
#include <QWidget>

class MainWidget : public QWidget {
  Q_OBJECT
public:
  MainWidget(QWidget *parent = nullptr);

protected:
  QListWidget *_list_widget;
  void initializeUi();
  void createActions();
private slots:
  void addItem();
  void insertItem();
  void removeItem();
  void clearItems();

protected:
  QAction *_addAction;
  QAction *_insertAction;
  QAction *_removeAction;
  QAction *_clearAction;
  QAction *_exitAction;
};

#endif // LIST_WIDGET_H
