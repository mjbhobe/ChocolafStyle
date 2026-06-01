#include <QObject>
#include <iostream>
#include <string>

class MyString {
  public:
    MyString(const std::string &str) : m_string(str) {}
    ~MyString() { std::cout << "MyString(" << m_string << ") destructor called!" << std::endl; }
    size_t length() const { return m_string.length(); }
    friend std::ostream &operator<<(std::ostream &ost, const MyString &str)
    {
      ost << str.m_string;
      return ost;
    }
  private:
    std::string m_string;
};

class MyOString : public QObject {
  public:
    MyOString(const std::string &str, QObject *parent = nullptr) : QObject(parent), m_string(str) {}
    ~MyOString() { std::cout << "MyOString(" << m_string << ") destructor called!" << std::endl; }
    size_t length() const { return m_string.length(); }
    friend std::ostream &operator<<(std::ostream &ost, const MyOString &str)
    {
      ost << str.m_string;
      return ost;
    }
  private:
    std::string m_string;
};

int main(void)
{
  QObject obj;
  // the pointer below is not auto-deleted (mem leak)
  MyString *a = new MyString("Hello World!");
  // the pointer below is auto-deleted (no mem leak!)
  MyOString *b = new MyOString("Hello World! I get auto-deleted", &obj);
  MyOString *c = new MyOString("Hello World! So do I", &obj);
  MyOString *d = new MyOString("Hello World! Me too!!", &obj);

  std::cout << "MyString -> [" << *a << "] of length " << a->length() << std::endl;
  std::cout << "MyOString -> [" << *b << "] of length " << b->length() << std::endl;
  std::cout << "MyOString -> [" << *c << "] of length " << c->length() << std::endl;
  std::cout << "MyOString -> [" << *d << "] of length " << d->length() << std::endl;

  return 0;
}
