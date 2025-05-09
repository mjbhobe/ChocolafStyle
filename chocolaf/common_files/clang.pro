# use this as an include in your Qmake file
QMAKE_CXX=clang++
QMAKE_CXX_FLAGS += -std=c++23 -stdlib=libc++
QMAKE_CXX_FLAGS -= -fno-keep-inline-dllexport
QMAKE_LFLAGS += -stdlib=libc++
