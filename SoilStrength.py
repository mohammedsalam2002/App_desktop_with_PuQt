import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QTextEdit, QGroupBox, QTabWidget, QHBoxLayout, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon

class CalculationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create main layout
        main_layout = QVBoxLayout()

        # Create tab widget
        tabs = QTabWidget()
        tabs.addTab(self.createSoilTab(), 'فحوصات التربة')
        tabs.addTab(self.createSubbaseTab(), 'فحوصات السبيس')

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
        self.setWindowTitle('SoilStrength Analyzer')
        self.setGeometry(300, 100, 600, 400)
        # Set window icon
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #6495ED;
                border-radius: 5px;
                margin-top: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit, QTextEdit {
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                font-size: 18px;
                padding: 8px 16px;
                border: 2px solid #32CD32;
                border-radius: 5px;
                background-color: #0F6343;
                color: #1fff;
            }
            QPushButton:hover {
                background-color:#7CFC00;
            }
        """)
        self.show()

    def createSoilTab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Create input group
        input_group = QGroupBox('إدخال البيانات')
        input_layout = QGridLayout()

        # Input fields for soil tests
        self.weight_input = QLineEdit(self)
        self.moisture_container_weight_input = QLineEdit(self)
        self.moisture_before_weight_input = QLineEdit(self)
        self.moisture_after_weight_input = QLineEdit(self)

        input_layout.addWidget(QLabel('وزن التربة'), 0, 0)
        input_layout.addWidget(self.weight_input, 0, 1)

        input_layout.addWidget(QLabel('w1'), 1, 0)
        input_layout.addWidget(self.moisture_container_weight_input, 1, 1)

        input_layout.addWidget(QLabel('w2'), 2, 0)
        input_layout.addWidget(self.moisture_before_weight_input, 2, 1)

        input_layout.addWidget(QLabel('w3'), 3, 0)
        input_layout.addWidget(self.moisture_after_weight_input, 3, 1)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Calculate button
        self.calculate_soil_btn = QPushButton('احسب', self)
        self.calculate_soil_btn.setFont(QFont('Arial', 14))
        self.calculate_soil_btn.clicked.connect(self.calculate_soil)
        button_layout.addWidget(self.calculate_soil_btn)

        # Save report button
        self.save_soil_report_btn = QPushButton('حفظ التقرير', self)
        self.save_soil_report_btn.setFont(QFont('Arial', 14))
        self.save_soil_report_btn.clicked.connect(self.save_soil_report)
        button_layout.addWidget(self.save_soil_report_btn)

        # Clear button
        self.clear_soil_btn = QPushButton('تنظيف', self)
        self.clear_soil_btn.setFont(QFont('Arial', 14))
        self.clear_soil_btn.clicked.connect(self.clear_soil)
        button_layout.addWidget(self.clear_soil_btn)

        layout.addLayout(button_layout)

        # Report output
        self.soil_report_output = QTextEdit(self)
        self.soil_report_output.setReadOnly(True)
        layout.addWidget(self.soil_report_output)

        widget.setLayout(layout)
        return widget

    def createSubbaseTab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Create input group
        input_group = QGroupBox('إدخال البيانات')
        input_layout = QGridLayout()

        # Input fields for subbase tests
        self.sand_container_weight_input = QLineEdit(self)
        self.sand_remaining_weight_input = QLineEdit(self)
        self.sand_cone_weight_input = QLineEdit(self)
        self.sand_density_input = QLineEdit(self)

        input_layout.addWidget(QLabel('وزن الرمل داخل الوعاء (غم):'), 0, 0)
        input_layout.addWidget(self.sand_container_weight_input, 0, 1)

        input_layout.addWidget(QLabel('وزن الرمل المتبقي داخل الوعاء (غم):'), 1, 0)
        input_layout.addWidget(self.sand_remaining_weight_input, 1, 1)

        input_layout.addWidget(QLabel('وزن الرمل في المخروط (غم):'), 2, 0)
        input_layout.addWidget(self.sand_cone_weight_input, 2, 1)

        input_layout.addWidget(QLabel('كثافة الرمل (غم/سم³):'), 3, 0)
        input_layout.addWidget(self.sand_density_input, 3, 1)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Calculate button
        self.calculate_subbase_btn = QPushButton('احسب', self)
        self.calculate_subbase_btn.setFont(QFont('Arial', 14))
        self.calculate_subbase_btn.clicked.connect(self.calculate_subbase)
        button_layout.addWidget(self.calculate_subbase_btn)

        # Save report button
        self.save_subbase_report_btn = QPushButton('حفظ التقرير', self)
        self.save_subbase_report_btn.setFont(QFont('Arial', 14))
        self.save_subbase_report_btn.clicked.connect(self.save_subbase_report)
        button_layout.addWidget(self.save_subbase_report_btn)

        # Clear button
        self.clear_subbase_btn = QPushButton('تنظيف', self)
        self.clear_subbase_btn.setFont(QFont('Arial', 14))
        self.clear_subbase_btn.clicked.connect(self.clear_subbase)
        button_layout.addWidget(self.clear_subbase_btn)

        layout.addLayout(button_layout)

        # Report output
        self.subbase_report_output = QTextEdit(self)
        self.subbase_report_output.setReadOnly(True)
        layout.addWidget(self.subbase_report_output)

        widget.setLayout(layout)
        return widget

    def calculate_soil(self):
        try:
            # Get input values
            volume = 981.25  # ثابت
            weight = float(self.weight_input.text())

            container_weight = float(self.moisture_container_weight_input.text())
            before_weight = float(self.moisture_before_weight_input.text())
            after_weight = float(self.moisture_after_weight_input.text())

            # Perform calculations
            field_density = weight / volume
            wet_weight = before_weight - after_weight
            dry_weight = after_weight - container_weight
            moisture_content = (wet_weight / dry_weight) 
            dry_density = field_density / (1 + (moisture_content))
            max_density = 1.806  # Given in the document
            compaction_ratio = (dry_density / max_density) * 100

            # Generate report
            report = f'rb  : {field_density:.3f} غم/سم³\n'
            report += f'Ww : {wet_weight:.3f} غم\n'
            report += f'Wd : {dry_weight:.3f} غم\n'
            report += f'w% : {moisture_content:.3f}%\n'
            report += f'rd : {dry_density:.3f} غم/سم³\n'
            report += f'cd : {compaction_ratio:.3f}%\n'
            if compaction_ratio >= 95:
                report += 'نسبة الحدل تلبي المتطلبات.\n'
            else:
                report += 'نسبة الحدل لا تلبي المتطلبات.\n'

            self.soil_report_output.setText(report)
            self.soil_report_output.setStyleSheet("color: blue;")
        except ValueError:
            self.soil_report_output.setText('خطأ في الإدخال، يرجى التأكد من القيم المدخلة.')
        except Exception as e:
            self.soil_report_output.setText(f"An unexpected error occurred: {e}")

    def save_soil_report(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.soil_report_output.toPlainText())
        except Exception as e:
            self.soil_report_output.setText(f"An error occurred while saving the file: {e}")

    def clear_soil(self):
        self.weight_input.clear()
        self.moisture_container_weight_input.clear()
        self.moisture_before_weight_input.clear()
        self.moisture_after_weight_input.clear()
        self.soil_report_output.clear()

    def calculate_subbase(self):
        try:
            # Get input values
            sand_container_weight = float(self.sand_container_weight_input.text())
            sand_remaining_weight = float(self.sand_remaining_weight_input.text())
            sand_cone_weight = float(self.sand_cone_weight_input.text())
            sand_density = float(self.sand_density_input.text())

            # Perform calculations
            sand_weight = sand_container_weight - sand_remaining_weight - sand_cone_weight
            hole_volume = sand_weight / sand_density
            total_density = sand_weight / hole_volume
            max_sand_density = 2.198  # Given in the document
            compaction_ratio_sand = (total_density / max_sand_density) * 100

            # Generate report
            report = f'وزن الرمل في الحفرة: {sand_weight:.2f} غم\n'
            report += f'حجم الحفرة: {hole_volume:.2f} سم³\n'
            report += f'الكثافة الكلية: {total_density:.2f} غم/سم³\n'
            report += f'نسبة الحدل للسبيس: {compaction_ratio_sand:.2f}%\n'
            if compaction_ratio_sand >= 95:
                report += 'نسبة الحدل للسبيس تلبي المتطلبات.\n'
            else:
                report += 'نسبة الحدل للسبيس لا تلبي المتطلبات.\n'

            self.subbase_report_output.setText(report)
        except ValueError:
            self.subbase_report_output.setText('خطأ في الإدخال، يرجى التأكد من القيم المدخلة.')
        except Exception as e:
            self.subbase_report_output.setText(f"An unexpected error occurred: {e}")

    def save_subbase_report(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.subbase_report_output.toPlainText())
        except Exception as e:
            self.subbase_report_output.setText(f"An error occurred while saving the file: {e}")

    def clear_subbase(self):
        self.sand_container_weight_input.clear()
        self.sand_remaining_weight_input.clear()
        self.sand_cone_weight_input.clear()
        self.sand_density_input.clear()
        self.subbase_report_output.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculationApp()
    sys.exit(app.exec_())
