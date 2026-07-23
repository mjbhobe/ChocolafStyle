// ==================================================================================
// Form Layout - laying out widgets in a form-style layout
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QComboBox>
#include <QDateTimeEdit>
#include <QFormLayout>
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
  window->setWindowTitle("Qt Layouts | QFormLayout");
  QLineEdit *firstNameLineEdit = new QLineEdit;
  QLineEdit *lastNameLineEdit = new QLineEdit;
  QSpinBox *ageSpinBox = new QSpinBox;
  ageSpinBox->setRange(1, 100);
  QComboBox *employmentStatusComboBox = new QComboBox;
  QStringList employmentStatus = {"Unemployed", "Employed", "NA"};
  employmentStatusComboBox->addItems(employmentStatus);

  // layout the controls on a form
  QFormLayout *layout = new QFormLayout;
  layout->addRow("First Name: ", firstNameLineEdit);
  layout->addRow("Last Name: ", lastNameLineEdit);
  layout->addRow("Age: ", ageSpinBox);
  layout->addRow("Employment Status: ", employmentStatusComboBox);
  window->setLayout(layout);

  window->show();
  return app.exec();
}
