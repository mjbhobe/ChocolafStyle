# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x0d\x9d\
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
 2.1\x0aimport QtQu\
ick.Layouts 1.0\x0a\
\x0aColumnLayout {\x0a\
    property ali\
as openGLButton:\
 openGLButton\x0a  \
  property alias\
 antialiasButton\
: antialiasButto\
n\x0a    spacing: 8\
\x0a    Layout.fill\
Height: true\x0a   \
 signal animatio\
nsEnabled(bool e\
nabled)\x0a    sign\
al seriesTypeCha\
nged(string type\
)\x0a    signal ref\
reshRateChanged(\
variant rate);\x0a \
   signal signal\
SourceChanged(st\
ring source, int\
 signalCount, in\
t sampleCount);\x0a\
    signal antia\
liasingEnabled(b\
ool enabled)\x0a   \
 signal openGlCh\
anged(bool enabl\
ed)\x0a\x0a    Text {\x0a\
        text: \x22S\
cope\x22\x0a        fo\
nt.pointSize: 18\
\x0a        color: \
\x22white\x22\x0a    }\x0a\x0a \
   MultiButton {\
\x0a        id: ope\
nGLButton\x0a      \
  text: \x22OpenGL:\
 \x22\x0a        items\
: [\x22false\x22, \x22tru\
e\x22]\x0a        curr\
entSelection: 1\x0a\
        onSelect\
ionChanged: open\
GlChanged(curren\
tSelection == 1)\
;\x0a    }\x0a\x0a    Mul\
tiButton {\x0a     \
   text: \x22Graph:\
 \x22\x0a        items\
: [\x22line\x22, \x22scat\
ter\x22]\x0a        cu\
rrentSelection: \
0\x0a        onSele\
ctionChanged: se\
riesTypeChanged(\
items[currentSel\
ection]);\x0a    }\x0a\
\x0a    MultiButton\
 {\x0a        id: s\
ignalSourceButto\
n\x0a        text: \
\x22Source: \x22\x0a     \
   items: [\x22sin\x22\
, \x22linear\x22]\x0a    \
    currentSelec\
tion: 0\x0a        \
onSelectionChang\
ed: signalSource\
Changed(\x0a       \
                \
         selecti\
on,\x0a            \
                \
    5,\x0a         \
                \
       sampleCou\
ntButton.items[s\
ampleCountButton\
.currentSelectio\
n]);\x0a    }\x0a\x0a    \
MultiButton {\x0a  \
      id: sample\
CountButton\x0a    \
    text: \x22Sampl\
es: \x22\x0a        it\
ems: [\x226\x22, \x22128\x22\
, \x221024\x22, \x2210000\
\x22]\x0a        curre\
ntSelection: 2\x0a \
       onSelecti\
onChanged: signa\
lSourceChanged(\x0a\
                \
                \
signalSourceButt\
on.items[signalS\
ourceButton.curr\
entSelection],\x0a \
                \
               5\
,\x0a              \
                \
  selection);\x0a  \
  }\x0a\x0a    MultiBu\
tton {\x0a        t\
ext: \x22Refresh ra\
te: \x22\x0a        it\
ems: [\x221\x22, \x2224\x22,\
 \x2260\x22]\x0a        c\
urrentSelection:\
 2\x0a        onSel\
ectionChanged: r\
efreshRateChange\
d(items[currentS\
election]);\x0a    \
}\x0a\x0a    MultiButt\
on {\x0a        id:\
 antialiasButton\
\x0a        text: \x22\
Antialias: \x22\x0a   \
     items: [\x22OF\
F\x22, \x22ON\x22]\x0a      \
  enabled: true\x0a\
        currentS\
election: 0\x0a    \
    onSelectionC\
hanged: antialia\
singEnabled(curr\
entSelection == \
1);\x0a    }\x0a}\x0a\
\x00\x00\x09{\
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
 2.0\x0aimport QtQu\
ick.Controls 1.0\
\x0aimport QtQuick.\
Controls.Styles \
1.0\x0a\x0aItem {\x0a    \
id: button\x0a\x0a    \
property string \
text: \x22Option: \x22\
\x0a    property va\
riant items: [\x22f\
irst\x22]\x0a    prope\
rty int currentS\
election: 0\x0a    \
signal selection\
Changed(variant \
selection)\x0a\x0a    \
signal clicked\x0a\x0a\
    implicitWidt\
h: buttonText.im\
plicitWidth + 5\x0a\
    implicitHeig\
ht: buttonText.i\
mplicitHeight + \
10\x0a\x0a    Button {\
\x0a        id: but\
tonText\x0a        \
width: parent.wi\
dth\x0a        heig\
ht: parent.heigh\
t\x0a\x0a        style\
: ButtonStyle {\x0a\
            labe\
l: Component {\x0a \
               T\
ext {\x0a          \
          text: \
button.text + bu\
tton.items[curre\
ntSelection]\x0a   \
                \
 clip: true\x0a    \
                \
wrapMode: Text.W\
ordWrap\x0a        \
            vert\
icalAlignment: T\
ext.AlignVCenter\
\x0a               \
     horizontalA\
lignment: Text.A\
lignHCenter\x0a    \
                \
anchors.fill: pa\
rent\x0a           \
     }\x0a         \
   }\x0a        }\x0a \
       onClicked\
: {\x0a            \
currentSelection\
 = (currentSelec\
tion + 1) % item\
s.length;\x0a      \
      selectionC\
hanged(button.it\
ems[currentSelec\
tion]);\x0a        \
}\x0a    }\x0a}\x0a\
\x00\x00\x12x\
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
arts 2.1\x0a\x0a//![1]\
\x0aChartView {\x0a   \
 id: chartView\x0a \
   animationOpti\
ons: ChartView.N\
oAnimation\x0a    t\
heme: ChartView.\
ChartThemeDark\x0a \
   property bool\
 openGL: true\x0a  \
  property bool \
openGLSupported:\
 true\x0a    onOpen\
GLChanged: {\x0a   \
     if (openGLS\
upported) {\x0a    \
        series(\x22\
signal 1\x22).useOp\
enGL = openGL;\x0a \
           serie\
s(\x22signal 2\x22).us\
eOpenGL = openGL\
;\x0a        }\x0a    \
}\x0a    Component.\
onCompleted: {\x0a \
       if (!seri\
es(\x22signal 1\x22).u\
seOpenGL) {\x0a    \
        openGLSu\
pported = false\x0a\
            open\
GL = false\x0a     \
   }\x0a    }\x0a\x0a    \
ValueAxis {\x0a    \
    id: axisY1\x0a \
       min: -1\x0a \
       max: 4\x0a  \
  }\x0a\x0a    ValueAx\
is {\x0a        id:\
 axisY2\x0a        \
min: -10\x0a       \
 max: 5\x0a    }\x0a\x0a \
   ValueAxis {\x0a \
       id: axisX\
\x0a        min: 0\x0a\
        max: 102\
4\x0a    }\x0a\x0a    Lin\
eSeries {\x0a      \
  id: lineSeries\
1\x0a        name: \
\x22signal 1\x22\x0a     \
   axisX: axisX\x0a\
        axisY: a\
xisY1\x0a        us\
eOpenGL: chartVi\
ew.openGL\x0a    }\x0a\
    LineSeries {\
\x0a        id: lin\
eSeries2\x0a       \
 name: \x22signal 2\
\x22\x0a        axisX:\
 axisX\x0a        a\
xisYRight: axisY\
2\x0a        useOpe\
nGL: chartView.o\
penGL\x0a    }\x0a//![\
1]\x0a\x0a    //![2]\x0a \
   Timer {\x0a     \
   id: refreshTi\
mer\x0a        inte\
rval: 1 / 60 * 1\
000 // 60 Hz\x0a   \
     running: tr\
ue\x0a        repea\
t: true\x0a        \
onTriggered: {\x0a \
           dataS\
ource.update(cha\
rtView.series(0)\
);\x0a            d\
ataSource.update\
(chartView.serie\
s(1));\x0a        }\
\x0a    }\x0a    //![2\
]\x0a\x0a    //![3]\x0a  \
  function chang\
