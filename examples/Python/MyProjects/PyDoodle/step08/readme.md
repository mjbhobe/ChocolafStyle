# PyQt5 Doodle Tutorial

## Step 6 - Adding multiple Squiggles
What we have achieved so far
- We created a custom main window for our application
- Added event handlers to underlying operating system events
    - Added `mouse event` handlers to accumulate points for our squiggle
    - Added a `paint event` handler to draw the squiggle
    - Added `close event` handler to check if it was Ok to close the application.
    - We also leveregad the `mouse events` to change our pen width & color
But we have been able to draw just one line so far - very limiting from the Doodling point of view. In this step we will make several changes to our code that will allow us to draw multiple squiggles, each with their own thickness & color. This will enable us to draw sufficiently complex Doodles, like the one shown below:

![I love PyQt](./images/Step06-ILoveQt.png)

Let's begin

## Separating the `squiggle` into its own class
We'll create a separate class for the Squiggle, which will enable us to create several squiggles and set pen width and color separately for each squiggle.

- Create a new file `squiggle.py` in the `step06` folder & add the following code:

```python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Squiggle(QObject):
    """
    class for a Squiggle in the doodle
    """
    def __init__(self, penWidth=3, penColor=QColor(qRgb(0,65,255))):
        super(QObject, self).__init__()
        self.__penWidth = 1
        self.__penColor = qRgb(0,0,0)
        # the squiggle has its own pen width & color
        self.penWidth = penWidth
        self.penColor = penColor
        self.points = []

    @property
    def penWidth(self):
        return self.__penWidth

    @penWidth.setter
    def penWidth(self, penWidth):
        newWidth = min(max(2, penWidth), 12)
        if (penWidth < 2) or (penWidth > 12):
            qDebug(f"WARNING: incorrect value for penWidth ({penWidth}). Expecting value between 2 & 12. Set to {newWidth}")
        if self.penWidth != newWidth:
            self.__penWidth = newWidth

    @property
    def penColor(self):
        return self.__penColor

    @penColor.setter
    def penColor(self, penColor):
        if self.penColor != penColor:
            self.__penColor = penColor

    def numPoints(self):
        return len(self.points)

    def append(self, pt: QPoint) -> None:
        self.points.append(pt)

    def draw(self, painter: QPainter) -> None:
        # squiggle has it's own method to draw on QPainter
        if self.numPoints() > 0:
            pen = QPen(self.penColor, self.penWidth)
            painter.setPen(pen)
            lastPt = None
            for i, pt in enumerate(self.points):
                if i > 0:
                    painter.drawLine(lastPt, pt)
                lastPt = pt
```


<span style="background-color:yellow; color:black"><b>TODO:</b>Complete Tutorial above....</span>

However, our squiggle was painted with the pen thickness and color that we set in the `DrawWindow.__init__(...)` method and there were no means provided to change these through the user interface. In this step, we will give the user the ability to change the squiggle's pen width and color.

## Using pre-canned or common dialogs
PyQt5 makes available several _pre-canned_ dialogs, which you can use out of the box. Several dialogs are available, for example:
- `QInputDialog`: which allows you to get simple input from the user in the form of text, integer or floats.
- `QFileDialog`: standard dialog used to choose file(s) to open & save.
- `QColorDialog`: standard dialog use to pick a color.
- `QPrintDialog`: standard print dialog
- `QFontDialog` : to select a font to use.
- `QMessageBox` : dialog to display a message to the user. We have used this dialog in our previous steps.

and so on...

In this step, we'll be using the `QInputDialog` and the `QColorDialog` to help with setting the pen thickness and color of the squiggle respectively.

Recall that we had defined 2 attributes of the `MainWindow` class - `penWidth` and `penColor`. We'll now proceed to show you how you can get the user to change values for these attributes using standard dialogs.

### Changing the `penWidth`
We will use the `QInputDialog.getInt(...)` call to get the new pen width from the user. Here is how you call the dialog:

```python
newWidth, ok = QInputDialog.getInt(
    self,           # parent of dialog
    "Pen Width",    # title of dialog
    # prompt to user above the input field
    "Enter new pen width (2-12):",
    self.penWidth,  # starting value in input field
    2, 12)          # min-max range of value
if ok:  
    self.penWidth = newWidth
```

Once called, this is what you will see:

![InputDialog](./images/Step05-InputDialog.png)

- Read the comments in the code while referring to the image above to co-relate the commenents with the code.
- The `getInt(..)` call forces an `int` value from the user. Since we are also providing a min-max range `(2-12)`, the input field is a `spinBox`.
- Since we set the initial value of `self.penWidth = 3`, that is the value you see in the `spinBox`.
- You can _spin_ the `spinBox` or enter a value of your choice (between the ranges `(2-12)`).
- Click `OK` to accept the value you entered & close dialog or press `Cancel` to close

This dialog returns 2 values, which we _capture_ in variables `newWidth` and `ok`.
- If the user clicks `OK` on the dialog box, then our variable `ok = True`. If user clicks `Cancel` on the dialog, `ok = False`. So we must check if user clicked `OK` button on dialog before doing anything with the value in `newWidth`
- If `ok == True`, the `newWidth` variable will hold the value chosen by user in the dialog. Hence our `if ok == True` block.

