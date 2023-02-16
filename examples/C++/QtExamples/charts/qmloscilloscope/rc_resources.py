# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.4.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x0e\x04\
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
1\x0d\x0aimport QtQuic\
k.Layouts 1.0\x0d\x0a\x0d\
\x0aColumnLayout {\x0d\
\x0a    property al\
ias openGLButton\
: openGLButton\x0d\x0a\
    property ali\
as antialiasButt\
on: antialiasBut\
ton\x0d\x0a    spacing\
: 8\x0d\x0a    Layout.\
fillHeight: true\
\x0d\x0a    signal ani\
mationsEnabled(b\
ool enabled)\x0d\x0a  \
  signal seriesT\
ypeChanged(strin\
g type)\x0d\x0a    sig\
nal refreshRateC\
hanged(variant r\
ate);\x0d\x0a    signa\
l signalSourceCh\
anged(string sou\
rce, int signalC\
ount, int sample\
Count);\x0d\x0a    sig\
nal antialiasing\
Enabled(bool ena\
bled)\x0d\x0a    signa\
l openGlChanged(\
bool enabled)\x0d\x0a\x0d\
\x0a    Text {\x0d\x0a   \
     text: \x22Scop\
e\x22\x0d\x0a        font\
.pointSize: 18\x0d\x0a\
        color: \x22\
white\x22\x0d\x0a    }\x0d\x0a\x0d\
\x0a    MultiButton\
 {\x0d\x0a        id: \
openGLButton\x0d\x0a  \
      text: \x22Ope\
nGL: \x22\x0d\x0a        \
items: [\x22false\x22,\
 \x22true\x22]\x0d\x0a      \
  currentSelecti\
on: 1\x0d\x0a        o\
nSelectionChange\
d: openGlChanged\
(currentSelectio\
n == 1);\x0d\x0a    }\x0d\
\x0a\x0d\x0a    MultiButt\
on {\x0d\x0a        te\
xt: \x22Graph: \x22\x0d\x0a \
       items: [\x22\
line\x22, \x22scatter\x22\
]\x0d\x0a        curre\
ntSelection: 0\x0d\x0a\
        onSelect\
ionChanged: seri\
esTypeChanged(it\
ems[currentSelec\
tion]);\x0d\x0a    }\x0d\x0a\
\x0d\x0a    MultiButto\
n {\x0d\x0a        id:\
 signalSourceBut\
ton\x0d\x0a        tex\
t: \x22Source: \x22\x0d\x0a \
       items: [\x22\
sin\x22, \x22linear\x22]\x0d\
\x0a        current\
Selection: 0\x0d\x0a  \
      onSelectio\
nChanged: signal\
SourceChanged(\x0d\x0a\
                \
                \
selection,\x0d\x0a    \
                \
            5,\x0d\x0a\
                \
                \
sampleCountButto\
n.items[sampleCo\
untButton.curren\
tSelection]);\x0d\x0a \
   }\x0d\x0a\x0d\x0a    Mult\
iButton {\x0d\x0a     \
   id: sampleCou\
ntButton\x0d\x0a      \
  text: \x22Samples\
: \x22\x0d\x0a        ite\
ms: [\x226\x22, \x22128\x22,\
 \x221024\x22, \x2210000\x22\
]\x0d\x0a        curre\
ntSelection: 2\x0d\x0a\
        onSelect\
ionChanged: sign\
alSourceChanged(\
\x0d\x0a              \
                \
  signalSourceBu\
tton.items[signa\
lSourceButton.cu\
rrentSelection],\
\x0d\x0a              \
                \
  5,\x0d\x0a          \
                \
      selection)\
;\x0d\x0a    }\x0d\x0a\x0d\x0a    \
MultiButton {\x0d\x0a \
       text: \x22Re\
fresh rate: \x22\x0d\x0a \
       items: [\x22\
1\x22, \x2224\x22, \x2260\x22]\x0d\
\x0a        current\
Selection: 2\x0d\x0a  \
      onSelectio\
nChanged: refres\
hRateChanged(ite\
ms[currentSelect\
ion]);\x0d\x0a    }\x0d\x0a\x0d\
\x0a    MultiButton\
 {\x0d\x0a        id: \
antialiasButton\x0d\
\x0a        text: \x22\
Antialias: \x22\x0d\x0a  \
      items: [\x22O\
FF\x22, \x22ON\x22]\x0d\x0a    \
    enabled: tru\
e\x0d\x0a        curre\
ntSelection: 0\x0d\x0a\
        onSelect\
ionChanged: anti\
aliasingEnabled(\
currentSelection\
 == 1);\x0d\x0a    }\x0d\x0a\
}\x0d\x0a\
\x00\x00\x09\xc0\
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
0\x0d\x0aimport QtQuic\
k.Controls 1.0\x0d\x0a\
import QtQuick.C\
ontrols.Styles 1\
.0\x0d\x0a\x0d\x0aItem {\x0d\x0a  \
  id: button\x0d\x0a\x0d\x0a\
    property str\
ing text: \x22Optio\
n: \x22\x0d\x0a    proper\
ty variant items\
: [\x22first\x22]\x0d\x0a   \
 property int cu\
rrentSelection: \
0\x0d\x0a    signal se\
lectionChanged(v\
ariant selection\
)\x0d\x0a\x0d\x0a    signal \
clicked\x0d\x0a\x0d\x0a    i\
mplicitWidth: bu\
ttonText.implici\
tWidth + 5\x0d\x0a    \
implicitHeight: \
buttonText.impli\
citHeight + 10\x0d\x0a\
\x0d\x0a    Button {\x0d\x0a\
        id: butt\
onText\x0d\x0a        \
width: parent.wi\
dth\x0d\x0a        hei\
ght: parent.heig\
ht\x0d\x0a\x0d\x0a        st\
yle: ButtonStyle\
 {\x0d\x0a            \
label: Component\
 {\x0d\x0a            \
    Text {\x0d\x0a    \
                \
text: button.tex\
t + button.items\
[currentSelectio\
n]\x0d\x0a            \
        clip: tr\
ue\x0d\x0a            \
        wrapMode\
: Text.WordWrap\x0d\
\x0a               \
     verticalAli\
gnment: Text.Ali\
gnVCenter\x0d\x0a     \
               h\
orizontalAlignme\
nt: Text.AlignHC\
enter\x0d\x0a         \
           ancho\
rs.fill: parent\x0d\
\x0a               \
 }\x0d\x0a            \
}\x0d\x0a        }\x0d\x0a  \
      onClicked:\
 {\x0d\x0a            \
currentSelection\
 = (currentSelec\
tion + 1) % item\
s.length;\x0d\x0a     \
       selection\
Changed(button.i\
tems[currentSele\
ction]);\x0d\x0a      \
  }\x0d\x0a    }\x0d\x0a}\x0d\x0a\