eSeriesType(type\
) {\x0a        char\
tView.removeAllS\
eries();\x0a\x0a      \
  // Create two \
new series of th\
e correct type. \
Axis x is the sa\
me for both of t\
he series,\x0a     \
   // but the se\
ries have their \
own y-axes to ma\
ke it possible t\
o control the y-\
offset\x0a        /\
/ of the \x22signal\
 sources\x22.\x0a     \
   if (type == \x22\
line\x22) {\x0a       \
     var series1\
 = chartView.cre\
ateSeries(ChartV\
iew.SeriesTypeLi\
ne, \x22signal 1\x22,\x0a\
                \
                \
                \
 axisX, axisY1);\
\x0a            ser\
ies1.useOpenGL =\
 chartView.openG\
L\x0a\x0a            v\
ar series2 = cha\
rtView.createSer\
ies(ChartView.Se\
riesTypeLine, \x22s\
ignal 2\x22,\x0a      \
                \
                \
           axisX\
, axisY2);\x0a     \
       series2.u\
seOpenGL = chart\
View.openGL\x0a    \
    } else {\x0a   \
         var ser\
ies1 = chartView\
.createSeries(Ch\
artView.SeriesTy\
peScatter, \x22sign\
al 1\x22,\x0a         \
                \
                \
        axisX, a\
xisY1);\x0a        \
    series1.mark\
erSize = 2;\x0a    \
        series1.\
borderColor = \x22t\
ransparent\x22;\x0a   \
         series1\
.useOpenGL = cha\
rtView.openGL\x0a\x0a \
           var s\
eries2 = chartVi\
ew.createSeries(\
ChartView.Series\
TypeScatter, \x22si\
gnal 2\x22,\x0a       \
                \
                \
          axisX,\
 axisY2);\x0a      \
      series2.ma\
rkerSize = 2;\x0a  \
          series\
2.borderColor = \
\x22transparent\x22;\x0a \
           serie\
s2.useOpenGL = c\
hartView.openGL\x0a\
        }\x0a    }\x0a\
