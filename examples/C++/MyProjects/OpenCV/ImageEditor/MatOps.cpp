// MatOps.cpp - MatOps class implementation
#include "MatOps.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <opencv2/opencv.hpp>

MatOp::MatOp(const QPixmap &pixmap, QObject *parent /*= nullptr*/) : QObject(parent)
{
  m_image = pixmap.toImage();
  m_image = m_image.convertToFormat(QImage::Format_RGB888);
  m_srcMat = cv::Mat(m_image.height(), m_image.width(), CV_8UC3, m_image.bits(),
                     m_image.bytesPerLine());
}

QPixmap MatOp::blur(cv::Size ksize /*= cv::Size(8,8)*/,
                    cv::Point anchor /*=cv::Point(-1,-1)*/, int borderType /*=4*/)
{
  cv::Mat conv;
  cv::blur(m_srcMat, conv, ksize, anchor, borderType);
  QImage blurredImage(conv.data, conv.cols, conv.rows, conv.step, QImage::Format_RGB888);
  return QPixmap::fromImage(blurredImage);
}

QPixmap MatOp::sharpen(int intensity /*= 2*/, cv::Size ksize /*= cv::Size(9, 9)*/,
                       double sigmaX /*= 0.0*/, double sigmaY /*= 0.0*/,
                       int borderType /*= 4*/)
{
  cv::Mat conv;
  cv::GaussianBlur(m_srcMat, conv, ksize, sigmaX, sigmaY, borderType);
  QImage sharpImage(conv.data, conv.cols, conv.rows, conv.step, QImage::Format_RGB888);
  return QPixmap::fromImage(sharpImage);
}

QPixmap
MatOp::erode(cv::Point anchor /*= cv::Point(-1, -1)*/, int iterations /*= 1*/,
             int borderType /*= 0*/,
             const cv::Scalar &borderValue /*= cv::morphologyDefaultBorderValue()*/)
{
  cv::erode(m_srcMat, m_srcMat, cv::Mat(), anchor, iterations, borderType, borderValue);
  QImage erodeImage(m_srcMat.data, m_srcMat.cols, m_srcMat.rows, m_srcMat.step,
                    QImage::Format_RGB888);
  return QPixmap::fromImage(erodeImage);
}

QPixmap MatOp::cartoonify(int ds_factor /*= 4*/, bool sketch_mode /*=false*/)
{
  // following code is taken from OpenCV with Python by Example by Prateek Joshi

  // convert source image to grayscale
  cv::Mat gray_image;
  cv::cvtColor(m_srcMat, gray_image, cv::COLOR_BGR2GRAY);
  // apply median filter to it
  cv::medianBlur(gray_image, gray_image, 7);
  // detect edges in image & threshold it
  cv::Mat edges, mask;
  cv::Laplacian(gray_image, edges, CV_8U, 5);
  auto ret = cv::threshold(edges, mask, 100, 255, cv::THRESH_BINARY_INV);
  if (sketch_mode) {
    cv::Mat color_image;
    cv::cvtColor(mask, color_image, cv::COLOR_GRAY2BGR);
    QImage cartoonImage(color_image.data, color_image.cols, color_image.rows,
                        color_image.step, QImage::Format_RGB888);
    return QPixmap::fromImage(cartoonImage);
  }

  // resize image to smaller size for faster computation
  cv::Mat small_image;
  cv::resize(m_srcMat, small_image, small_image.size(), 1.0 / ds_factor, 1.0 / ds_factor,
             cv::INTER_AREA);
  auto num_repetitions = 10;
  auto sigma_color = 5;
  auto sigma_space = 7;
  auto size = 5;

  for (auto i = 0; i < num_repetitions; ++i)
    cv::bilateralFilter(small_image, small_image, 5, sigma_color, sigma_space);
  cv::Mat out_image;
  cv::resize(small_image, out_image, out_image.size(), ds_factor, ds_factor,
             cv::INTER_AREA);
  cv::bitwise_and(out_image, out_image, mask);
  QImage cartoonImage(out_image.data, out_image.cols, out_image.rows, out_image.step,
                      QImage::Format_RGB888);
  return QPixmap::fromImage(cartoonImage);

  /*
    int num_down = 2;
    int num_bilateral = 7;

    cv::Mat copy1, copy2;

    copy1 = m_srcMat.clone();
    for (int i = 0; i < num_down; ++i) {
      cv::pyrDown(copy1, copy2);
      copy1 = copy2.clone();
    }

    for (int i = 0; i < num_bilateral; ++i) {
      cv::bilateralFilter(copy1, copy2, 9, 9, 7);
      copy1 = copy2.clone();
    }

    for (int i = 0; i < num_down; ++i) {
      cv::pyrUp(copy1, copy2);
      copy1 = copy2.clone();
    }

    QImage cartoonImage(copy1.data, copy1.cols, copy1.rows, copy1.step,
                        QImage::Format_RGB888);
    return QPixmap::fromImage(cartoonImage);
    */
}