\x00\x00\x13\x0b\
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
ts 2.1\x0d\x0a\x0d\x0a//![1]\
\x0d\x0aChartView {\x0d\x0a \
   id: chartView\
\x0d\x0a    animationO\
ptions: ChartVie\
w.NoAnimation\x0d\x0a \
   theme: ChartV\
iew.ChartThemeDa\
rk\x0d\x0a    property\
 bool openGL: tr\
ue\x0d\x0a    property\
 bool openGLSupp\
orted: true\x0d\x0a   \
 onOpenGLChanged\
: {\x0d\x0a        if \
(openGLSupported\
) {\x0d\x0a           \
 series(\x22signal \
1\x22).useOpenGL = \
openGL;\x0d\x0a       \
     series(\x22sig\
nal 2\x22).useOpenG\
L = openGL;\x0d\x0a   \
     }\x0d\x0a    }\x0d\x0a \
   Component.onC\
ompleted: {\x0d\x0a   \
     if (!series\
(\x22signal 1\x22).use\
OpenGL) {\x0d\x0a     \
       openGLSup\
ported = false\x0d\x0a\
            open\
GL = false\x0d\x0a    \
    }\x0d\x0a    }\x0d\x0a\x0d\x0a\
    ValueAxis {\x0d\
\x0a        id: axi\
sY1\x0d\x0a        min\
: -1\x0d\x0a        ma\
x: 4\x0d\x0a    }\x0d\x0a\x0d\x0a \
   ValueAxis {\x0d\x0a\
        id: axis\
Y2\x0d\x0a        min:\
 -10\x0d\x0a        ma\
x: 5\x0d\x0a    }\x0d\x0a\x0d\x0a \
   ValueAxis {\x0d\x0a\
        id: axis\
X\x0d\x0a        min: \
0\x0d\x0a        max: \
1024\x0d\x0a    }\x0d\x0a\x0d\x0a \
   LineSeries {\x0d\
\x0a        id: lin\
eSeries1\x0d\x0a      \
  name: \x22signal \
1\x22\x0d\x0a        axis\
X: axisX\x0d\x0a      \
  axisY: axisY1\x0d\
\x0a        useOpen\
GL: chartView.op\
enGL\x0d\x0a    }\x0d\x0a   \
 LineSeries {\x0d\x0a \
       id: lineS\
eries2\x0d\x0a        \
name: \x22signal 2\x22\
\x0d\x0a        axisX:\
 axisX\x0d\x0a        \
axisYRight: axis\
Y2\x0d\x0a        useO\
penGL: chartView\
.openGL\x0d\x0a    }\x0d\x0a\
//![1]\x0d\x0a\x0d\x0a    //\
![2]\x0d\x0a    Timer \
{\x0d\x0a        id: r\
efreshTimer\x0d\x0a   \
     interval: 1\
 / 60 * 1000 // \
60 Hz\x0d\x0a        r\
unning: true\x0d\x0a  \
      repeat: tr\
ue\x0d\x0a        onTr\
iggered: {\x0d\x0a    \
        dataSour\
ce.update(chartV\
iew.series(0));\x0d\
\x0a            dat\
aSource.update(c\
hartView.series(\
1));\x0d\x0a        }\x0d\
\x0a    }\x0d\x0a    //![\
2]\x0d\x0a\x0d\x0a    //![3]\
\x0d\x0a    function c\
hangeSeriesType(\
type) {\x0d\x0a       \
 chartView.remov\
eAllSeries();\x0d\x0a\x0d\
\x0a        // Crea\
te two new serie\
s of the correct\
 type. Axis x is\
 the same for bo\
th of the series\
,\x0d\x0a        // bu\
t the series hav\
e their own y-ax\
es to make it po\
ssible to contro\
l the y-offset\x0d\x0a\
        // of th\
e \x22signal source\
s\x22.\x0d\x0a        if \
(type == \x22line\x22)\
 {\x0d\x0a            \
var series1 = ch\
artView.createSe\
ries(ChartView.S\
eriesTypeLine, \x22\
signal 1\x22,\x0d\x0a    \
                \
                \
             axi\
sX, axisY1);\x0d\x0a  \
          series\
1.useOpenGL = ch\
artView.openGL\x0d\x0a\
\x0d\x0a            va\
r series2 = char\
tView.createSeri\
es(ChartView.Ser\
iesTypeLine, \x22si\
gnal 2\x22,\x0d\x0a      \
                \
                \
           axisX\
, axisY2);\x0d\x0a    \
        series2.\
useOpenGL = char\
tView.openGL\x0d\x0a  \
      } else {\x0d\x0a\
            var \
series1 = chartV\
iew.createSeries\
(ChartView.Serie\
sTypeScatter, \x22s\
ignal 1\x22,\x0d\x0a     \
                \
                \
            axis\
X, axisY1);\x0d\x0a   \
         series1\
.markerSize = 2;\
\x0d\x0a            se\
ries1.borderColo\
r = \x22transparent\
\x22;\x0d\x0a            \
series1.useOpenG\
L = chartView.op\
enGL\x0d\x0a\x0d\x0a        \
    var series2 \
= chartView.crea\
teSeries(ChartVi\
ew.SeriesTypeSca\
tter, \x22signal 2\x22\
,\x0d\x0a             \
                \
                \
    axisX, axisY\
2);\x0d\x0a           \
 series2.markerS\
ize = 2;\x0d\x0a      \
      series2.bo\
rderColor = \x22tra\
nsparent\x22;\x0d\x0a    \
        series2.\
useOpenGL = char\
tView.openGL\x0d\x0a  \
      }\x0d\x0a    }\x0d\x0a\
