# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x0e\xec\
/\
****************\
****************\
****************\
****************\
************\x0d\x0a**\
\x0d\x0a** Copyright (\
C) 2016 The Qt C\
ompany Ltd.\x0d\x0a** \
Contact: https:/\
/www.qt.io/licen\
sing/\x0d\x0a**\x0d\x0a** Th\
is file is part \
of the Qt Charts\
 module of the Q\
t Toolkit.\x0d\x0a**\x0d\x0a\
** $QT_BEGIN_LIC\
ENSE:GPL$\x0d\x0a** Co\
mmercial License\
 Usage\x0d\x0a** Licen\
sees holding val\
id commercial Qt\
 licenses may us\
e this file in\x0d\x0a\
** accordance wi\
th the commercia\
l license agreem\
ent provided wit\
h the\x0d\x0a** Softwa\
re or, alternati\
vely, in accorda\
nce with the ter\
ms contained in\x0d\
\x0a** a written ag\
reement between \
you and The Qt C\
ompany. For lice\
nsing terms\x0d\x0a** \
and conditions s\
ee https://www.q\
t.io/terms-condi\
tions. For furth\
er\x0d\x0a** informati\
on use the conta\
ct form at https\
://www.qt.io/con\
tact-us.\x0d\x0a**\x0d\x0a**\
 GNU General Pub\
lic License Usag\
e\x0d\x0a** Alternativ\
ely, this file m\
ay be used under\
 the terms of th\
e GNU\x0d\x0a** Genera\
l Public License\
 version 3 or (a\
t your option) a\
ny later version\
\x0d\x0a** approved by\
 the KDE Free Qt\
 Foundation. The\
 licenses are as\
 published by\x0d\x0a*\
* the Free Softw\
are Foundation a\
nd appearing in \
the file LICENSE\
.GPL3\x0d\x0a** includ\
ed in the packag\
ing of this file\
. Please review \
the following\x0d\x0a*\
* information to\
 ensure the GNU \
General Public L\
icense requireme\
nts will\x0d\x0a** be \
met: https://www\
.gnu.org/license\
s/gpl-3.0.html.\x0d\
\x0a**\x0d\x0a** $QT_END_\
LICENSE$\x0d\x0a**\x0d\x0a**\
****************\
****************\
****************\
****************\
**********/\x0d\x0a\x0d\x0ai\
mport QtQuick 2.\
0\x0d\x0aimport QtChar\
ts 2.0\x0d\x0a\x0d\x0aItem {\
\x0d\x0a    width: 400\
\x0d\x0a    height: 30\
0\x0d\x0a    property \
int __activeInde\
x: 1\x0d\x0a    proper\
ty real __interv\
alCoefficient: 0\
\x0d\x0a\x0d\x0a    //![1]\x0d\x0a\
    ChartView {\x0d\
\x0a        id: cha\
rtView\x0d\x0a        \
anchors.fill: pa\
rent\x0d\x0a        ti\
tle: \x22Wheel of f\
ortune\x22\x0d\x0a       \
 legend.visible:\
 false\x0d\x0a        \
antialiasing: tr\
ue\x0d\x0a\x0d\x0a        Pi\
eSeries {\x0d\x0a     \
       id: wheel\
OfFortune\x0d\x0a     \
       horizonta\
lPosition: 0.3\x0d\x0a\
        }\x0d\x0a\x0d\x0a   \
     SplineSerie\
s {\x0d\x0a           \
 id: splineSerie\
s\x0d\x0a        }\x0d\x0a\x0d\x0a\
        ScatterS\
eries {\x0d\x0a       \
     id: scatter\
Series\x0d\x0a        \
}\x0d\x0a    }\x0d\x0a    //\
![1]\x0d\x0a\x0d\x0a    //![\
2]\x0d\x0a    Componen\
t.onCompleted: {\
\x0d\x0a        __inte\
rvalCoefficient \
= Math.random() \
+ 0.25;\x0d\x0a\x0d\x0a     \
   for (var i = \
0; i < 20; i++)\x0d\
\x0a            whe\
elOfFortune.appe\
nd(\x22\x22, 1);\x0d\x0a\x0d\x0a  \
      var interv\
al = 1;\x0d\x0a       \
 for (var j = 0;\
 interval < 800;\
 j++) {\x0d\x0a       \
     interval = \
__intervalCoeffi\
cient * j * j;\x0d\x0a\
            spli\
neSeries.append(\
j, interval);\x0d\x0a \
       }\x0d\x0a      \
  chartView.axis\
X(scatterSeries)\
.max = j;\x0d\x0a     \
   chartView.axi\
sY(scatterSeries\
).max = 1000;\x0d\x0a \
   }\x0d\x0a    //![2]\
\x0d\x0a\x0d\x0a    Timer {\x0d\
\x0a        id: tim\
er\x0d\x0a        prop\
erty color switc\
hColor\x0d\x0a        \
triggeredOnStart\
: true\x0d\x0a        \
running: true\x0d\x0a \
       repeat: t\
rue\x0d\x0a        int\
erval: 100\x0d\x0a    \
    onTriggered:\
 {\x0d\x0a            \
var index = __ac\
tiveIndex % whee\
lOfFortune.count\
;\x0d\x0a            i\
f (interval < 70\
0) {\x0d\x0a          \
      //![3]\x0d\x0a  \
              wh\
eelOfFortune.at(\
index).exploded \
= false;\x0d\x0a      \
          __acti\
veIndex++;\x0d\x0a    \
            inde\
x = __activeInde\
x % wheelOfFortu\
ne.count;\x0d\x0a     \
           wheel\
OfFortune.at(ind\
ex).exploded = t\
rue;\x0d\x0a          \
      //![3]\x0d\x0a  \
              in\
terval = splineS\
eries.at(__activ\
eIndex).y;\x0d\x0a    \
            //![\
4]\x0d\x0a            \
    scatterSerie\
s.clear();\x0d\x0a    \
            scat\
terSeries.append\
(__activeIndex, \
interval);\x0d\x0a    \
            scat\
terSeries.color \
= Qt.tint(scatte\
rSeries.color, \x22\
#05FF0000\x22);\x0d\x0a  \
              sc\
atterSeries.mark\
erSize += 0.5;\x0d\x0a\
                \
//![4]\x0d\x0a        \
    } else {\x0d\x0a  \
              //\
![5]\x0d\x0a          \
      // Switch \
the colors of th\
e slice and the \
border\x0d\x0a        \
        wheelOfF\
ortune.at(index)\
.borderWidth = 2\
;\x0d\x0a             \
   switchColor =\
 wheelOfFortune.\
at(index).border\
Color;\x0d\x0a        \
        wheelOfF\
ortune.at(index)\
.borderColor = w\
heelOfFortune.at\
(index).color;\x0d\x0a\
                \
wheelOfFortune.a\
t(index).color =\
 switchColor;\x0d\x0a \
               /\
/![5]\x0d\x0a         \
   }\x0d\x0a        }\x0d\
\x0a    }\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x11\
\x08=X\xd3\
\x00q\
\x00m\x00l\x00c\x00u\x00s\x00t\x00o\x00m\x00i\x00z\x00a\x00t\x00i\x00o\x00n\x00s\
\
\x00\x08\
\x08\x01Z\x5c\
\x00m\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x004\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x83\x97f\x8e\x01\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
