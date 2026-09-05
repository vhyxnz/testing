# Tindahan ni Aling Nena

## Play without Python (Windows)

Double-click `dist/SariSariStore.exe`. This standalone Windows 64-bit build
includes Python, Ursina, and its assets. You may copy the EXE to another folder
or Windows PC; no installation or internet connection is needed to play.
The first launch can take a few seconds while the bundled files unpack.

To rebuild from source after installing dependencies and `pyinstaller`:

```powershell
python -m PyInstaller --noconfirm SariSariStore.spec
```

A playable, procedural 3D sari-sari store in a single Python script. Includes a
fixed first-person cashier view, wooden estante, colorful hanging sachets, glass
aparador, security grille, bell, and customers who approach and leave the window.
All visuals use built-in engine primitives; the bell uses a visible **Ting!** cue.

## Install and run

Install Python 3.12 or newer and use a computer with working OpenGL graphics drivers.
From this folder, run:

```sh
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS / Linux:

```sh
source .venv/bin/activate
```

Then install and launch:

```sh
python -m pip install -r requirements.txt
python sari_sari.py
```

If Windows uses the Python launcher, substitute `py -3.12` for `python` when
creating the environment. You can also skip activation and run
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, followed by
`.\.venv\Scripts\python.exe sari_sari.py`.

## Play

1. Read the customer's Filipino order at the top.
2. Click the matching 3D shelf packages, or use **1–6**. Each click places one
   package on the counter. **Backspace** or **Undo item** removes the last package.
3. Click the countertop, **Checkout**, or press **Enter** to submit the basket.
4. The customer states the total and gives a bill. Calculate payment minus total.
   Click peso denominations to assemble change; **Undo** and **Clear** correct it.
   The P20 coin and P20 bill are separately available and have the same value.
5. Click **Give change** or press **Enter**. For exact payment, submit zero change.
6. Reach the daily sales goal, then choose **Next day**. Goals increase by P100;
   orders grow to three different products from day three onward.

Incorrect items or change cost eight reputation points and allow a retry. Correct
sales restore three. At zero reputation the store closes; **Restart** begins anew.
Press **Esc** to quit. The mouse stays free; the camera is intentionally stationary.

Cash starts at P500 and increases by net sale receipts. Daily goal measures sales,
not profit; stock and change denominations are unlimited for arithmetic practice.
There are no supplier costs, finite cash-drawer counts, timers, or save files.
Prices are fictional. No external art, audio, or brand logos are bundled.

## Check the arithmetic without installing Ursina

```sh
python sari_sari.py --self-test
```

Official engine reference: https://www.ursinaengine.org/api_reference.html
