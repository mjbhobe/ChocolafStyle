# PyQt5 Doodle Tutorial

This is a step-by-step tutorial where we develop a rudimentary doodling application using PyQt5. The aim is to illustrate how easy it is to develop fairly rich GUI applications in Python using PyQt5.

Our application will include a standard menu bar & toolbar and will allow us to draw doodles using a mouse. A doodle is a collection of swiggles, each of which can have it's own color & thickness.

The final version will look somewhat like the image below.

<div style='background-color: yellow; color: black;'>
[TODO: Insert Final Image]()
</div>

## Requirements
- Python 3.0+ (I used Python 3.7+)
- PyQt5 framework (I use PyQt 5.15.x, with Qt 5.15.x)
- PyQt5 tools, like Designer to layout forms & dialogs.
- A text editor of your choice that provides syntax highlighting of Python code and allows you to run `*.py` files from the editor. I use Visual Studio Code or the Atom editor.


### Installing PyQt5
It is assumed that you have Python installed. A full scientific Python stack (like the one available at Ananconda.com is highly recommended, but not required)

- On the command line (Unix/Linux or Mac terminal or Windows command prompt), run _either_ of the following:
    * If you have the Anaconda distribution
        ```bash
        $> conda install -c dsdale24 pyqt5
        ```
    * You can also use pip as below (refer [this link](https://pypi.org/project/PyQt5/))
        ```bash
        $> pip install PyQt5
        ```

## Code Organization
I have developed this code in several incremental _steps_. Each _step_ has 
its own directory (e.g. `step0x`). The _main_ file in `step0x` directory is 
named `step0X.py` - where `X` designates the step number (e.g. `step01.py`). 
To _run the program_ for any step, change to the directory of that step (e.g.
`step05`) and fun the following command:
```bash
$> cd step05
$> python step05.py
```

## **NOTE**
- All code has been developed & tested on a Windows 10 and a Linux machine running KDE Plasma 5.24 (Manjaro Linux). **I have not tested this code on a Mac (as I don't own one :( )**. Screen-shots captured alternate between Windows 10 & KDE Plasma.
- The code uses a custom dark-chocolate theme (Chocolaf), developed by your's truly.
