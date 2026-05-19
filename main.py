import sys
import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QSizePolicy
)

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ProCalc - Modern Calculator")
        self.setMinimumSize(360, 520)
        self.resize(380, 560)
        
        # State variables
        self.expression = ""       # Stores the full expression to be calculated (e.g. "12 + 5")
        self.current_value = "0"   # Stores the current input value
        self.is_result_shown = False # Track if the current display is a calculated result
        
        # Initialize UI
        self.init_ui()
        self.apply_styles()
        
    def init_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # --- DISPLAY AREA ---
        display_container = QWidget()
        display_container.setObjectName("displayContainer")
        display_layout = QVBoxLayout(display_container)
        display_layout.setContentsMargins(12, 12, 12, 12)
        display_layout.setSpacing(4)
        
        # Secondary display for the current full equation (e.g. "25 + 12 =")
        self.equation_label = QLabel("")
        self.equation_label.setObjectName("equationLabel")
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # Main display for current input/result
        self.display = QLineEdit("0")
        self.display.setObjectName("display")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        display_layout.addWidget(self.equation_label)
        display_layout.addWidget(self.display)
        main_layout.addWidget(display_container)
        
        # --- BUTTONS GRID ---
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(10)
        
        # Button labels and their coordinates in the grid (row, col, rowspan, colspan, style_class)
        buttons = {
            # Row 0
            "AC": (0, 0, 1, 1, "special"),
            "C": (0, 1, 1, 1, "special"),
            "±": (0, 2, 1, 1, "special"),
            "÷": (0, 3, 1, 1, "operator"),
            
            # Row 1
            "7": (1, 0, 1, 1, "number"),
            "8": (1, 1, 1, 1, "number"),
            "9": (1, 2, 1, 1, "number"),
            "×": (1, 3, 1, 1, "operator"),
            
            # Row 2
            "4": (2, 0, 1, 1, "number"),
            "5": (2, 1, 1, 1, "number"),
            "6": (2, 2, 1, 1, "number"),
            "−": (2, 3, 1, 1, "operator"),
            
            # Row 3
            "1": (3, 0, 1, 1, "number"),
            "2": (3, 1, 1, 1, "number"),
            "3": (3, 2, 1, 1, "number"),
            "+": (3, 3, 1, 1, "operator"),
            
            # Row 4
            "0": (4, 0, 1, 2, "number"),  # Spans 2 columns
            ".": (4, 2, 1, 1, "number"),
            "=": (4, 3, 1, 1, "equals")
        }
        
        for text, params in buttons.items():
            row, col, rowspan, colspan, btn_type = params
            btn = QPushButton(text)
            btn.setObjectName(f"btn_{text}")
            btn.setProperty("class", btn_type)
            
            # Set size policies to allow clean expanding while keeping them proportional
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            btn.setMinimumSize(50, 50)
            
            # Connect buttons to handlers
            btn.clicked.connect(self.on_button_clicked)
            
            grid_layout.addWidget(btn, row, col, rowspan, colspan)
            
        main_layout.addWidget(grid_widget, stretch=1)
        
    def apply_styles(self):
        """Applies a professional, stunning dark theme using QSS."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0E0F12;
            }
            
            #displayContainer {
                background-color: #1A1C23;
                border-radius: 16px;
                border: 1px solid #282C37;
            }
            
            #equationLabel {
                color: #7A8099;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                font-size: 14px;
                font-weight: 500;
                background-color: transparent;
                border: none;
                padding-right: 4px;
            }
            
            #display {
                color: #FFFFFF;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                font-size: 38px;
                font-weight: 600;
                background-color: transparent;
                border: none;
                padding-right: 4px;
            }
            
            QPushButton {
                font-family: 'Segoe UI', -apple-system, sans-serif;
                font-size: 20px;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                color: #FFFFFF;
            }
            
            /* Styles for numbers: Sleek dark grey buttons */
            QPushButton[class="number"] {
                background-color: #21242E;
                color: #F3F4F6;
            }
            QPushButton[class="number"]:hover {
                background-color: #2D313E;
            }
            QPushButton[class="number"]:pressed {
                background-color: #16181F;
            }
            
            /* Styles for base operators: Distinct high-contrast accent orange */
            QPushButton[class="operator"] {
                background-color: #F59E0B;
                color: #FFFFFF;
            }
            QPushButton[class="operator"]:hover {
                background-color: #FBBF24;
            }
            QPushButton[class="operator"]:pressed {
                background-color: #D97706;
            }
            
            /* Styles for secondary operations (AC, C, ±): Muted blue-grey */
            QPushButton[class="special"] {
                background-color: #374151;
                color: #E5E7EB;
            }
            QPushButton[class="special"]:hover {
                background-color: #4B5563;
            }
            QPushButton[class="special"]:pressed {
                background-color: #1F2937;
            }
            
            /* Styles for '=' button: Vibrant green */
            QPushButton[class="equals"] {
                background-color: #10B981;
                color: #FFFFFF;
            }
            QPushButton[class="equals"]:hover {
                background-color: #34D399;
            }
            QPushButton[class="equals"]:pressed {
                background-color: #059669;
            }
        """)

    def on_button_clicked(self):
        button = self.sender()
        if not button:
            return
        
        text = button.text()
        self.process_input(text)
        
    def process_input(self, char):
        # Reset display if there was a previous error
        if self.display.text() in ["Error", "Cannot Divide by Zero"]:
            self.clear_all()
            
        if char == "AC":
            self.clear_all()
            
        elif char == "C":
            self.backspace()
            
        elif char == "±":
            self.toggle_sign()
            
        elif char in ["+", "−", "×", "÷"]:
            # Standardize operators for display vs calculation
            op_map = {"−": "-", "×": "*", "÷": "/"}
            calc_op = op_map.get(char, char)
            self.handle_operator(calc_op, char)
            
        elif char == "=":
            self.calculate_result()
            
        elif char == ".":
            self.append_decimal()
            
        else: # Number digit
            self.append_digit(char)

    def append_digit(self, digit):
        if self.is_result_shown:
            self.current_value = digit
            self.is_result_shown = False
        elif self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit
            
        self.update_display()

    def append_decimal(self):
        if self.is_result_shown:
            self.current_value = "0."
            self.is_result_shown = False
        elif "." not in self.current_value:
            self.current_value += "."
            
        self.update_display()

    def toggle_sign(self):
        if self.current_value != "0":
            if self.current_value.startswith("-"):
                self.current_value = self.current_value[1:]
            else:
                self.current_value = "-" + self.current_value
            self.update_display()

    def handle_operator(self, calc_op, disp_op):
        # If we have an active input, push it to the expression
        if self.current_value != "":
            self.expression += f" {self.current_value} {calc_op}"
            self.current_value = ""
        # If expression is empty but we have a result, reuse the result
        elif self.expression == "" and self.display.text() not in ["0", "Error", "Cannot Divide by Zero"]:
            self.expression = f" {self.display.text()} {calc_op}"
        # If user clicks another operator consecutively, replace the last one
        elif self.expression != "":
            # Replace the last character (operator) in the expression
            self.expression = self.expression.strip()
            # Remove the last operator
            self.expression = re.sub(r'[\+\-\*/]$', calc_op, self.expression)
            self.expression = f" {self.expression} "
            
        self.is_result_shown = False
        self.update_equation_label(disp_op)

    def calculate_result(self):
        if self.current_value == "" and self.expression == "":
            return
            
        # Append the final input if any
        full_expr = self.expression
        if self.current_value != "":
            full_expr += f" {self.current_value}"
        else:
            # If expression ends with an operator, just evaluate what we have
            full_expr = full_expr.strip()
            full_expr = re.sub(r'[\+\-\*/]$', '', full_expr)
            
        if not full_expr.strip():
            return
            
        # Clean up consecutive operators/spaces
        full_expr = " ".join(full_expr.split())
        
        # Prepare friendly display format for the equation label
        friendly_expr = full_expr.replace("*", " × ").replace("/", " ÷ ").replace("-", " − ").replace("+", " + ")
        
        try:
            # Strict validation to only allow numbers and simple operations
            if not re.match(r'^[0-9\.\+\-\*/\s\(\)]+$', full_expr):
                raise ValueError("Invalid Expression")
                
            # Perform evaluation
            result = eval(full_expr, {"__builtins__": None}, {})
            
            # Format the output beautifully
            if isinstance(result, float):
                # Remove trailing zeros for clean decimals
                if result.is_integer():
                    display_text = str(int(result))
                else:
                    # Round to max 10 decimal places to prevent overflow
                    display_text = f"{result:.10f}".rstrip('0').rstrip('.')
            else:
                display_text = str(result)
                
            self.display.setText(display_text)
            self.equation_label.setText(friendly_expr + " =")
            
            # Reset states with the new result
            self.current_value = display_text
            self.expression = ""
            self.is_result_shown = True
            
        except ZeroDivisionError:
            self.display.setText("Cannot Divide by Zero")
            self.equation_label.setText("")
            self.current_value = ""
            self.expression = ""
        except Exception:
            self.display.setText("Error")
            self.equation_label.setText("")
            self.current_value = ""
            self.expression = ""

    def backspace(self):
        if self.is_result_shown:
            self.clear_all()
            return
            
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
            if self.current_value == "-":
                self.current_value = "0"
        else:
            self.current_value = "0"
            
        self.update_display()

    def clear_all(self):
        self.expression = ""
        self.current_value = "0"
        self.is_result_shown = False
        self.display.setText("0")
        self.equation_label.setText("")

    def update_display(self):
        self.display.setText(self.current_value)

    def update_equation_label(self, operator):
        # Format stored expression for nice display
        formatted = self.expression.replace("*", " × ").replace("/", " ÷ ").replace("-", " − ").replace("+", " + ")
        self.equation_label.setText(formatted)
        
    # --- KEYBOARD EVENT HANDLING ---
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        
        # Mapping physical keys to button presses
        if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Equal]:
            self.process_input("=")
        elif key == Qt.Key.Key_Backspace:
            self.process_input("C")
        elif key == Qt.Key.Key_Escape:
            self.process_input("AC")
        elif text == "+":
            self.process_input("+")
        elif text == "-":
            self.process_input("−")
        elif text == "*":
            self.process_input("×")
        elif text == "/":
            self.process_input("÷")
        elif text in [".", ","]:
            self.process_input(".")
        elif text.isdigit():
            self.process_input(text)
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec())
