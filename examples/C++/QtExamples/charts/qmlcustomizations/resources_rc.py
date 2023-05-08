# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x0e{\
/\
****************\
****************\
****************\
****************\
************\x0a**\x0a\
** Copyright (C)\
 2016 The Qt Com\
pany Ltd.\x0a** Con\
tact: https://ww\
w.qt.io/licensin\
g/\x0a**\x0a** This fi\
le is part of th\
e Qt Charts modu\
le of the Qt Too\
lkit.\x0a**\x0a** $QT_\
BEGIN_LICENSE:GP\
L$\x0a** Commercial\
 License Usage\x0a*\
* Licensees hold\
ing valid commer\
cial Qt licenses\
 may use this fi\
le in\x0a** accorda\
nce with the com\
mercial license \
agreement provid\
ed with the\x0a** S\
oftware or, alte\
rnatively, in ac\
cordance with th\
e terms containe\
d in\x0a** a writte\
n agreement betw\
een you and The \
Qt Company. For \
licensing terms\x0a\
** and condition\
s see https://ww\
w.qt.io/terms-co\
nditions. For fu\
rther\x0a** informa\
tion use the con\
tact form at htt\
ps://www.qt.io/c\
ontact-us.\x0a**\x0a**\
 GNU General Pub\
lic License Usag\
e\x0a** Alternative\
ly, this file ma\
y be used under \
the terms of the\
 GNU\x0a** General \
Public License v\
ersion 3 or (at \
your option) any\
 later version\x0a*\
* approved by th\
e KDE Free Qt Fo\
undation. The li\
censes are as pu\
blished by\x0a** th\
e Free Software \
Foundation and a\
ppearing in the \
file LICENSE.GPL\
3\x0a** included in\
 the packaging o\
f this file. Ple\
ase review the f\
ollowing\x0a** info\
rmation to ensur\
e the GNU Genera\
l Public License\
 requirements wi\
ll\x0a** be met: ht\
tps://www.gnu.or\
g/licenses/gpl-3\
.0.html.\x0a**\x0a** $\
QT_END_LICENSE$\x0a\
**\x0a*************\
****************\
****************\
****************\
***************/\
\x0a\x0aimport QtQuick\
 2.0\x0aimport QtCh\
arts 2.0\x0a\x0aItem {\
\x0a    width: 400\x0a\
    height: 300\x0a\
    property int\
 __activeIndex: \
1\x0a    property r\
eal __intervalCo\
efficient: 0\x0a\x0a  \
  //![1]\x0a    Cha\
rtView {\x0a       \
 id: chartView\x0a \
       anchors.f\
ill: parent\x0a    \
    title: \x22Whee\
l of fortune\x22\x0a  \
      legend.vis\
ible: false\x0a    \
    antialiasing\
: true\x0a\x0a        \
PieSeries {\x0a    \
        id: whee\
lOfFortune\x0a     \
       horizonta\
lPosition: 0.3\x0a \
       }\x0a\x0a      \
  SplineSeries {\
\x0a            id:\
 splineSeries\x0a  \
      }\x0a\x0a       \
 ScatterSeries {\
\x0a            id:\
 scatterSeries\x0a \
       }\x0a    }\x0a \
   //![1]\x0a\x0a    /\
/![2]\x0a    Compon\
ent.onCompleted:\
 {\x0a        __int\
ervalCoefficient\
 = Math.random()\
 + 0.25;\x0a\x0a      \
  for (var i = 0\
; i < 20; i++)\x0a \
           wheel\
OfFortune.append\
(\x22\x22, 1);\x0a\x0a      \
  var interval =\
 1;\x0a        for \
(var j = 0; inte\
rval < 800; j++)\
 {\x0a            i\
nterval = __inte\
rvalCoefficient \
* j * j;\x0a       \
     splineSerie\
s.append(j, inte\
rval);\x0a        }\
\x0a        chartVi\
ew.axisX(scatter\
Series).max = j;\
\x0a        chartVi\
ew.axisY(scatter\
Series).max = 10\
00;\x0a    }\x0a    //\
![2]\x0a\x0a    Timer \
{\x0a        id: ti\
mer\x0a        prop\
erty color switc\
hColor\x0a        t\
riggeredOnStart:\
 true\x0a        ru\
nning: true\x0a    \
    repeat: true\
\x0a        interva\
l: 100\x0a        o\
nTriggered: {\x0a  \
          var in\
dex = __activeIn\
dex % wheelOfFor\
tune.count;\x0a    \
        if (inte\
rval < 700) {\x0a  \
              //\
![3]\x0a           \
     wheelOfFort\
une.at(index).ex\
ploded = false;\x0a\
                \
__activeIndex++;\
\x0a               \
 index = __activ\
eIndex % wheelOf\
Fortune.count;\x0a \
               w\
heelOfFortune.at\
(index).exploded\
 = true;\x0a       \
         //![3]\x0a\
                \
interval = splin\
eSeries.at(__act\
iveIndex).y;\x0a   \
             //!\
[4]\x0a            \
    scatterSerie\
s.clear();\x0a     \
           scatt\
erSeries.append(\
__activeIndex, i\
nterval);\x0a      \
          scatte\
rSeries.color = \
Qt.tint(scatterS\
eries.color, \x22#0\
5FF0000\x22);\x0a     \
           scatt\
erSeries.markerS\
ize += 0.5;\x0a    \
            //![\
4]\x0a            }\
 else {\x0a        \
        //![5]\x0a \
               /\
/ Switch the col\
ors of the slice\
 and the border\x0a\
                \
wheelOfFortune.a\
t(index).borderW\
idth = 2;\x0a      \
          switch\
Color = wheelOfF\
ortune.at(index)\
.borderColor;\x0a  \
              wh\
eelOfFortune.at(\
index).borderCol\
or = wheelOfFort\
une.at(index).co\
lor;\x0a           \
     wheelOfFort\
une.at(index).co\
lor = switchColo\
r;\x0a             \
   //![5]\x0a      \
      }\x0a        \
}\x0a    }\x0a}\x0a\
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
\x00\x00\x01\x87\xf4\x8dL\x13\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
