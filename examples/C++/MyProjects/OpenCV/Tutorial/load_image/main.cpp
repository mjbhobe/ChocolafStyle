#include <QtCore>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;

/**
 * @brief getRandomImagePath
 *  gets a random image path from the standard pictures folder of the OS
 * @return a random image path from the standard pictures folder for OS
 */
QString getRandomImagePath()
{
   // look up the standard pictures folder & get a random image path
   QStringList imagePaths = QStandardPaths::standardLocations(
       QStandardPaths::PicturesLocation);
   // NOTE: on my OS all HD wallpaers are located in HD wallpapers sub-folder
   // Plase COMMENT FOLOWING LINE on your system
   auto picsFolderPath = imagePaths.first() + QDir::separator() + "HD Wallpapers";
   qDebug() << "Will look for images in " << picsFolderPath << " folder";

   if (picsFolderPath.isEmpty()) {
      qDebug() << "Unable to locate system pictures folder!!";
      return "";
   }

   QDir picsFolder = QDir(picsFolderPath);
   if (picsFolder.isEmpty()) {
      qDebug() << "Pictures folder does not exist!";
      return "";
   }

   // list all pictures in this folder
   QStringList imageFilters;
   imageFilters << "*.jpg" << "*.jpeg" << "*.png" << "*.bmp";
   QStringList imageFiles = picsFolder.entryList(imageFilters, QDir::Files);
   if (imageFiles.isEmpty()) {
      qDebug() << "No images found in " << picsFolderPath;
      return "";
   }

   int randomIndex = QRandomGenerator::global()->bounded(imageFiles.size());
   QString randomImagePath = picsFolder.absoluteFilePath(imageFiles[randomIndex]);
   qDebug() << "Selected image: " << randomImagePath;
   return randomImagePath;
}

int main()
{
   QString randomImagePath = getRandomImagePath();
   qDebug() << "Displaying " << randomImagePath;
   // OpenCV uses cv::String
   //cv::String image_path = cv::String(randomImagePath.toStdString().c_str());
   std::string image_path = randomImagePath.toStdString();
   cv::Mat image = cv::imread(image_path, cv::IMREAD_COLOR);
   if (image.empty()) {
      qDebug() << "FATAL: could not read image " << randomImagePath;
      return -1;
   }

   // create a display windows of size (1024, 768) to display image
   // image will be re-sized to this dimension, else for large images, window
   // could be larger than scree
   std::string win_title
       = QString("OpenCV Image Viewer: Displaying %1").arg(randomImagePath).toStdString();
   //cv::String windowName(win_title);
   cv::namedWindow(win_title, cv::WINDOW_NORMAL);
   //cv::resizeWindow(windowName, 1024, 768);
   cv::resizeWindow(win_title, 1024, 768);
   //cv::imshow(windowName, image);
   cv::imshow(win_title, image);
   cv::waitKey(0); // wait for user to press any key
   cv::destroyAllWindows();
   return 0;
}
