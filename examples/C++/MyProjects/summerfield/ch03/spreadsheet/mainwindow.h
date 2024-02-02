// ch03/spreadsheet/mainwindow.h
#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class QAction;
class QLabel;
class FindDialog;
class Spreadsheet;

class MainWindow : public QMainWindow
{
    Q_OBJECT
  public:
    MainWindow();

  protected:
    void closeEvent(QCloseEvent *event);

  public slots:
    void newFile();
    void open();
    void save();
    void saveAs();
    void find();
    void goToCell();
    void sort();
    void about();
    void openRecentFile();
    void updateStatusBar();
    void spreadSheetModified();

  private:
    void createActions();
    void createMenus();
    void createContextMenu();
    void createToolBars();
    void createStatusBar();
    void readSettings();
    void writeSettings();
    bool okToContinue();
    bool loadFile(const QString& fileName);
    bool saveFile(const QString& fileName);
    void setCurrentFile(const QString& fileName);
    void updateRecentFileActions();
    QString strippedName(const QString& fullFileName);

    // variables
    Spreadsheet *spreadSheet;
    FindDialog *findDialog;
    QLabel *locationLabel;
    QLabel *formulaLabel;
    QStringList recentFiles;
    QString curFile;

    enum { MaxRecentFiles = 5};
    QAction *recentFileActions[MaxRecentFiles];
    QAction *separatorAction;
    QMenu *fileMenu;
    QMenu *editMenu;
};

#endif  // __MainWindow_h__
