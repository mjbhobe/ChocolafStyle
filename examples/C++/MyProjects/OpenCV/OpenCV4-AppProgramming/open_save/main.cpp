#include "common_funcs.h"
#include <QCoreApplication>
#include <QTextStream>
// openCV headers
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#ifdef USING_QT6
static QTextStream cout(stdout, QIODeviceBase::WriteOnly);
#else
static QTextStream cout(stdout, QIODevice::WriteOnly);
#endif

void onMouse(int event, int x, int y, int flags, void *param);

void displayImage(cv::Mat &image, const QString &window_name)
{
  cv::namedWindow(window_name.toStdString().c_str());
  // mouse callback
  cv::setMouseCallback(window_name.toStdString().c_str(), onMouse,
                       reinterpret_cast<void *>(&image));
  cv::imshow(window_name.toStdString().c_str(), image);
  cv::waitKey(0);
}

void onMouse(int event, int x, int y, int flags, void *param)
{
  cv::Mat *image = reinterpret_cast<cv::Mat *>(param);
  switch (event) {
    case cv::EVENT_LBUTTONDOWN:
      // left mouse clicked - display (x, y) co-ords
      cout << "Click at (" << x << ", " << y
           << ") value is: " << static_cast<int>(image->at<uchar>(cv::Point(x, y)))
           << Qt::endl;
      break;
  }
}

int main(int argc, char *argv[])
{
  QCoreApplication a(argc, argv);

  auto image_path = "/home/mjbhobe/code/git-projects/learning_Qt/bogo2bogo/ChocolafStyle/"
                    "examples/C++/MyProjects/OpenCV/images/cat-1.jpg";

  cv::Mat image; // an empty image
  cout << "Empty image has " << image.rows << " rows & " << image.cols << " cols "
       << image.channels() << " channels." << Qt::endl;
  // load the image
  image = cv::imread(image_path, cv::IMREAD_COLOR);
  if (image.empty()) {
    cout << "FATAL ERROR:  unable to load image!" << Qt::endl;
    return -1;
  } else {
    cout << "Loaded image dimensions: " << image.rows << " x " << image.cols << " x "
         << image.channels() << Qt::endl;
    // display image in named window
    displayImage(image, QString("A cat"));
  }
  return 0;
  // return a.exec();
}