Now that we have seen how to accept the new value for `penWidth`, one issue remains: Where do we put this code? Since
we have not yet introduced standard GUI features such as toolbars and menus, we will use a rather rudimentary
approach in this step. We'll display this dialog in the `left mouse press` event handler _provided_ the `Control` key (or `Command` key on the Mac) is also pressed simultaneously (i.e. a `Ctrl+left-mouse-press` action will trigger this dialog).

**NOTE: This approach is NOT recommended in professional GUIs as it is non-intuitive. We'll correct this in subsequent steps.**

Let's modify our `mousePressEvent(...)` function as shown below:

```python
class DrawWindow(QMainWindow):
    ...
    # other functions hidden for brevity...
    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse press (left or right button) events """
        if e.button() == Qt.LeftButton:
            if (e.modifiers() == Qt.ControlModifier):
                # if Ctrl/Command key is also pressed with mouse press, display
                # dialog to change pen thickness
                newWidth, ok = QInputDialog.getInt(self, 
                    "Pen Width",
                    "Enter new pen width (2-12):",
                    self.penWidth, 2, 12)
                if ok:  # user clicked Ok on QInputDialog
                    self.penWidth = newWidth                
            else:
                # clear any previous doodle(s)
                self.points = []
                # start a new doodle
                pt = QPoint(e.pos().x(), e.pos().y())
                #print(f"Got mousePressEvent at ({pt.x()}, {pt.y()})")
                self.points.append(pt)
                self.modified = True
                self.dragging = True
        elif e.button() == Qt.RightButton:
            self.points = []
            self.modified = False
            self.update()

```
To check if the `ctrl` (`Command` on the Mac) key is also pressed, we use the following code:
```python
if (e.modifiers() == Qt.ControlModifier):
    # -- rest of the code
```
So our `QInputDialog` is displayed only if `Ctrl+left-mouse-press` event is received.

If you run the code now and do the following steps:
- Draw a squiggle. It will be drawn in the default pen thickness (`= 3`). Somwhat like shown  below (from `Step04`):

![Default Pen Width](./images/Step04-DrawSquiggle.png)

- Press the left mouse button while holding down the `Ctrl` key (or `Command` key on the Mac), you should see the following dialog. Notice that the initial value of `penWidth` displayed `= 3`. 

![Pen Width Dialog](./images/Step05-InputDialogClick.png)

- Enter new value of pen (between 2 & 12) or spin the `spinBox` to choose a new value. Click `OK` to accept the new value.
- Now drag the mouse in the client area, line with chosen thickness will be drawn, as shown below.

![Squiggle With New Pen Thickness](./images/Step05-DrawSquiggleNewThick.png)

### Changing the `penColor`
To change the pen color we'll use another pre-canned dialog `QColorDialog` that is provided by `PyQt5`. 

Calling this dialog is much simpler & is done as shown below:
```python
newColor = QColorDialog.getColor(self.penColor, self)
if newColor.isValid():
    self.penColor = newColor
```
- We pass the _initial_ color to the `QColorDialog` as the first parameter along with the parent window as the second parameter.
- If the user chooses a color & clicks `OK` on the `QColorDialog`, then a _valid_ color is returned. Hence the check `if newColor.isValid()`

We'll call this dialog when the `Ctrl+right-mouse-press` event is caught (i.e. when the `right mouse` button is pressed when the `Ctrl` key [`Command` key on the Mac] is held down.)

Here is the modified `mousePressEvent` to handle the `right-mouse-press` event:

```python
def mousePressEvent(self, e: QMouseEvent) -> None:
        """ handler for mouse press (left or right button) events """
        if e.button() == Qt.LeftButton:
            # code omitted for brevity...
        elif e.button() == Qt.RightButton:
            if (e.modifiers() == Qt.ControlModifier):
                # if Ctrl key is also pressed with mouse press, display
                # dialog to change pen color
                newColor = QColorDialog.getColor(self.penColor, self)
                if newColor.isValid():
                    self.penColor = newColor
            else:
                self.points = []
                self.modified = False
                self.update()
```
If you run the code now and do the following steps:
- Draw a squiggle. It will be drawn in the default pen thickness (`= 3`) and blue color (`=RGB(0,65,255)`). Somewhat like shown  below (from `Step04`):

![Default Pen Color](./images/Step04-DrawSquiggle.png)

- Right press the mouse button while holding down the `Ctrl` key (`Command` key on the Mac). You should see the `QColorDialog` as shown below:

Notice that the default color has been selected by the dialog - this is because we passed this value as the _initial_ color (`= RGB(0,65,255)`)

![Color Dialog](./images/Step05-ColorDialog.png)

- Select a new pen color of your choice. For example, I have selected green color (`=(RGB(0,120,0)`)

![Pick New Color](./images/Step05-ColorDialogColorSelect.png)

- Click on the `OK` button to select the color. Start drawing a new squiggle. You should see the squiggle in the color you selected. For example, my squiggle is in green color.

![Draw New Color](./images/Step05-DrawNewColor.png)

<hr/>

<span style="color:blue">This completes Step5 of our tutorial</span>, where we demonstrated how you can use `PyQt5` provided pre-canned (or standard) dialogs, like `QInputDialog` and `QColorDialog` to change the pen width and pen color.

<br/>

__NOTE:__ I have written this tutorial on a Ubuntu Linux machine, so the window look & feel is specific to my OS. On a Windows machine, the look & feel will be native to Windows, and likewise on a Mac. However, you won't have to change your code - PyQt5 handles the low level stuff for you.
