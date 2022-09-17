#ifndef __MatOps_h__
#define __MatOps_h__

// --------------------------------------------------
// MatOps.h - cv::Mat image operations

#include <QPixmap>
#include <opencv2/opencv.hpp>

class MatOp : public QObject
{
public:
  MatOp(const QPixmap &pixMap, QObject *parent = nullptr);
  ~MatOp()
  {
  }

  // operations
  QPixmap blur(cv::Size ksize = cv::Size(8, 8), cv::Point anchor = cv::Point(-1, -1),
               int borderType = 4);
  QPixmap sharpen(int intensity = 2, cv::Size ksize = cv::Size(9, 9), double sigmaX = 0.0,
                  double sigmaY = 0.0, int borderType = 4);
  QPixmap erode(cv::Point anchor = cv::Point(-1, -1), int iterations = 1,
                int borderType = 0,
                const cv::Scalar &borderValue = cv::morphologyDefaultBorderValue());
  QPixmap cartoonify(int ds_factor = 4, bool sketch_mode = false);

private:
  QImage m_image;
  cv::Mat m_srcMat;
};

#endif // __MatOps_h__
