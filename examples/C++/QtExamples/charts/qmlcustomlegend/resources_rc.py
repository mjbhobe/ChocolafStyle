# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x0ah\
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
arts 2.0\x0a\x0a//![1]\
\x0aChartView {\x0a   \
 id: chartViewHi\
ghlighted\x0a    ti\
tle: \x22\x22\x0a    prop\
erty variant sel\
ectedSeries\x0a    \
signal clicked\x0a \
   legend.visibl\
e: false\x0a    mar\
gins.top: 10\x0a   \
 margins.bottom:\
 0\x0a    antialias\
ing: true\x0a\x0a    L\
ineSeries {\x0a    \
    id: lineSeri\
es\x0a\x0a        axis\
X: ValueAxis {\x0a \
           min: \
2006\x0a           \
 max: 2012\x0a     \
       labelForm\
at: \x22%.0f\x22\x0a     \
       tickCount\
: 7\x0a        }\x0a  \
      axisY: Val\
ueAxis {\x0a       \
     id: axisY\x0a \
           title\
Text: \x22EUR\x22\x0a    \
        min: 0\x0a \
           max: \
40000\x0a          \
  labelFormat: \x22\
%.0f\x22\x0a          \
  tickCount: 5\x0a \
       }\x0a    }\x0a/\
/![1]\x0a\x0a    Mouse\
Area {\x0a        a\
nchors.fill: par\
ent\x0a        onCl\
icked: {\x0a       \
     chartViewHi\
ghlighted.clicke\
d();\x0a        }\x0a \
   }\x0a\x0a    onSele\
ctedSeriesChange\
d: {\x0a        lin\
eSeries.clear();\
\x0a        lineSer\
ies.color = sele\
ctedSeries.color\
;\x0a        var ma\
xVal = 0.0;\x0a    \
    for (var i =\
 0; i < selected\
Series.upperSeri\
es.count; i++ ) \
{\x0a            va\
r y = selectedSe\
ries.upperSeries\
.at(i).y - selec\
tedSeries.lowerS\
eries.at(i).y;\x0a \
           lineS\
eries.append(sel\
ectedSeries.uppe\
rSeries.at(i).x,\
 y);\x0a           \
 if (maxVal < y)\
\x0a               \
 maxVal = y;\x0a   \
     }\x0a        c\
hartViewHighligh\
ted.title = sele\
ctedSeries.name;\
\x0a        axisY.m\
ax = maxVal;\x0a   \
     axisY.apply\
NiceNumbers()\x0a  \
  }\x0a}\x0a\x0a\