\x0a    function cr\
eateAxis(min, ma\
x) {\x0a        // \
The following cr\
eates a ValueAxi\
s object that ca\
n be then set as\
 a x or y axis f\
or a series\x0a    \
    return Qt.cr\
eateQmlObject(\x22i\
mport QtQuick 2.\
0; import QtChar\
ts 2.0; ValueAxi\
s { min: \x22\x0a     \
                \
             + m\
in + \x22; max: \x22 +\
 max + \x22 }\x22, cha\
rtView);\x0a    }\x0a \
   //![3]\x0a\x0a    f\
unction setAnima\
tions(enabled) {\
\x0a        if (ena\
bled)\x0a          \
  chartView.anim\
ationOptions = C\
hartView.SeriesA\
nimations;\x0a     \
   else\x0a        \
    chartView.an\
imationOptions =\
 ChartView.NoAni\
mation;\x0a    }\x0a\x0a \
   function chan\
geRefreshRate(ra\
te) {\x0a        re\
freshTimer.inter\
val = 1 / Number\
(rate) * 1000;\x0a \
   }\x0a}\x0a\
\x00\x00\x0a`\
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
 2.0\x0a\x0a//![1]\x0aIte\
m {\x0a    id: main\
\x0a    width: 600\x0a\
    height: 400\x0a\
\x0a    ControlPane\
l {\x0a        id: \
controlPanel\x0a   \
     anchors.top\
: parent.top\x0a   \
     anchors.top\
Margin: 10\x0a     \
   anchors.botto\
m: parent.bottom\
\x0a        anchors\
.left: parent.le\
ft\x0a        ancho\
rs.leftMargin: 1\
0\x0a//![1]\x0a\x0a      \
  onSignalSource\
Changed: {\x0a     \
       if (sourc\
e == \x22sin\x22)\x0a    \
            data\
Source.generateD\
ata(0, signalCou\
nt, sampleCount)\
;\x0a            el\
se\x0a             \
   dataSource.ge\
nerateData(1, si\
gnalCount, sampl\
eCount);\x0a       \
     scopeView.a\
xisX().max = sam\
pleCount;\x0a      \
  }\x0a        onSe\
riesTypeChanged:\
 scopeView.chang\
eSeriesType(type\
);\x0a        onRef\
reshRateChanged:\
 scopeView.chang\
eRefreshRate(rat\
e);\x0a        onAn\
tialiasingEnable\
d: scopeView.ant\
ialiasing = enab\
led;\x0a        onO\
penGlChanged: {\x0a\
            scop\
eView.openGL = e\
nabled;\x0a        \
}\x0a    }\x0a\x0a//![2]\x0a\
    ScopeView {\x0a\
        id: scop\
eView\x0a        an\
chors.top: paren\
t.top\x0a        an\
chors.bottom: pa\
rent.bottom\x0a    \
    anchors.righ\
t: parent.right\x0a\
        anchors.\
left: controlPan\
el.right\x0a       \
 height: main.he\
ight\x0a\x0a        on\
OpenGLSupportedC\
hanged: {\x0a      \
      if (!openG\
LSupported) {\x0a  \
              co\
ntrolPanel.openG\
LButton.enabled \
= false\x0a        \
        controlP\
anel.openGLButto\
n.currentSelecti\
on = 0\x0a         \
   }\x0a        }\x0a \
   }\x0a//![2]\x0a\x0a}\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00x<\
\x00q\
\x00m\x00l\
\x00\x0f\
\x05\xbb\x87\x05\
\x00q\
\x00m\x00l\x00o\x00s\x00c\x00i\x00l\x00l\x00o\x00s\x00c\x00o\x00p\x00e\
\x00\x10\
\x03\x81\xe5\xdc\
\x00C\
\x00o\x00n\x00t\x00r\x00o\x00l\x00P\x00a\x00n\x00e\x00l\x00.\x00q\x00m\x00l\
\x00\x0f\
\x0c;>\x5c\
\x00M\
\x00u\x00l\x00t\x00i\x00B\x00u\x00t\x00t\x00o\x00n\x00.\x00q\x00m\x00l\
\x00\x0d\
\x0c\x86\x84\xdc\
\x00S\
\x00c\x00o\x00p\x00e\x00V\x00i\x00e\x00w\x00.\x00q\x00m\x00l\
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
\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x04\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x000\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x87_\xcdZZ\
\x00\x00\x00\x9a\x00\x00\x00\x00\x00\x01\x00\x00)\x9c\
\x00\x00\x01\x87_\xcdZZ\
\x00\x00\x00V\x00\x00\x00\x00\x00\x01\x00\x00\x0d\xa1\
\x00\x00\x01\x87_\xcdZZ\
\x00\x00\x00z\x00\x00\x00\x00\x00\x01\x00\x00\x17 \
\x00\x00\x01\x87_\xcdZZ\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
