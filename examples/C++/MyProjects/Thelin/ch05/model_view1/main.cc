// Qt/C++ - Model View basics
// main.cc - displays a window with QTreeView, QListView & QTableView
//  all showing data from a QStandardModel
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

int main(int argc, char **argv)
{
   QApplication app(argc, argv);
   app.setStyle("Fusion");

   // create & show the GUI
   QTreeView *tree = new QTreeView();
   QListView *list = new QListView();
   QTableView *table = new QTableView();

   // create a splitter to hold the views
   QSplitter *splitter = new QSplitter();
   splitter->addWidget(tree);
   splitter->addWidget(list);
   splitter->addWidget(table);

   // create the standard model - data in 5 rows
   QStandardItemModel model(5, 3);
   for (int r = 0; r < 5; ++r) {
      for (int c = 0; c < 3; ++c) {
         QStandardItem *item = 
            new QStandardItem(QString("Row:%1, Col:%2").arg(r).arg(c));

         // create sub-items (will be used in QTreeView only!)
         if (c == 0)
            for (int i = 0; i < 3; ++i) {
               QStandardItem *child = new QStandardItem(QString("Item %1").arg(i));
               child->setEditable(false);
               item->appendRow(child);
            }
         model.setItem(r, c, item);
      }
   }
   model.setHorizontalHeaderItem(0, new QStandardItem("Name"));
   model.setHorizontalHeaderItem(1, new QStandardItem("Address"));
   model.setHorizontalHeaderItem(2, new QStandardItem("Phone"));

   // set model as the model for all the views
   tree->setModel(&model);
   list->setModel(&model);
   table->setModel(&model);

   // synch selections across all item views
   list->setSelectionModel(tree->selectionModel());
   table->setSelectionModel(tree->selectionModel());

   QWidget *mainWindow = new QWidget();
   mainWindow->setWindowTitle(QString("Qt %1 ItemView demos").arg(QT_VERSION_STR));
   QVBoxLayout *layout = new QVBoxLayout;
   layout->addWidget(splitter);
   mainWindow->setLayout(layout);
   mainWindow->show();

   return app.exec();
}


