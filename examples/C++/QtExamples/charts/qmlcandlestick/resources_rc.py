# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x08\x87\
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
arts 2.2\x0a\x0aChartV\
iew {\x0a    title:\
 \x22Candlestick se\
ries\x22\x0a    width:\
 800\x0a    height:\
 600\x0a    theme: \
ChartView.ChartT\
hemeLight\x0a    le\
gend.alignment: \
Qt.AlignBottom\x0a \
   antialiasing:\
 true\x0a\x0a    Candl\
estickSeries {\x0a \
       name: \x22Ac\
me Ltd.\x22\x0a       \
 increasingColor\
: \x22green\x22\x0a      \
  decreasingColo\
r: \x22red\x22\x0a\x0a      \
  CandlestickSet\
 { timestamp: 14\
35708800000; ope\
n: 6.90; high: 6\
.94; low: 5.99; \
close: 6.60 }\x0a  \
      Candlestic\
kSet { timestamp\
: 1435795200000;\
 open: 6.69; hig\
h: 6.69; low: 6.\
69; close: 6.69 \
}\x0a        Candle\
stickSet { times\
tamp: 1436140800\
000; open: 4.85;\
 high: 6.23; low\
: 4.85; close: 6\
.00 }\x0a        Ca\
ndlestickSet { t\
imestamp: 143622\
7200000; open: 5\
.89; high: 6.15;\
 low: 3.77; clos\
e: 5.69 }\x0a      \
  CandlestickSet\
 { timestamp: 14\
36313600000; ope\
n: 4.64; high: 4\
.64; low: 2.54; \
close: 2.54 }\x0a  \
  }\x0a}\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x0e\
\x0a\x99\xb8\xfb\
\x00q\
\x00m\x00l\x00c\x00a\x00n\x00d\x00l\x00e\x00s\x00t\x00i\x00c\x00k\
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
\x00\x00\x00.\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x87_\xcdZW\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
