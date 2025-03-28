/********************************************************************************
** Form generated from reading UI file 'listDialog.ui'
**
** Created by: Qt User Interface Compiler version 5.15.11
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_LISTDIALOG_H
#define UI_LISTDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_ListDialog
{
public:
    QGridLayout *gridLayout;
    QListWidget *list;
    QVBoxLayout *verticalLayout;
    QPushButton *addButton;
    QPushButton *editButton;
    QPushButton *deleteButton;
    QSpacerItem *verticalSpacer;
    QPushButton *clearButton;

    void setupUi(QDialog *ListDialog)
    {
        if (ListDialog->objectName().isEmpty())
            ListDialog->setObjectName(QString::fromUtf8("ListDialog"));
        ListDialog->resize(400, 300);
        gridLayout = new QGridLayout(ListDialog);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        list = new QListWidget(ListDialog);
        list->setObjectName(QString::fromUtf8("list"));
        list->setFrameShape(QFrame::StyledPanel);
        list->setFrameShadow(QFrame::Sunken);

        gridLayout->addWidget(list, 0, 0, 1, 1);

        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        addButton = new QPushButton(ListDialog);
        addButton->setObjectName(QString::fromUtf8("addButton"));

        verticalLayout->addWidget(addButton);

        editButton = new QPushButton(ListDialog);
        editButton->setObjectName(QString::fromUtf8("editButton"));

        verticalLayout->addWidget(editButton);

        deleteButton = new QPushButton(ListDialog);
        deleteButton->setObjectName(QString::fromUtf8("deleteButton"));

        verticalLayout->addWidget(deleteButton);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);

        clearButton = new QPushButton(ListDialog);
        clearButton->setObjectName(QString::fromUtf8("clearButton"));

        verticalLayout->addWidget(clearButton);


        gridLayout->addLayout(verticalLayout, 0, 1, 1, 1);

        QWidget::setTabOrder(list, addButton);
        QWidget::setTabOrder(addButton, editButton);
        QWidget::setTabOrder(editButton, deleteButton);
        QWidget::setTabOrder(deleteButton, clearButton);

        retranslateUi(ListDialog);
        QObject::connect(clearButton, SIGNAL(clicked()), list, SLOT(clear()));

        QMetaObject::connectSlotsByName(ListDialog);
    } // setupUi

    void retranslateUi(QDialog *ListDialog)
    {
        ListDialog->setWindowTitle(QCoreApplication::translate("ListDialog", "Phone Book", nullptr));
        addButton->setText(QCoreApplication::translate("ListDialog", "Add New", nullptr));
        editButton->setText(QCoreApplication::translate("ListDialog", "Edit", nullptr));
        deleteButton->setText(QCoreApplication::translate("ListDialog", "Delete", nullptr));
        clearButton->setText(QCoreApplication::translate("ListDialog", "Clear All", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ListDialog: public Ui_ListDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_LISTDIALOG_H
