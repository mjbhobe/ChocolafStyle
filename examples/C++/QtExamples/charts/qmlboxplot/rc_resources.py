# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x07\xcb\
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
ts 2.0\x0d\x0a\x0d\x0aChartV\
iew {\x0d\x0a    title\
: \x22Box Plot seri\
es\x22\x0d\x0a    width: \
400\x0d\x0a    height:\
 300\x0d\x0a    theme:\
 ChartView.Chart\
ThemeBrownSand\x0d\x0a\
    legend.align\
ment: Qt.AlignBo\
ttom\x0d\x0a    antial\
iasing: true\x0d\x0a\x0d\x0a\
    BoxPlotSerie\
s {\x0d\x0a        id:\
 plotSeries\x0d\x0a   \
     name: \x22Inco\
me\x22\x0d\x0a        Box\
Set { label: \x22Ja\
n\x22; values: [3, \
4, 5.1, 6.2, 8.5\
] }\x0d\x0a        Box\
Set { label: \x22Fe\
b\x22; values: [5, \
6, 7.5, 8.6, 11.\
8] }\x0d\x0a        Bo\
xSet { label: \x22M\
ar\x22; values: [3.\
2, 5, 5.7, 8, 9.\
2] }\x0d\x0a        Bo\
xSet { label: \x22A\
pr\x22; values: [3.\
8, 5, 6.4, 7, 8]\
 }\x0d\x0a        BoxS\
et { label: \x22May\
\x22; values: [4, 5\
, 5.2, 6, 7] }\x0d\x0a\
    }\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x0a\
\x09`{$\
\x00q\
\x00m\x00l\x00b\x00o\x00x\x00p\x00l\x00o\x00t\
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
\x00\x00\x00&\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x83\x97f\x8d\xf1\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
