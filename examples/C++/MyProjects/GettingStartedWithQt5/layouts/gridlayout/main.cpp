// ==================================================================================
// Grid Layouts - laying out widgets in a grid layout
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QComboBox>
#include <QDateTimeEdit>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QSpinBox>
#include <QStringList>

int main(int argc, char *argv[])
{
  QApplication app(argc, argv);

  // create the UI
  QWidget *window = new QWidget;
  window->setWindowTitle("Qt Layouts | QGridLayout");

  // instantiate your widgets
  QLabel *nameLabel = new QLabel("Open Happiness");
  QLineEdit *firstNameLineEdit = new QLineEdit;
  firstNameLineEdit->setToolTip("Enter first name");
  QLineEdit *lastNameLineEdit = new QLineEdit;
  lastNameLineEdit->setToolTip("Enter last name");
  QSpinBox *ageSpinBox = new QSpinBox;
  ageSpinBox->setToolTip("Enter age");
  ageSpinBox->setRange(1, 100);
  QComboBox *employmentStatusComboBox = new QComboBox;
  QStringList employmentStatus = {"Unemployed", "Employed", "NA"};
  employmentStatusComboBox->addItems(employmentStatus);

  // layout the widgets on grid
  QGridLayout *layout = new QGridLayout;
  layout->addWidget(nameLabel, 0, 0);
  layout->addWidget(firstNameLineEdit, 0, 1);
  layout->addWidget(lastNameLineEdit, 0, 2);
  layout->addWidget(ageSpinBox, 1, 0);
  layout->addWidget(employmentStatusComboBox, 1, 1, 1, 2);
  window->setLayout(layout);

  window->show();
  return app.exec();
}
