# PyQt Doodle Tutorial

This is a step-by-step tutorial where we develop a rudimentary doodling application using PyQt. The aim is to illustrate how easy it is to develop fairly rich GUI applications in Python using PyQt.

Our application will include a standard menu bar & toolbar and will allow us to draw doodles using a mouse. A doodle is a collection of swiggles, each of which can have it's own color & thickness.

The final version will look somewhat like the image below.

<div style='background-color: yellow; color: black;'>
[<b>TODO</b>: Insert Final Image]()
</div>

## Requirements
- Python 3.0+ (I used Python 3.7+)
- PyQt framework (we'll be using PyQt6)
- PyQt tools, like Designer to layout forms & dialogs.
- A text editor of your choice that provides syntax highlighting of Python code and allows you to run `*.py` files from the editor. I use Visual Studio Code or the Atom editor.


### Installing PyQt
It is assumed that you have Python installed. A full scientific Python stack (like the one available at Ananconda.com is highly recommended, but not required)

- On the command line (Unix/Linux or Mac terminal or Windows command prompt), run _either_ of the following:
<div style='background-color: yellow; color: black;'>
[<b>TODO</b>: Change this to use <b>uv</b>]
</div>
    * If you have the Anaconda distribution
        ```bash
        $> conda install -c dsdale24 pyqt5
        ```
    * You can also use pip as below (refer [this link](https://pypi.org/project/PyQt/))
        ```bash
        $> pip install PyQt
        ```

## Code Organization
I have developed this code in several incremental _steps_. Each _step_ has its own directory (e.g. `step0x`). The _main_ file in `step0x` directory is 
named `step0X.py` - where `X` designates the step number (e.g. `step01.py`). 
To _run the program_ for any step, change to the directory of that step (e.g.
`step05`) and fun the following command:
<div style='background-color: yellow; color: black;'>
[<b>TODO</b>: Change this to use <b>uv commands</b>]
</div>

```bash
$> cd step05
$> python step05.py
OR
$> uv run step05.py
```

## **NOTE**
- All code has been developed & tested on a Windows 11 and a Linux machine running KDE Plasma 6.x (Manjaro Linux). 
- **I have not tested this code on a Mac (as I don't own one :( )**. But I think code should work without any changes as we are not using platform specific code.
- Screen-shots captured alternate between Windows 11 & KDE Plasma.
