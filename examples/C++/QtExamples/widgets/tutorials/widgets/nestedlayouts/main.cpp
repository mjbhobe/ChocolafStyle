/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the documentation of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

//! [main program]
//! [first part]
#include <QtWidgets>

int main(int argc, char *argv[])
{
  QApplication app(argc, argv);
  // apply Chocolaf styling
  QFile f(":chocolaf/chocolaf.css");
  if (!f.exists()) {
    printf("Unable to open stylesheet!");
  }
  else {
    f.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&f);
    app.setStyleSheet(ts.readAll());
  }

  QWidget window;

  QLabel *queryLabel = new QLabel(QApplication::translate("nestedlayouts", "Query:"));
  QLineEdit *queryEdit = new QLineEdit();
  QTableView *resultView = new QTableView();

  QHBoxLayout *queryLayout = new QHBoxLayout();
  queryLayout->addWidget(queryLabel);
  queryLayout->addWidget(queryEdit);

  QVBoxLayout *mainLayout = new QVBoxLayout();
  mainLayout->addLayout(queryLayout);
  mainLayout->addWidget(resultView);
  window.setLayout(mainLayout);

  // Set up the model and configure the view...
  //! [first part]

  //! [set up the model]
  QStandardItemModel model;
  model.setHorizontalHeaderLabels({QApplication::translate("nestedlayouts", "Name"),
                                   QApplication::translate("nestedlayouts", "Office")});

  const QStringList rows[] = {
      QStringList{QStringLiteral("Verne Nilsen"), QStringLiteral("123")},
      QStringList{QStringLiteral("Carlos Tang"), QStringLiteral("77")},
      QStringList{QStringLiteral("Bronwyn Hawcroft"), QStringLiteral("119")},
      QStringList{QStringLiteral("Alessandro Hanssen"), QStringLiteral("32")},
      QStringList{QStringLiteral("Andrew John Bakken"), QStringLiteral("54")},
      QStringList{QStringLiteral("Vanessa Weatherley"), QStringLiteral("85")},
      QStringList{QStringLiteral("Rebecca Dickens"), QStringLiteral("17")},
      QStringList{QStringLiteral("David Bradley"), QStringLiteral("42")},
      QStringList{QStringLiteral("Knut Walters"), QStringLiteral("25")},
      QStringList{QStringLiteral("Andrea Jones"), QStringLiteral("34")}};

  QList<QStandardItem *> items;
  for (const QStringList &row : rows) {
    items.clear();
    for (const QString &text : row)
      items.append(new QStandardItem(text));
    model.appendRow(items);
  }

  resultView->setModel(&model);
  resultView->verticalHeader()->hide();
  resultView->horizontalHeader()->setStretchLastSection(true);
  //! [set up the model]
  //! [last part]
  window.setWindowTitle(QApplication::translate("nestedlayouts", "Nested layouts"));
  window.show();
  return app.exec();
}
//! [last part]
//! [main program]