\x00\x00\x04\x85\
\x00\
\x00\x0f\xa3x\xda\xc5VYo\xdbF\x10~\xd7\xaf\x98\
\x1a.`71E\xea\x96\xfa\xe4:\xb2\x10\xd40\xec\
ZN\x13\x14E\xb0\x22G\xd2\xc2\xcb]f\xb9\xd4\x81\
\xc0\xff\xbd\xb3K\xea\xb4\x5cIF\x80\x10\x06$\xcf|\
s}sP\xe5\xdf~\xe0Sr\x7fp\xa5\x92\xb9\xe6\
\xa3\xb1\x81\xb3\xabs\xa8\xf8A\x03\xfac\x84{C\x9a\
8ar\x0e7&\xf2r\xa44,4\x1d\x18\x1b\x93\
\xa4\x9dry:\x9dz\xdf\x8c\xc7UY\xf0\x10e\xca\
\xe5\xa8\x5cx\xed\x8fy\x0aC.\x10\xe83a\xda\x80\
\x1a\x82)\xfc\x8e\xe9\xff\x14b\x15e\xa4_\xc9\xfbJ\
\x89'n\xbc\xc2\xc5\xe9}\xff\xeb\x1f\xdd\xde\xc7\xdb\xaf\
7\x1f\xaf\xba\xb7\x0f\xddN\xef\xee\xe64O$\x8eQ\
\x87\x9c\x09\xb8q\x81\x11\x1eS6B\xab+\x04\x98\xc2\
X\x89\x882\x82\x09\x13<\x82peC\xa1\xf2|\x09\
\x14\xb39ddoV\xf9J\xeb\x86\x85\xa1\xd2\x11\x93\
!\xc2\x94\x9b\xb1Kq\xcdEa\x0fl\xa4\x11c\x94\
\x06\x12\xad&<\xc2h\x09\xb7^\x1e\xd4\xd0L\x99\xa6\
\x22\xf5{`\xc2\xa0\x96\xcc\xf0\x09\x8a\xf9{\x8a\xb33\
\x08a\xe2\x94B\x11\xd5\x5c\x92\xbb\x22\x1d\x98jn\x0c\
\xca\xb5\x88\x034S$\xc9\x5ce\xc0d\xb4\xd55\x0f\
\xae\x95\x86e_r\xbf\xce\x95\xb4d\xc8\x88\x1b\xaed\
\x0aD\xd5\x8e~:\xf4\xc5\x0a\x96{\x1bf\x9aR\xd4\
\xd6\x0b\x97C\xa5cf\x95\x05\x7f\x98'\x1d\x1a\xb0\x1a\
`f\x87\xdb\x02q\x91\xa5\x8b&\xf7n\x1f\xa1\x87\x12\
5\x91z\x97\x0d(\xdf\x97-\xbd\xdc$n\xd5*\xdb\
\xbc\x01\xda\xf8\x11d2B\xbd\xc6`1V\xe4\xdf\x85\
\xd9\x1db\x82:\xb5\x15T\xa9ApF)\x13\x97\x1a\
Tb\xcb:\x07;\xfb\x82\x91\xbb\x05\xce\xd1\x97\xd8N\
S\xc0\xc1\xdc\x05\xf8\xf3C\x17\xae\xa9%\x96\xfakE\
Y8N<\xd7\x8d\xe5\x94\xd9\x11`\xb4\x076z:\
v\xc6\xd6\x97\xb5w\xb6\xcb9Yyp}\xa2`\xc8\
\xb4m\x1fM\x8bE\xbb\xb2\x8bu\xf0h\x1d\xaay/\
B\x91EnV\x1c(a\xe1\x13\x1bY+GB\xc1\
\x96\x07w\x02\x19\x15\xadq\xc2q\x9a\xbbSB\xa8)\
!\xb7[j\x14P\xe6\x99\xc6\x05\x89\xaf1\xa8\xf1[\
\xc6\xb5\x1b\xc8\x94\x86X\x08\xeb\x89z\x12\xe3\xd6\x9d\x18\
\xc9\xccSzT^pR\x1e%\xe2\xa2\xea\xf9\xde\xd8\
\xc4b}\xe5\xbb\xb7\x1f\x16\x0b\x7f\x9a\x8b\x7f\xdcS.\
\x95x\x9c(\xbaF\xf7\xe6>\xe3\xe1\x13T<\x7f%\
*\x0e\x93\x95\x95\xdc\xf7O\x96\xa8\xef%\xa0\x87G\x1d\
\x08\x172'1\xdc\x08\xec\xc0I\x8f\xc6AK\xb7\x92\
}6\xc3\xf4\xc4i\x05\x8ePF\xde\x84\xa7|`a\
C&Rt\x9a\x94\x8f$\x11Ix\xd4\x18\x9d\xa5\xc6\
58E\xcd1\xbde1\x9eo\xa0f\xdc\xbc\x0e\x8a\
\x99\xa6>\xa7\x9eQI\x07\x02\x7fC6P\xc6\xa8\xb8\
\x03\xb9\x94ICw\x8b3{\x0b:`t\x86%'\
\xff\xc4D\x86\x973\x9a\x91\xbc\xccE\xa9\x8cD\x9f\x97\
\x92\x98\xcb\x0e\xbd\x1a\xfc\xc6J\xc2fV\x12T\x96\x12\
Ct^\xd1\xf8R\xdf\x9bK\xa1`\x03\x14\xd7n\xac\
\x88\xa9_=\x7f\x98\xb3\xf3\xbc?\xfa\x975\xcfDt\
\x1fg\xd6E\xf7\xf1\xaf\x93\xcd\xb4\xfc\xcd\x9c\xda>=\
\xbb\x92\x0a\xfcC\xb3\xba\x94\x9c4\x18]jd\x0f\x8e\
\xf1\xad\xf4RC\xea\x5c\xb3\x94Kj\x0a9s\xaaU\
\x86\x8e\xc6m6]u\xdbE\x0e\xe8M\x80\xfao\x1e\
\x99\xf1zM\x19]\x00\x9d\x87\xea\xd0\xd2I|\x91\xd0\
FR\x8f\x16\xbe\xa1\xfa\xfc\xe5Nq\x1a\xcd\xef0\xcb\
[\xf8;\xcc;P\xad\x06A\x9b\xea\xfd?d3G\
6\xdb\xb5`\x0f\xb2\xe5\x905\x9a\x86\xca\x1ed;\xf7\
\xd9j\xb7\xf7\xf8\x0c\xfc\x1cY\xf3\xeb\xf5=\xc8\xa0@\
\xd6\xf7\x22+;\xa3\xaf\xbe\xd1-<\x80\xec\xdd\x8c\xfa\
\x07\xb1\xe9\x1f\xc4\xa4\x7f\x10\x8b\xfeA\x0c\xfa\x07\xb1\xe7\
\x1f\xc4\x9c\xff\x82\xb5bc\xca\xe5_\xfe\x09\xfe=l\
y\xe2L\xf2\x90'L\xec^\xa0\xa5\xfa\xa7,\xd12\
\xfaq\x8b\xf4\x0e\x82j\xadV=b\xa1\xc8\xa2N\xa6\
G,\x16Y4\xea\xf5c\x16\x8c,\x9am\xbfv\xc4\
\xa2Y\x8bz\xbb}\xc4\xc2\x91\x05]\xdc\xca\x11\x8bg\
-\x82fs\xff\x02n\x1d\xb4\xe7\xf5I;\xf0N+\
\xfbc\xfd\x95C\xedt\xf4F\x0d\xbd\x9fs\xae]\xfc\
\xb7\x8d\x19}\xb6Z\xfb\xae\xdd\xceq{G\x8aJ\xb5\
\xf5\x86\xb1#K\x0a\xde|\xc3\xf8\x91e\xa5\xdal\xbc\
a\x0c\xad\xa5\xbf\xd7r\xd78Z\xcbF5x\xc3X\
\x92e\xb5\xd1j\xec\x1f\xcf\x1d\xa7\xe2\xb9\xf4\x5c\xfa\x0f\
\xfc\xbc>\xb6\
\x00\x00\x05\xd4\
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
arts 2.0\x0a\x0aAreaSe\
ries {\x0a    id: s\
eries\x0a\x0a    Behav\
ior on opacity {\
\x0a        NumberA\
nimation { durat\
ion: 250 }\x0a    }\
\x0a}\x0a\
\x00\x00\x11\x9b\
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
arts 2.0\x0a\x0aRectan\
gle {\x0a    id: le\
gend\x0a    color: \
\x22lightgray\x22\x0a\x0a   \
 property int se\
riesCount: 0\x0a   \
 property varian\
t seriesNames: [\
]\x0a    property v\
ariant seriesCol\
ors: []\x0a    sign\
al entered(strin\
g seriesName)\x0a  \
  signal exited(\
string seriesNam\
e)\x0a    signal se\
lected(string se\
riesName)\x0a\x0a    f\
unction addSerie\
s(seriesName, co\
lor) {\x0a        v\
ar names = serie\
sNames;\x0a        \
names[seriesCoun\
t] = seriesName;\
\x0a        seriesN\
ames = names;\x0a\x0a \
       var color\
s = seriesColors\
;\x0a        colors\
[seriesCount] = \
color;\x0a        s\
eriesColors = co\
lors;\x0a\x0a        s\
eriesCount++;\x0a  \
  }\x0a\x0a    Gradien\
t {\x0a        id: \
buttonGradient\x0a \
       GradientS\
top { position: \
0.0; color: \x22#F0\
F0F0\x22 }\x0a        \
GradientStop { p\
osition: 1.0; co\
lor: \x22#A0A0A0\x22 }\
\x0a    }\x0a\x0a    Grad\
ient {\x0a        i\
d: buttonGradien\
tHovered\x0a       \
 GradientStop { \
position: 0.0; c\
olor: \x22#FFFFFF\x22 \
}\x0a        Gradie\
ntStop { positio\
n: 1.0; color: \x22\
#B0B0B0\x22 }\x0a    }\
\x0a\x0a    //![2]\x0a   \
 Component {\x0a   \
     id: legendD\
elegate\x0a        \
Rectangle {\x0a    \
        id: rect\
\x0a    //![2]\x0a    \
        property\
 string name: se\
riesNames[index]\
\x0a            pro\
perty color mark\
erColor: seriesC\
olors[index]\x0a   \
         gradien\
t: buttonGradien\
t\x0a            bo\
rder.color: \x22#A0\
A0A0\x22\x0a          \
  border.width: \
1\x0a            ra\
dius: 4\x0a\x0a       \
     implicitWid\
th: label.implic\
itWidth + marker\
.implicitWidth +\
 30\x0a            \
implicitHeight: \
label.implicitHe\
ight + marker.im\
plicitHeight + 1\
0\x0a\x0a            R\
ow {\x0a           \
     id: row\x0a   \
             spa\
cing: 5\x0a        \
        anchors.\
verticalCenter: \
parent.verticalC\
enter\x0a          \
      anchors.le\
ft: parent.left\x0a\
                \
anchors.leftMarg\
in: 5\x0a          \
      Rectangle \
{\x0a              \
      id: marker\
\x0a               \
     anchors.ver\
ticalCenter: par\
ent.verticalCent\
er\x0a             \
       color: ma\
rkerColor\x0a      \
              op\
acity: 0.3\x0a     \
               r\
adius: 4\x0a       \
             wid\
th: 12\x0a         \
           heigh\
t: 10\x0a          \
      }\x0a        \
        Text {\x0a \
                \
   id: label\x0a   \
                \
 anchors.vertica\
lCenter: parent.\
verticalCenter\x0a \
                \
   anchors.verti\
calCenterOffset:\
 -1\x0a            \
        text: na\
me\x0a             \
   }\x0a           \
 }\x0a\x0a    //![3]\x0a \
           Mouse\
Area {\x0a         \
       id: mouse\
Area\x0a           \
     anchors.fil\
l: parent\x0a      \
          hoverE\
nabled: true\x0a   \
             onE\
ntered: {\x0a      \
              re\
ct.gradient = bu\
ttonGradientHove\
red;\x0a           \
         legend.\
entered(label.te\
xt);\x0a           \
     }\x0a         \
       onExited:\
 {\x0a             \
       rect.grad\
ient = buttonGra\
dient;\x0a         \
           legen\
d.exited(label.t\
ext);\x0a          \
          marker\
.opacity = 0.3;\x0a\
                \
    marker.heigh\
t = 10;\x0a        \
        }\x0a      \
          onClic\
ked: {\x0a         \
           legen\
d.selected(label\
.text);\x0a        \
            mark\
er.opacity = 1.0\
;\x0a              \
      marker.hei\
ght = 12;\x0a      \
          }\x0a    \
        }\x0a    //\
![3]\x0a        }\x0a \
   }\x0a\x0a    //![1]\
\x0a    Row {\x0a     \
   id: legendRow\
\x0a        anchors\
.centerIn: paren\
t\x0a        spacin\
g: 10\x0a\x0a        R\
epeater {\x0a      \
      id: legend\
Repeater\x0a       \
     model: seri\
esCount\x0a        \
    delegate: le\
gendDelegate\x0a   \
     }\x0a    }\x0a   \
 //![1]\x0a}\x0a\
\x00\x00\x0a\x06\
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
\x0a    id: main\x0a  \
  width: 400\x0a   \
 height: 320\x0a\x0a  \
  Column {\x0a     \
   id: column\x0a  \
      anchors.fi\
ll: parent\x0a     \
   anchors.botto\
mMargin: 10\x0a    \
    spacing: 0\x0a\x0a\
        ChartVie\
wSelector {\x0a    \
        id: char\
tViewSelector\x0a  \
          width:\
 parent.width\x0a  \
          height\
: parent.height \
- customLegend.h\
eight - anchors.\
bottomMargin\x0a   \
         onSerie\
sAdded: customLe\
gend.addSeries(s\
eriesName, serie\
sColor);\x0a       \
 }\x0a\x0a        Cust\
omLegend {\x0a     \
       id: custo\
mLegend\x0a        \
    width: paren\
t.width\x0a        \
    height: 50\x0a \
           ancho\
rs.horizontalCen\
ter: parent.hori\
zontalCenter\x0a   \
         onEnter\
ed: chartViewSel\
ector.highlightS\
eries(seriesName\
);\x0a            o\
nExited: chartVi\
ewSelector.highl\
ightSeries(\x22\x22);\x0a\
            onSe\
lected: chartVie\
wSelector.select\
Series(seriesNam\
e);\x0a        }\x0a  \
  }\x0a\x0a    states:\
 State {\x0a       \
 name: \x22highligh\
ted\x22\x0a        Pro\
pertyChanges {\x0a \
           targe\
t: chartViewHigh\
lighted\x0a        \
    width: colum\
n.width\x0a        \
    height: (col\
umn.height - col\
umn.anchors.marg\
ins * 2 - custom\
Legend.height)\x0a \
       }\x0a       \
 PropertyChanges\
 {\x0a            t\
arget: chartView\
Stacked\x0a        \
    width: 1\x0a   \
         height:\
 1\x0a        }\x0a   \
 }\x0a}\x0a\
\x00\x00\x0eD\
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
\x0a    id: chartVi\
ewSelector\x0a    w\
idth: parent.wid\
th\x0a    height: p\
arent.height\x0a   \
 signal seriesAd\
ded(string serie\
sName, color ser\
iesColor)\x0a\x0a    f\
unction highligh\
tSeries(seriesNa\
me) {\x0a        if\
 (seriesName == \
\x22\x22) {\x0a          \
  if (state != \x22\
\x22)\x0a             \
   state = \x22\x22;\x0a\x0a\
            for \
(var i = 0; i < \
chartViewStacked\
.count; i++)\x0a   \
             cha\
rtViewStacked.se\
ries(i).opacity \
= 1.0;\x0a        }\
 else {\x0a        \
    var targetOp\
acity = 0.1;\x0a   \
         for (va\
r j = 0; j < cha\
rtViewStacked.co\
unt; j++) {\x0a    \
            if (\
chartViewStacked\
.series(j).name \
!= seriesName)\x0a \
                \
   chartViewStac\
ked.series(j).op\
acity = 0.25;\x0a  \
              el\
se if (state == \
\x22highlight\x22)\x0a   \
                \
 chartViewSelect\
ed.selectedSerie\
s = chartViewSta\
cked.series(j);\x0a\
            }\x0a  \
      }\x0a    }\x0a\x0a \
   function sele\
ctSeries(seriesN\
ame) {\x0a        f\
or (var i = 0; i\
 < chartViewStac\
ked.count; i++) \
{\x0a            if\
 (chartViewStack\
ed.series(i).nam\
e == seriesName)\
 {\x0a             \
   chartViewSele\
cted.selectedSer\
ies = chartViewS\
tacked.series(i)\
;\x0a              \
  if (chartViewS\
elector.state ==\
 \x22\x22)\x0a           \
         chartVi\
ewSelector.state\
 = \x22highlighted\x22\
;\x0a              \
  else\x0a         \
           chart\
ViewSelector.sta\
te = \x22\x22;\x0a       \
     }\x0a        }\
\x0a    }\x0a\x0a    Char\
tViewStacked {\x0a \
       id: chart\
ViewStacked\x0a    \
    anchors.left\
: parent.left\x0a  \
      anchors.le\
ftMargin: 0\x0a    \
    width: paren\
t.width\x0a        \
height: parent.h\
eight\x0a        on\
SeriesAdded: cha\
rtViewSelector.s\
eriesAdded(serie\
s.name, series.c\
olor);\x0a    }\x0a\x0a  \
  ChartViewHighl\
ighted {\x0a       \
 id: chartViewSe\
lected\x0a        a\
nchors.left: cha\
rtViewStacked.ri\
ght\x0a        widt\
h: parent.width\x0a\
        height: \
parent.height\x0a\x0a \
       opacity: \
0.0\x0a        onCl\
icked: {\x0a       \
     chartViewSe\
lector.state = \x22\
\x22;\x0a        }\x0a   \
 }\x0a\x0a    states: \
State {\x0a        \
name: \x22highlight\
ed\x22\x0a        Prop\
ertyChanges {\x0a  \
          target\
: chartViewSelec\
ted\x0a            \
opacity: 1.0\x0a   \
     }\x0a        P\
ropertyChanges {\
\x0a            tar\
get: chartViewSt\
acked\x0a          \
  anchors.leftMa\
rgin: -chartView\
Stacked.width\x0a  \
          opacit\
y: 0.0\x0a        }\
\x0a    }\x0a\x0a    tran\
sitions: Transit\
ion {\x0a        Pr\
opertyAnimation \
{\x0a            pr\
operties: \x22width\
, height, opacit\
y, anchors.leftM\
argin\x22\x0a         \
   duration: 400\
\x0a        }\x0a    }\
\x0a}\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x0f\
\x09so\x84\
\x00q\
\x00m\x00l\x00c\x00u\x00s\x00t\x00o\x00m\x00l\x00e\x00g\x00e\x00n\x00d\
\x00\x18\
\x06T\x1c\x9c\
\x00C\
\x00h\x00a\x00r\x00t\x00V\x00i\x00e\x00w\x00H\x00i\x00g\x00h\x00l\x00i\x00g\x00h\
\x00t\x00e\x00d\x00.\x00q\x00m\x00l\
\x00\x14\
\x02\x04P|\
\x00C\
\x00h\x00a\x00r\x00t\x00V\x00i\x00e\x00w\x00S\x00t\x00a\x00c\x00k\x00e\x00d\x00.\
\x00q\x00m\x00l\
\x00\x16\
\x00\xa9\xa7\x1c\
\x00A\
\x00n\x00i\x00m\x00a\x00t\x00e\x00d\x00A\x00r\x00e\x00a\x00S\x00e\x00r\x00i\x00e\
\x00s\x00.\x00q\x00m\x00l\
\x00\x10\
\x0e\x91\xb5<\
\x00C\
\x00u\x00s\x00t\x00o\x00m\x00L\x00e\x00g\x00e\x00n\x00d\x00.\x00q\x00m\x00l\
\x00\x08\
\x08\x01Z\x5c\
\x00m\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
\x00\x15\
\x000s\x1c\
\x00C\
\x00h\x00a\x00r\x00t\x00V\x00i\x00e\x00w\x00S\x00e\x00l\x00e\x00c\x00t\x00o\x00r\
\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x06\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x01\x02\x00\x00\x00\x00\x00\x01\x00\x000v\
\x00\x00\x01\x87\xf4\x8dL\x13\
\x00\x00\x00\x94\x00\x00\x00\x00\x00\x01\x00\x00\x0e\xf5\
\x00\x00\x01\x87\xf4\x8dL\x13\
\x00\x00\x00f\x00\x01\x00\x00\x00\x01\x00\x00\x0al\
\x00\x00\x01\x87\xf4\x8dL\x13\
\x00\x00\x000\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x87\xf4\x8dL\x13\
\x00\x00\x00\xec\x00\x00\x00\x00\x00\x01\x00\x00&l\
\x00\x00\x01\x87\xf4\x8dL\x13\
\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x01\x00\x00\x14\xcd\
\x00\x00\x01\x87\xf4\x8dL\x13\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
