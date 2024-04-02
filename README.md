# Assignment 3 
## UI
We try to build a simple browser-based GUI application with PyWebIO, which provides a series of imperative functions to obtain user input and output on the browser, turning the browser into a "rich text terminal".

## Installation

Stable version:

```bash
pip3 install -U pywebio
```

Development version:
```bash
pip3 install -U https://github.com/pywebio/PyWebIO/archive/dev-release.zip
```

**Prerequisites**: PyWebIO requires Python 3.5.2 or newer

## Script
```bash
python GUI_option_pricer.py
```

**Serve as web service**
The program will be opened in Chrome.
<p align="center">
    <a href="http://pywebio-demos.pywebio.online/?pywebio_api=bmi">
        <img src="https://raw.githubusercontent.com/wang0618/PyWebIO/dev/docs/assets/demo.gif" alt="PyWebIO demo" width="400px"/>
    </a>
</p>


**Step 1: Choose the class of your option**<br/>
First you need to choose the type of option you want to compute.

**Step 2: Input parameters**<br/>
Then you need to enter the parameters of your option.

<img src="https://github.com/chixnran/COMP7405Assignment3/assets/144542687/b9244284-af6b-4b3f-b1ac-968bed9b1786" width="300" height="200">

**Step 3: Computation**<br/>
Click 'Submit' to conduct computing.

The above pricer will exit immediately after the calculation.