\x0d\x0a    function c\
reateAxis(min, m\
ax) {\x0d\x0a        /\
/ The following \
creates a ValueA\
xis object that \
can be then set \
as a x or y axis\
 for a series\x0d\x0a \
       return Qt\
.createQmlObject\
(\x22import QtQuick\
 2.0; import QtC\
harts 2.0; Value\
Axis { min: \x22\x0d\x0a \
                \
                \
 + min + \x22; max:\
 \x22 + max + \x22 }\x22,\
 chartView);\x0d\x0a  \
  }\x0d\x0a    //![3]\x0d\
\x0a\x0d\x0a    function \
setAnimations(en\
abled) {\x0d\x0a      \
  if (enabled)\x0d\x0a\
            char\
tView.animationO\
ptions = ChartVi\
ew.SeriesAnimati\
ons;\x0d\x0a        el\
se\x0d\x0a            \
chartView.animat\
ionOptions = Cha\
rtView.NoAnimati\
on;\x0d\x0a    }\x0d\x0a\x0d\x0a  \
  function chang\
eRefreshRate(rat\
e) {\x0d\x0a        re\
freshTimer.inter\
val = 1 / Number\
(rate) * 1000;\x0d\x0a\
    }\x0d\x0a}\x0d\x0a\
\x00\x00\x0a\xb0\
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
0\x0d\x0a\x0d\x0a//![1]\x0d\x0aIte\
m {\x0d\x0a    id: mai\
n\x0d\x0a    width: 60\
0\x0d\x0a    height: 4\
00\x0d\x0a\x0d\x0a    Contro\
lPanel {\x0d\x0a      \
  id: controlPan\
el\x0d\x0a        anch\
ors.top: parent.\
top\x0d\x0a        anc\
hors.topMargin: \
10\x0d\x0a        anch\
ors.bottom: pare\
nt.bottom\x0d\x0a     \
   anchors.left:\
 parent.left\x0d\x0a  \
      anchors.le\
ftMargin: 10\x0d\x0a//\
![1]\x0d\x0a\x0d\x0a        \
onSignalSourceCh\
anged: {\x0d\x0a      \
      if (source\
 == \x22sin\x22)\x0d\x0a    \
            data\
Source.generateD\
ata(0, signalCou\
nt, sampleCount)\
;\x0d\x0a            e\
lse\x0d\x0a           \
     dataSource.\
generateData(1, \
signalCount, sam\
pleCount);\x0d\x0a    \
        scopeVie\
w.axisX().max = \
sampleCount;\x0d\x0a  \
      }\x0d\x0a       \
 onSeriesTypeCha\
nged: scopeView.\
changeSeriesType\
(type);\x0d\x0a       \
 onRefreshRateCh\
anged: scopeView\
.changeRefreshRa\
te(rate);\x0d\x0a     \
   onAntialiasin\
gEnabled: scopeV\
iew.antialiasing\
 = enabled;\x0d\x0a   \
     onOpenGlCha\
nged: {\x0d\x0a       \
     scopeView.o\
penGL = enabled;\
\x0d\x0a        }\x0d\x0a   \
 }\x0d\x0a\x0d\x0a//![2]\x0d\x0a  \
  ScopeView {\x0d\x0a \
       id: scope\
View\x0d\x0a        an\
chors.top: paren\
t.top\x0d\x0a        a\
nchors.bottom: p\
arent.bottom\x0d\x0a  \
      anchors.ri\
ght: parent.righ\
t\x0d\x0a        ancho\
rs.left: control\
Panel.right\x0d\x0a   \
     height: mai\
n.height\x0d\x0a\x0d\x0a    \
    onOpenGLSupp\
ortedChanged: {\x0d\
\x0a            if \
(!openGLSupporte\
d) {\x0d\x0a          \
      controlPan\
el.openGLButton.\
enabled = false\x0d\
\x0a               \
 controlPanel.op\
enGLButton.curre\
ntSelection = 0\x0d\
\x0a            }\x0d\x0a\
        }\x0d\x0a    }\
\x0d\x0a//![2]\x0d\x0a\x0d\x0a}\x0d\x0a\
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
\x00\x00\x01\x83\x97f\x8e\x0c\
\x00\x00\x00\x9a\x00\x00\x00\x00\x00\x01\x00\x00*\xdb\
\x00\x00\x01\x83\x97f\x8e\x16\
\x00\x00\x00V\x00\x00\x00\x00\x00\x01\x00\x00\x0e\x08\
\x00\x00\x01\x83\x97f\x8e\x16\
\x00\x00\x00z\x00\x00\x00\x00\x00\x01\x00\x00\x17\xcc\
\x00\x00\x01\x83\x97f\x8e\x16\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
