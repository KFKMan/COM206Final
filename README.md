# ProCalc — Modern & Sleek Calculator
**Final Project Submission by Kaan Faruk Kınalı for COM206**

A simple, beautiful, and highly responsive 4-operation desktop calculator built using **Python** and **PySide6 (Qt6)**. 

This application provides essential arithmetic operations—addition, subtraction, multiplication, division, sign toggling, and floating-point math—wrapped in a gorgeous iOS/macOS-inspired dark mode UI. The interface is styled with customized Qt Style Sheets (QSS) featuring smooth hover and pressed animations. It also supports physical keyboard inputs for an ergonomic workspace.

---

## Key Features

*   **Modern Aesthetic:** Styled with dark, curated color palettes, elegant border radii, and fluid visual states for buttons.
*   **Physical Keyboard Support:** Standard operations (`+`, `-`, `*`, `/`), digits (`0`-`9`), decimal (`.`), calculation execution (`Enter` / `=`), backspace (`Backspace` / `C`), and complete reset (`Escape` / `AC`) map directly to keyboard keys.
*   **Advanced Formula Display:** Dual-screen design that keeps track of the entire current expression (`12.5 + 5 =`) in a secondary label while displaying the current operand or result in high font weight on the main display.
*   **Intelligent Operator Handling:** Consecutively clicking operators replaces the last operator seamlessly instead of breaking the expression flow.
*   **Crash-Proof Design:** Robust handling of division-by-zero or malformed expressions—showing helpful inline error messages (`Cannot Divide by Zero`, `Error`) instead of crashing the program.
*   **Fully Localized to English:** All codes, comments, user interface elements, error messages, and variables are completely in English.

---

## Installation & How to Run

### 1. Setting Up a Virtual Environment (venv)
To isolate project dependencies and keep your global Python environment clean, set up a virtual environment:

**Windows (PowerShell):**
```powershell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Installing Dependencies
With your virtual environment active, install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Running the App
Launch the desktop calculator application:
```bash
python main.py
```

---

## Running with Docker
You can run the application inside an isolated Docker container with graphical display forwarding.

### 1. Build the Docker Image
```bash
docker build -t calculator-app .
```

### 2. Run the Container (with GUI Mount)

**Linux:**
First, allow local container connections to your X server:
```bash
xhost +local:docker
```
Then run the container:
```bash
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix calculator-app
```

**macOS (XQuartz installed and running):**
First, authorize Docker to access XQuartz (ensure "Allow connections from network clients" is checked in your XQuartz security preferences):
```bash
xhost +host.docker.internal
```
Then run the container:
```bash
docker run -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix calculator-app
```

**Windows (Two Options):**

*   **Option A: Using modern WSL2 with native GUI (WSLg) support** (Recommended):
    ```powershell
    docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix calculator-app
    ```
*   **Option B: Using a third-party X Server (like VcXsrv or Xming)** running on the Windows host:
    ```powershell
    docker run -e DISPLAY=host.docker.internal:0.0 calculator-app
    ```

---

## Understanding X11 Forwarding (`/tmp/.X11-unix`)
In the Docker command above, you might notice the flags `-e DISPLAY=$DISPLAY` and `-v /tmp/.X11-unix:/tmp/.X11-unix`. 

### What does this do?
*   **The Problem:** By default, Docker containers are isolated sandboxes and do not have access to a graphical window server or screen. If you try to run a GUI application (like a Qt/PySide6 desktop app) inside a standard container, it will crash because there is no display server to draw and render the window.
*   **The Solution (X11 Socket Sharing):** 
    - `/tmp/.X11-unix` is a special system directory on Linux and macOS that hosts the **Unix Domain Sockets** used by the **X11 Display Server** (Xorg/XQuartz) to communicate with graphical applications.
    - By mounting this socket directory into the container using `-v /tmp/.X11-unix:/tmp/.X11-unix`, we allow the containerized application to talk directly to your host machine's display server.
    - Combined with `-e DISPLAY=$DISPLAY`, which tells the application *which* specific screen/display socket to draw on, the containerized Python process can paint the window directly onto your physical monitor just like a native app.

---

## Project Structure

*   `main.py` — The core application containing UI widgets, event handling, math logic, and QSS style configurations.
*   `requirements.txt` — Project dependencies (`PySide6`).
*   `Dockerfile` — Instructions to build the Docker image with necessary OS libraries for Qt rendering.
*   `README.md` — This documentation and setup guide.
