import sys
import locale
from rich.console import Console
from pathlib import Path
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableView,
                             QHeaderView, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDateTime, QTimeZone
from PyQt6.QtGui import QPalette, QFont, QColor, QPainter, QBrush
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis

from download_stocks_data import get_quarterly_performance_report

console = Console()

# path to holdings file
DATA_FILE_PATH = Path(__file__).parent / "holdings_mjb.csv"
if not DATA_FILE_PATH.exists():
    console.print(f"[red]ERROR: Holdings file ({str(DATA_FILE_PATH)}) not found! Please check path.[/red]")
    sys.exit(1)

# Sets locale to your choice to display floats/ints (e.g., 'en_US', 'de_DE', etc.)
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except locale.Error:
    # Fallback for systems that might use a slightly different string format
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN')
    except locale.Error:
        console.print("[red]NOTE: Locale \'en_IN\' not supported on this system. Falling back to default.[/red]")
        locale.setlocale(locale.LC_ALL, '')


# 1. Custom Table Model for Pandas
class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            col_name = self._data.columns[index.column()]
            value = self._data.iloc[index.row(), index.column()]

            # 1. Handle NaN or None (Display as blank)
            if pd.isna(value) or value is None:
                return ""

            # Format numbers in locale aware format
            # return f"{value:.2f}" if isinstance(value, (float, int)) else str(value)
            if isinstance(value, (float, int)):
                # Apply currency symbol (₹) only to 'Value_' columns or the 'Totals' row in specific columns
                if "Value_" in col_name:
                    # symbol=True adds the ₹ symbol
                    # grouping=True handles the Lakhs/Crores separators (12,34,567.00)
                    return locale.currency(value, symbol=True, grouping=True)
                else:
                    # Standard locale formatting for prices/quantities without the ₹ symbol
                    return locale.format_string("%.2f", value, grouping=True)

            return str(value)

        # Handle Bold Font for the "Totals" row
        if role == Qt.ItemDataRole.FontRole:
            # Check if the text in the first column (Symbol) of this row is "Totals"
            if str(self._data.iloc[index.row(), 0]) == "TOTALS":
                font = QFont()
                font.setBold(True)
                return font

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None


# 2. Frozen Column Widget Implementation
class FrozenTable(QTableView):
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.frozenTableView = QTableView(self)
        self._init_frozen_view()

        self.horizontalHeader().sectionResized.connect(self.update_section_width)
        self.verticalHeader().sectionResized.connect(self.update_section_height)
        self.verticalScrollBar().valueChanged.connect(
            self.frozenTableView.verticalScrollBar().setValue
        )
        self.frozenTableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue
        )

    def _init_frozen_view(self):
        self.frozenTableView.setModel(self.model())
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )

        # Freeze the first 4 columns as requested
        for col in range(4, self.model().columnCount()):
            self.frozenTableView.setColumnHidden(col, True)

        # Theme Detection and Styling
        self.apply_theme_styles()

        self.frozenTableView.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport().stackUnder(self.frozenTableView)

        self.update_frozen_geometry()
        self.frozenTableView.show()

    def apply_theme_styles(self):
        """Detects system theme and applies appropriate colors to frozen columns."""
        palette = QApplication.palette()
        is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128

        if is_dark:
            # Dark Theme: Dark grey background, white text
            bg_color = "#2d2d2d"
            text_color = "#ffffff"
            border_color = "#555555"
        else:
            # Light Theme: Light grey background, black text
            bg_color = "#f0f0f0"
            text_color = "#000000"
            border_color = "#cccccc"

        style = f"""
            QTableView {{
                border: none;
                background-color: {bg_color};
                color: {text_color};
                gridline-color: {border_color};
            }}
        """
        self.frozenTableView.setStyleSheet(style)

    def update_section_width(self, logicalIndex, oldSize, newSize):
        if logicalIndex < 4:
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.update_frozen_geometry()

    def update_section_height(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_frozen_geometry()

    def update_frozen_geometry(self):
        # Calculate width of the first FOUR columns
        width = sum(self.columnWidth(i) for i in range(4))

        self.frozenTableView.setGeometry(
            self.verticalHeader().width() + self.frameWidth(),
            self.frameWidth(),
            width,
            self.viewport().height() + self.horizontalHeader().height()
        )


class PerformanceChart(QMainWindow):
    def __init__(self, symbol, dates, values, bg_color, grid_color):
        super().__init__()
        self.setWindowTitle(f"Performance: {symbol}")
        self.resize(900, 500)

        # 1. Create Series
        series = QLineSeries()
        pen = series.pen()
        pen.setWidth(3)
        pen.setColor(QColor("#00FF00"))  # Bright Green
        series.setPen(pen)
        text_brush = QBrush(QColor(grid_color))

        for d, v in zip(dates, values):
            dt = QDateTime.fromString(d, "dd-MMM-yy")
            series.append(float(dt.toMSecsSinceEpoch()), v)

        # 2. Create Chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"Performance of {symbol} stock")
        chart.legend().hide()

        # Styling
        chart.setBackgroundBrush(QColor(bg_color))
        chart.setTitleBrush(QColor("#FFFFFF" if bg_color == "#2d2d2d" else "#000000"))

        # 3. Axes
        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd-MMM-yy")
        axis_x.setTitleText("Date")
        axis_x.setGridLineColor(QColor(grid_color))
        axis_x.setLabelsBrush(text_brush)
        axis_x.setTitleBrush(text_brush)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Value")
        axis_y.setGridLineColor(QColor(grid_color))
        axis_y.setLabelsBrush(text_brush)
        axis_y.setTitleBrush(text_brush)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        # 4. View & Scrolling
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.setCentralWidget(chart_view)

        # Zoom in slightly to enable horizontal scrolling
        chart.zoom(1.5)
        # Scroll to extreme right (most recent data)
        chart.scroll(chart.plotArea().width(), 0)


# 4. Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Quarterly Performance")
        self.resize(1000, 600)

        # Fetch Data using your module
        df = get_quarterly_performance_report(str(DATA_FILE_PATH))
        # Reset index so 'symbol' becomes a column (Column 0)
        df = df.reset_index()
        df.rename(columns={'index': 'Symbol'}, inplace=True)

        # Create UI
        self.model = PandasModel(df)
        self.table = FrozenTable(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # when I double click on any line (other than Total or header)
        # display line chart
        self.table.doubleClicked.connect(self.show_chart)

    def show_chart(self, index):
        row = index.row()
        # Get the Symbol from column 0
        symbol = self.model._data.iloc[row, 0]

        # 1. Ignore Header and Totals row
        if symbol == "Totals":
            return

        # 2. Extract Data
        df_row = self.model._data.iloc[row]
        dates = []
        values = []

        # look for Closing price entries
        closing_price_col = "Close_"

        for col in self.model._data.columns:
            if col.startswith(closing_price_col):
                # Extract date from "Close_dd-Mmm-yy"
                date_str = col.replace(closing_price_col, "")
                val = df_row[col]
                if pd.notna(val):
                    dates.append(date_str)
                    values.append(val)

        # 3. Get colors from the table's current theme
        palette = QApplication.palette()
        is_dark = palette.color(QPalette.ColorRole.Window).lightness() < 128
        bg = "#2d2d2d" if is_dark else "#f0f0f0"
        grid = "#555555" if is_dark else "#cccccc"

        # 4. Launch Chart
        self.chart_window = PerformanceChart(symbol, dates, values, bg, grid)
        self.chart_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
