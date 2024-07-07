// stlstreams.cc - STL streams
#include <iostream>
#include <sstream>
#include <fstream>

using namespace std;

int main(void) {
   ostringstream strbuf;

   int lucky{7};
   float pi{3.1415f};
   double e{2.71828};
   const auto SPACE{' '};

   // print to string stream & display contents
   cout << "An in-memory stream" << endl;
   strbuf << "luckynumber: " << lucky << endl
      << " pi: " << pi << endl
      << " e: " << e << endl;
   cout << strbuf.str();

   // write it out to a file stream
   cout << "Writing in-memory stream to file (mydata.dat)" << endl;
   ofstream ofs("mydata.dat");
   if (ofs) {
      ofs << strbuf.str();
      ofs.close();
   }
   // read data from stream
   cout << "Reading from file (mydata.dat)" << endl;
   ifstream ifs;
   string newstr;
   ifs.open("mydata.dat");
   if (ifs) {
      // read first line "luckynumber: 7"
      int lucky2;
      ifs >> newstr >> lucky2;
      if (lucky != lucky2)
         cerr << "ERROR reading file " << newstr << SPACE << lucky2 << endl;
      else 
         cout << "Read -> " << newstr << SPACE << lucky2 << endl;

      float pi2;
      ifs >> newstr >> pi2;
      if (pi != pi2)
         cerr << "ERROR reading file " << newstr << SPACE << pi2 << endl;
      else 
         cout << "Read -> " << newstr << SPACE << pi2 << endl;

      double e2;
      ifs >> newstr >> e2;
      if (e != e2)
         cerr << "ERROR reading file " << newstr << SPACE << e2 << endl;
      else 
         cout << "Read -> " << newstr << SPACE << e2 << endl;
   }

   return 0;
}

   
