#include <cstdlib>
#include <QCoreApplication>
#include <QStringList>
#include <QTextStream>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);

   QString winter = "December, January, February";
   QString spring = "March, April, May";
   QString summer = "June, July, August";
   QString fall = "September, October, November";

   // build a string list
   QStringList list;
   // add at end using << operator
   list << winter;
   list << spring;
   // add at end using append()
   list.append(summer);
   // add at beginning using prepend()
   list.prepend(fall);

   // you can access each item of a string list using index
   cout << "The string list has " << list.length() << " items" << Qt::endl;
   cout << "  Here is the first: " << list[0] << Qt::endl;
   cout << "  and this is the last: " << list[list.length() - 1] << Qt::endl;

   // get all items of the list as a single string
   auto all_items = list.join(", ");
   cout << "Here are all the items: " << all_items << Qt::endl;

   // and split them into individual elements
   QStringList list2 = all_items.split(", ");
   cout << "list2 has " << list2.length() << " items shown below:" << Qt::endl;
   foreach (const QString &str, list2)
      cout << str << ", ";
   cout << Qt::endl;

   // here is another iterator (C++ style)
   cout << "Iterating over the list using STL like iterator..." << Qt::endl;
   QStringList::iterator it = list2.begin();
   for (; it != list2.end() - 1; ++it)
      cout << *it << ", ";
   cout << *(list2.end() - 1) << Qt::endl;

   // Java-style iteration
   cout << "Using Java-style iteration..." << Qt::endl;
   QListIterator<QString> iter2(list2);
   while (iter2.hasNext())
      cout << iter2.next() << ", ";
   cout << Qt::endl;

   return EXIT_SUCCESS;
}
