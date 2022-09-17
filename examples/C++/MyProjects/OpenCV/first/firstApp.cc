// ==================================================================================
// firstApp.cc - first OpenCV C++ application with Qt 5.X
// @author Manish Bhobe
// ==================================================================================
#include "argparse/argparse.hpp"
#include <QTextStream>
#include <cstdlib>
#include <filesystem>
#include <opencv2/opencv.hpp>

using namespace cv;
namespace fs = std::filesystem;

static QTextStream cout(stdout, QIODevice::WriteOnly);
static QTextStream cerr(stderr, QIODevice::WriteOnly);
static QTextStream cin(stdin, QIODevice::ReadOnly);

// define command line arguments
// @see: https://github.com/morrisfranken/argparse
struct MyArgs : public argparse::Args {
  // -i | --image <image path>
  std::string &image_path = kwarg("i,image", "Full path to the image file to display.");
};

int main(int argc, char **argv)
{
  // parse the command line arguments
  MyArgs args = argparse::parse<MyArgs>(argc, argv);

  /*
  if (argc < 2) {
     QString progName = fs::path(argv[0]).filename().string().c_str();
     cout << "ERROR: Expecting path of image to view as argument" << Qt::endl;
     cout << "Usage: " << progName << " image_path_to_view" << Qt::endl;
     cout << "  where image_path_to_view is a valid full or relative path to image file"
          << Qt::endl;
     return -1;
 } */

  // check if path exists
  // fs::path p = argv[1];
  fs::path p = args.image_path;
  if (!fs::exists(p)) {
    cout << "FATAL: image " << args.image_path.c_str() /* argv[1] */
         << " does not exist. Please check path" << Qt::endl;
    return -1;
  }

  Mat image;
  // image = imread(argv[1]);
  image = imread(args.image_path.c_str());

  if (!image.data) {
    cout << "Could not open image! Please check if "
         << args.image_path.c_str() /* argv[1] */
         << " is a valid image file." << Qt::endl;
    return -1;
  }

  QString dispWin =
      QString("Display Image: %1").arg(args.image_path.c_str() /* argv[1] */);

  namedWindow(dispWin.toStdString().c_str(), WINDOW_NORMAL); // WINDOW_AUTOSIZE
  imshow(dispWin.toStdString().c_str(), image);
  waitKey(0);
  destroyAllWindows();

  return EXIT_SUCCESS;
}
