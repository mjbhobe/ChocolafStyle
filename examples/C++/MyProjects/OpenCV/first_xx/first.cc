#include <QTextStream>
#include <cstdlib>
#include <filesystem>
#include <opencv2/opencv.hpp>

using namespace cv;
namespace fs = std::filesystem;

static QTextStream cout(stdout, QIODeviceBase::WriteOnly);
static QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
static QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int argc, char **argv)
{
   if (argc < 2) {
      QString progName = fs::path(argv[0]).filename().string().c_str();
      cout << "ERROR: Expecting path of image to view as argument" << Qt::endl;
      cout << "Usage: " << progName << " image_path_to_view" << Qt::endl;
      cout << "    where image_path_to_view is a valid full or relative path to image file" << Qt::endl;
      return -1;
   }

   // check if path exists
   fs::path p = argv[1];
   if (!fs::exists(p)) {
      cout << "FATAL: image " << argv[1] << " does not exist. Please check path" << Qt::endl;
      return -1;
   }

   Mat image;
   image = imread(argv[1]);

   if (!image.data) {
      cout << "Could not open image! Please check if " << argv[1] << " is a valid image file." << Qt::endl;
      return -1;
   }

   QString dispWin = QString("Display Image: %1").arg(argv[1]);

   namedWindow(dispWin.toStdString().c_str(), WINDOW_NORMAL); // WINDOW_AUTOSIZE
   imshow(dispWin.toStdString().c_str(), image);
   waitKey(0);
   destroyAllWindows();

   return EXIT_SUCCESS;
}
