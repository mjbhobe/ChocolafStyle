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

int main(int argc, char *argv[])
{
  QCoreApplication a(argc, argv);

  auto image_path = "/home/mjbhobe/code/git-projects/learning_Qt/bogo2bogo/ChocolafStyle/"
                    "examples/C++/MyProjects/OpenCV/images/puppy.bmp";

  // create names windows to display images in
  cv::namedWindow("Image 1");
  cv::namedWindow("Image 2");
  cv::namedWindow("Image 3");
  cv::namedWindow("Image 4");
  cv::namedWindow("Image 5");
  cv::namedWindow("Image");

  // create an image with all pixels initialized to 200
  cv::Mat image1(240, 320, CV_8U, 100);
  cv::imshow("Image", image1);
  cv::waitKey(0);

  // re-allocate the image
  image1.create(200, 200, CV_8U);
  image1 = 200;
  cv::imshow("Image", image1);
  cv::waitKey(0);

  // create a red-pixel image
  cv::Mat image2(cv::Size(320, 240), CV_8UC3);
  // NOTE: colors are specified as cv::Scalar(B, G, R) & NOT RGB
  image2 = cv::Scalar(0, 0, 255);
  cv::imshow("Image", image2);
  cv::waitKey(0);

  // read in the image
  cv::Mat image3 = cv::imread(image_path);
  // make copies
  cv::Mat image4(image3);
  image1 = image3;
  image3.copyTo(image2);
  cv::Mat image5 = image3.clone();

  // flip image3 on x-axis
  cv::flip(image3, image3, 0);

  // check which images have been affected by the processing
  cv::imshow("Image 3", image3);
  cv::imshow("Image 1", image1);
  cv::imshow("Image 2", image2);
  cv::imshow("Image 4", image4);
  cv::imshow("Image 5", image5);
  cv::waitKey(0); // wait for a key pressed

  return 0;
  // return a.exec();
}
