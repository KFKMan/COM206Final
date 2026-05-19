# Use a lightweight Python base image
FROM python:3.10-slim

# Install necessary system libraries for Qt6 / PySide6 GUI rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libegl1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libfontconfig1 \
    libxrender1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application code
COPY main.py .

# Set default display environment variable (can be overridden at runtime)
ENV DISPLAY=:0

# Command to execute the app
CMD ["python", "main.py"]
