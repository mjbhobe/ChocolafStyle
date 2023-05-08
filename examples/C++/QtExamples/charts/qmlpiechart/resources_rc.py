# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x07\x87\
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
\x0a\x0a//![1]\x0aimport \
QtQuick 2.0\x0aimpo\
rt QtCharts 2.0\x0a\
\x0aChartView {\x0a   \
 width: 400\x0a    \
height: 300\x0a    \
theme: ChartView\
.ChartThemeBrown\
Sand\x0a    antiali\
asing: true\x0a\x0a//!\
[1]\x0a//![2]\x0a    P\
ieSeries {\x0a     \
   id: pieSeries\
\x0a        PieSlic\
e { label: \x22eate\
n\x22; value: 94.9 \
}\x0a        PieSli\
ce { label: \x22not\
 yet eaten\x22; val\
ue: 5.1 }\x0a    }\x0a\
//![2]\x0a\x0a    Comp\
onent.onComplete\
d: {\x0a        if \
(false) {\x0a      \
      //![4]\x0a   \
         pieSeri\
es.append(\x22don't\
 care\x22, 1.1);\x0a  \
          //![4]\
\x0a\x0a            //\
![5]\x0a           \
 pieSeries.at(0)\
.exploded = true\
;\x0a            //\
![5]\x0a        }\x0a \
   }\x0a\x0a//![3]\x0a}\x0a/\
/![3]\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x0b\
\x0fInT\
\x00q\
\x00m\x00l\x00p\x00i\x00e\x00c\x00h\x00a\x00r\x00t\
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
\x00\x00\x00(\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x87\xf4\x8dL\x16\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
