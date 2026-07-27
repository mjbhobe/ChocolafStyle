#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>
#include <tuple>

class QMenu;
class QAction;
class QLabel;
class QToolBar;
class QLineEdit;
class QDateEdit;
class QPushButton;
class QWidget;
class QTableView;
class QStandardItemModel;
class QVBoxLayout;
class QCloseEvent;

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    MainWindow();
    ~MainWindow() override = default;
  protected:
    // overridden to save data displayed in QTableView
    void closeEvent(QCloseEvent *e) override;
  private:
    void createActions();
    void createMenus();
    void createToolBar();
    void setupCentralWidget();
    QVBoxLayout *createDataEntryForm();
    QTableView *createTableView();
    void applyLocaleWith4DigitYear(QDateEdit *dateEdit);
    bool saveData();
    std::tuple<bool, QStandardItemModel *> loadData(QObject *parent = nullptr);


    QWidget *m_centralWidget;
    QLineEdit *m_txtName;
    QDateEdit *m_txtDob;
    QLineEdit *m_txtPhoneNo;
    QTableView *m_tableView;
    QStandardItemModel *m_tableModel;
    QPushButton *m_btnSave;
    QPushButton *m_btnClearAll;
    // menus & actions
    QMenu *m_fileMenu;
    QMenu *m_helpMenu;
    QToolBar *m_toolBar;
    QAction *m_newAction;
    QAction *m_openAction;
    QAction *m_saveAction;
    QAction *m_quitAction;
    QAction *m_clearAction;
    QAction *m_aboutAction;
    QAction *m_aboutQtAction;

  private slots:
    void fileNew();
    void fileOpen();
    void saveRecord();
    void clearFields();
    void about();
};


#endif // __MainWindow_h__
