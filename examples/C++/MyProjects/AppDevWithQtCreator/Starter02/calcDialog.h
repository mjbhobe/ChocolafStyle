// calcDlg.h - class declaration for simple calculator
//
#ifndef __CalcDlg_h__
#define __CalcDlg_h__

#include <QDialog>

namespace Ui {
  class CalcDialog;
}

class QPushButton;
class QLabel;
class QLineEdit;

class CalcDialog : public QDialog {
    Q_OBJECT
  public:
    explicit CalcDialog(QWidget *parent = nullptr);
    ~CalcDialog() override;
  private slots:
    //void onClose();
    /*
    void onPlusClicked();
    void onMinusClicked();
    void onMultiplyClicked();
    void onDivideClicked();
    */
    void enableOpsBtns();
  private:
    void performOp(char op);
  private:
    Ui::CalcDialog *ui;
    QPushButton *plusBtn, *minusBtn, *multiplyBtn, *divideBtn;
    QPushButton *closeBtn;
    QLineEdit *op1Txt, *op2Txt;
    QLabel *resultLbl;
};

#endif // __CalcDlg_h__
