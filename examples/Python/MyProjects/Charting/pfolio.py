#!/usr/bin/env python
"""
* pfolio.py: download closing prices of stock portfolio and display in a QTableView
* @author (Chocolaf): Manish Bhobé
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import argparse
import pathlib
from pathlib import Path

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import yfinance
import numpy as np
import pandas as pd
import datetime
import locale

import chocolaf


logger = chocolaf.get_logger(pathlib.Path(__file__))

# some pandas tweaks
pd.set_option("display.max_rows", 80)
pd.set_option("display.max_columns", 50)
pd.options.display.float_format = "{:,.2f}".format
pd.options.display.width = 1024

todays_date = datetime.datetime.now()
year, month, day, hour = (
    todays_date.year,
    todays_date.month,
    todays_date.day,
    todays_date.hour,
)
# adjust for financial year - if today() in Jan, Feb or Mar, decrease year by 1
year = year - 1 if month in range(1, 4) else year
# adjust day - if todays_date returns hour in the IST less than 4 PM (trading day ends 3:15 PM)
# then subtract 1 day. We'll use timedelta to auto-set year, month respectively.
# td = None if hour >= 16 else datetime.timedelta(days=-1)
td = None  # data downloads missing 1 day for some reason :(

# NOTE: start date is 01-Apr of current financial year
START_DATE: datetime.datetime = datetime.datetime(year, 4, 1)
END_DATE: datetime.datetime = datetime.datetime.now()
END_DATE = END_DATE if td is None else END_DATE + td

# Start Modification (12-Apr-24):
# I need a lookback of at least LOOKBACK_WINDOW days for plotting, so modify the start date
# if days between start_date & end_date < 90. Push back start_date to before 01-Apr-YYYY
LOOKBACK_WINDOW = 90
FOR_MJB = True

# adjust START_DATE to date LOOKBACK_WINDOW days before END_DATE
START_DATE = (
    END_DATE - datetime.timedelta(days=LOOKBACK_WINDOW)
    if (END_DATE - START_DATE).days < LOOKBACK_WINDOW
    else START_DATE
)

# End Modification (12-Apr-24):

logger.info(
    # if start_date is not 01-Apr-YYYY, then it has been adjusted
    f"START_DATE = {START_DATE.strftime('%d-%b-%Y')} - END_DATE = "
    f"{END_DATE.strftime('%d-%b-%Y')}"
)

# set to India locale for correct number & currency formats, if available (else fallback to default)
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except locale.Error:
    # Fallback for systems that might use a slightly different string format
    try:
        locale.setlocale(locale.LC_ALL, 'en_IN')
    except locale.Error:
        console.print("[red]NOTE: Locale \'en_IN\' not supported on this system. Falling back to default.[/red]")
        locale.setlocale(locale.LC_ALL, '')


def show_candlestick(
    symbol: str,
    days_past: int = LOOKBACK_WINDOW,
    start_date: datetime.datetime = START_DATE,
    end_date: datetime.datetime = END_DATE,
    style="yahoo",
    show_volume=True,
    fig_size=(18, 10),
):
    import mplfinance as mpf

    # Start Modification (12-Apr-24):
    # modification - days_past must be in range (1, LOOKBACK_WINDOW)
    days_past = max(1, days_past)  # make any -ve value == 1
    days_past = min(days_past, LOOKBACK_WINDOW)  # can't be > LOOKBACK_WINDOW!
    # End Modification (12-Apr-24):

    df = yfinance.download(symbol, start=start_date, end=end_date, progress=False)
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")

    # use mplfinance to plot the candlestick
    # mpf.figure(figsize=fig_size)
    # title = f"{symbol} chart from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    title = f"{symbol} chart for last {days_past} days"
    mpf.plot(
        df[-days_past:],
        type="candle",
        style=style,
        volume=show_volume,
        title=title,
        figratio=fig_size,
        # returnfig=True,
    )
    # fig.tight_layout()

    # plt.show()


def show_plot(symbol: str, fig_size=(10, 6)):
    import matplotlib.pyplot as mpl
    import matplotlib.pyplot as plt

    # @see: https://matplotlib.org/stable/gallery/event_handling/coords_demo.html
    from matplotlib.backend_bases import MouseButton

    def on_move(event):
        if event.inaxes:
            # print(f"data coords {event.xdata} {event.ydata}")
            xdata, ydata = event.xdata, event.ydata
            xdata2 = datetime.datetime.strftime(
                datetime.date.fromtimestamp(xdata), "%Y-%m-%d"
            )
            # ydata = f"{ydata:,.3f}"
            ydata = locale.currency(ydata, grouping=True)
            # tooltip.set_text(f"({xdata},{ydata})")
            print(f"({xdata},{xdata2},{ydata})")

    mpl.rcParams["font.family"] = "SF Pro Rounded, Calibri, DejaVu Sans, Sans"
    mpl.rcParams["font.weight"] = 500

    today = QDateTime.currentDateTime().toString("dd-MMM-yyyy")
    save_path = Path(__file__).absolute().parents[0] / "pfolio" / f"pfolio_{today}.csv"
    plot_df = pd.read_csv(save_path, index_col=0)
    plot_df = plot_df.drop(["Qty"], axis=1)

    plt.figure(figsize=fig_size)
    binding_id = plt.connect("motion_notify_event", on_move)
    plot_values = plot_df.loc[symbol, :]
    plot_values.plot()

    plt.title(f"{symbol} - closing price from 01-Apr-{year} - {today}")
    plt.show()


def download_stock_prices(
    holdings: pd.DataFrame,
    start_date: datetime.datetime = START_DATE,
    end_date: datetime.datetime = END_DATE,
    save_path: str = None,
    force_download: bool = False,
) -> pd.DataFrame:
    """
    downloads stock prices read from holdings dataframe from START_DATE to END_DATE
    into a dataframe, which is saved to save_path (if specified)
    @param: holdings (pd.DataFrame): the dataframe with your stock holdings (symbol & qty)
    @param: start_date (datatime.datetime): start date to download stock prices
    @param: end_date (datatime.datetime): end date to download stock prices
    @param: save_path (str; optional - default = None): valid full path where downloaded
        stock prices should be saved (e.g. ~/stock_data/stock_prices.csv)
    @param: force_download (bool, optional - default = False): forces download if True
        (otherwise it assumes that stock prices are to be loaded from save_path)
    @return: (pd.DataFrame) - dataframe of prices for each stock in holdings
        (rows = number of stocks in your holdings dataframe, cols = qty + end_date - start_date
         index = symbol name)
        Example of output dataframe: if today is 2020-10-09
                          |  Qty | start_date | start_date+1 | ... | end_date-1 | end_date
            ASIANPAINT.NS |  25  |  1024.56   | 1025.67      | ... | 1028.32    | 1024.79
            ...
            RELIANCE.NS   |  50  | 2256.78    | 2250.25      | ... | 2260.29    | 2251.12
    """
    if (save_path is not None) and (os.path.exists(save_path)) and (not force_download):
        # if portfolio was saved before, load from save_path (if exists) unless force_download = True
        pfolio_df = pd.read_csv(save_path, index_col=0)
        logger.info(f"Portfolio loaded from {save_path}")
    else:
        # download stock prices
        logger.info("Downloading stock prices...")
        pfolio_df = pd.DataFrame()
        # Start Modification - 19-Apr-2024 --------------------

        # for symbol in holdings["SYMBOL"]:
        #     logger.info(f"Downloading {symbol} data from {start_date} to {end_date}...")
        #     stock_df = yfinance.download(
        #         symbol, start=start_date, end=end_date, progress=False
        #     )
        #     if len(stock_df) != 0:
        #         pfolio_df[symbol] = stock_df["Close"]
        # try downloading all in one shot
        all_symbols = " ".join(symb for symb in list(holdings["SYMBOL"]))
        logger.info(f"Portfolio symbols: {all_symbols}")
        logger.info(
            f"Downloading above symbols data from {start_date} to {end_date}..."
        )
        all_stocks_df = yfinance.download(all_symbols, start=start_date, end=end_date)
        for symbol in holdings["SYMBOL"]:
            if len(all_stocks_df["Close"][symbol]) != 0:
                pfolio_df[symbol] = all_stocks_df["Close"][symbol]
            else:
                logger.warn(f"WARNING: unable to download data for {symbol}")

        # End Modification - 19-Apr-2024 --------------------
        pfolio_df.index = pd.to_datetime(pfolio_df.index)
        pfolio_df.index = pfolio_df.index.date
        # transpose so that stock names form the index
        pfolio_df = pfolio_df.T
        # add qty column
        pfolio_df.insert(0, "Qty", list(holdings["NUM_SHARES"]))
        # save portfolio
        pfolio_df.to_csv(f"{save_path}", header=True, index=True)
        print(f"Portfolio saved to {save_path}")
    return pfolio_df


def calculate_values(df, num_days=5) -> pd.DataFrame:
    """
    calculate value (= qty * price) for each stock for last num_days
    @param: df - the dataframe with downloaded values
    @param: num_days - for how may days before today should values be calculated
        (optional, default = 5 [values will be calculated for last 5 days])
    @returns: dataframe having quantity, price and value for last num_days
        (rows = number of stocks in your portfolio, cols = qty + num_days * 2
         index = symbol name)
        Example of output dataframe: if today is 2020-10-09
                          |  Qty | 2020-10-05 | 2020-10-05_Value | ... | 2020-10-05 | 2020-10-05_Value
            ASIANPAINT.NS |  25  |  1024.56   | 25614            | ... | 1028.32    | 25708
            ...
            RELIANCE.NS   |  50  | 2256.78    | 112839           | ... | 2260.29    | 113014.50

    """
    cols = df.columns

    df_new = df[["Qty"]]

    # calculate value of stocks for each day
    for col in cols[-num_days:]:
        df_new[col] = df[col]
        df_new[f"{col}_Value"] = df[col] * df["Qty"]
    return df_new


def build_output(entry: Path, long: bool = False):
    if long:
        size = entry.stat().st_size
        date = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime(
            "%d-%b-%Y %H:%M:%S"
        )
        type = "d" if entry.is_dir() else "f"
        return f"{type} {size:>10d} {date} {entry.name}"
    return entry.name


class PandasTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super(PandasTableModel, self).__init__()
        self._data: pd.DataFrame = data

    def data(self, index: QModelIndex, role: int):
        numRows = self.rowCount(0)  # any value for index is ok
        prevValue = None

        if index.row() == (numRows - 1):
            value = ""
            # I am on the Totals row, which does not exist in the dataset!
            # if column() is a "_Value" column, then calculate total & display it
            colName = str(self._data.columns[index.column()]).strip()
            if colName.endswith("_Value"):
                value = self._data[colName].sum()
                # logger.info(f"Sum of column {colName} is {value:,.2f}")
                # NOTE: the _Value columns are even columns
                if (index.column() % 2 == 0) and (index.column() != 2):
                    prevColName = str(self._data.columns[index.column() - 2]).strip()
                    prevValue = self._data[prevColName].sum()
                #     prevValue = self._data.iloc[index.row(), index.column() - 2]
        else:
            # get value from dataframe
            value = self._data.iloc[index.row(), index.column()]
            # note: Odd column numbers have stock values
            if (index.column() % 2 != 0) and (index.column() != 1):
                prevValue = self._data.iloc[index.row(), index.column() - 2]

        # value = self._data.iloc[index.row(), index.column()]

        if role == Qt.ItemDataRole.EditRole:
            return value

        if role == Qt.ItemDataRole.DisplayRole:
            # special formatting for floats, ints and dates
            if isinstance(value, str):
                return "%s" % value
            if isinstance(value, datetime.datetime):
                # display dates as YYYY-MM-DD
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float) or (value.dtype == np.float64):
                # format as currency using locale specific format
                return locale.currency(value, grouping=True)
            if isinstance(value, int) or (value.dtype == np.int64):
                # format with locale format
                val = f"{value:,}"
                return val
            # for all other cases, return value as-is
            return value
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # right align ints & floats
            # or isinstance(value, int):
            if isinstance(value, str):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
            elif (
                isinstance(value, float)
                or (value.dtype == np.float64)
                or isinstance(value, int)
                or (value.dtype == np.int64)
            ):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
            else:
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignLeft
        elif role == Qt.ItemDataRole.FontRole:
            # allowa yo to set the font of individual cells
            if index.row() == (numRows - 1):
                # for Totals row, make font bold
                font = QFont()
                font.setBold(True)
                return font
        elif role == Qt.ItemDataRole.ForegroundRole:
            # set foreground color
            if prevValue is not None:
                green = QColor("#089981")
                red = QColor("#F23645")
                brushColor = green if prevValue < value else red
                return QBrush(brushColor)

    def rowCount(self, index):
        # NOTE: we specify 1 more than the number of data rows to accomodate Totals
        return self._data.shape[0] + 1

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "%s" % str(self._data.columns[section]).strip()

            if orientation == Qt.Orientation.Vertical:
                return (
                    "TOTAL VALUE"
                    if (section == self.rowCount(0) - 1)
                    else "%s" % str(self._data.index[section]).strip()
                )


class MyTableView(QTableView):
    def __init__(self):
        super(MyTableView, self).__init__()
        self.doubleClicked.connect(self.on_double_clicked)
        # Enable extended selection to allow dragging across ranges
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def on_double_clicked(self, index):
        model = self.model()
        try:
            symbol = model._data.index[index.row()]
        except IndexError:
            symbol = "Unk"
        logger.info(f"You double clicked in cell {index.row()}-{index.column()} with symbol {symbol}")
        if symbol != "Unk":
            show_candlestick(symbol)

    def keyPressEvent(self, event):
        # Check for Ctrl+C (or Cmd+C on macOS)
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection_to_clipboard()
        else:
            super().keyPressEvent(event)

    def copy_selection_to_clipboard(self):
        """ copies selected values , including column headings to clibpoard as TAB delimited text,
        which can be pasted into Excel """

        # do I have text selected?
        selection = self.selectionModel().selectedIndexes()
        if not selection:
            return

        # 1. Sort indexes by row, then by column to maintain layout
        selection.sort(key=lambda x: (x.row(), x.column()))

        # 2. Get unique columns in the selection to build the header row
        unique_cols = sorted(list(set(index.column() for index in selection)))
        
        headers = []
        for col in unique_cols:
            # Get horizontal header text for the selected columns
            header_text = self.model().headerData(
                col, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            headers.append(str(header_text))

        # 3. Build the final copy string starting with headers
        copy_text = "\t".join(headers) + "\n"
        
        current_row = selection[0].row()
        row_data = []
        
        for index in selection:
            if index.row() != current_row:
                copy_text += "\t".join(row_data) + "\n"
                row_data = []
                current_row = index.row()
            
            # Fetch raw text from the model (i.e. excluding locale-specific formatting)
            #value = self.model().data(index, Qt.ItemDataRole.DisplayRole)
            value = self.model().data(index, Qt.ItemDataRole.EditRole)
            row_data.append(str(value))

        # Add the final data row
        copy_text += "\t".join(row_data)

        # 4. Output to system clipboard
        QApplication.clipboard().setText(copy_text)
        logger.info("Selection with headers copied to clipboard.") 


class MainWindow(QMainWindow):
    """the main window of the application"""

    def __init__(self, dataframe: pd.DataFrame):
        super(MainWindow, self).__init__()
        self.dataframe = dataframe
        # self.tableView = QTableView()
        self.tableView = MyTableView()
        self.tableView.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignHCenter
        )
        self.model = PandasTableModel(self.dataframe)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.setCentralWidget(self.tableView)


DAY_WINDOW = 10

if __name__ == "__main__":
    chocolaf.enable_hi_dpi()
    app = QApplication(sys.argv)
    # app = chocolaf.ChocolafApp(sys.argv)
    # # app.setStyle("Chocolaf")
    # app.setStyle("Fusion")

    parser = argparse.ArgumentParser()
    # on command line pass --zoom 1.2 to increase font size by 20%
    parser.add_argument(
        "--zoom",
        type=float,
        default=1.0,
        help="Zoom level for the font size used in grid (optional, default=1.0, no zoom)",
    )
    # Start Modification (12-Apr-24):
    # on command line pass --lookback 120 to change lookback window
    parser.add_argument(
        "--lookback",
        type=int,
        default=LOOKBACK_WINDOW,
        help=f"Lookback window (# of days) for plotting graphs (optional, default={LOOKBACK_WINDOW})",
    )
    # on command line pass --force_download to force download
    parser.add_argument(
        "--force_download",
        action="store_false",
        # type=bool,
        # default=True,
        help=f"Flag to force download of stock prices (optional, default=True)",
    )
    # End Modification (12-Apr-24):
    parser.add_argument(
        "--for_sjb",
        action="store_false",
        # type=bool,
        # default=True,
        help=f"Flag to check if portfolio is for MJB or SJB (default=True)",
    )
    # Start modification (01-Feb-25):

    # End modification (01-Feb-25):
    args = parser.parse_args()
    font = app.font()
    logger.info(f"Default font: {font.family()}, {font.pointSize()} points")
    font.setPointSize(int(font.pointSize() * args.zoom))
    logger.info(
        f"Zoomed font: {font.family()}, {font.pointSize()} points (zoom = {args.zoom})"
    )
    app.setFont(font)
    # Start Modification (12-Apr-24):
    # lookback window set from command line argument
    LOOKBACK_WINDOW = args.lookback
    FOR_MJB = args.for_sjb
    logger.info(f"Lookback window: {LOOKBACK_WINDOW} days")
    logger.info(f"Force download of stock data? {args.force_download}")
    # End Modification (12-Apr-24):

    today = QDateTime.currentDateTime().toString("dd-MMM-yyyy")

    save_path = Path(__file__).absolute().parents[0] / "pfolio"
    if not save_path.exists():
        save_path.mkdir(exist_ok=True)

    save_path = (
        save_path / f"pfolio_mjb_{today}.csv" if FOR_MJB else f"pfolio_sjb_{today}.csv"
    )

    # open holdings CSV (update this when holdings change)
    holdings_csv_file = "holdings_mjb.csv" if FOR_MJB else "holdings_sjb.csv"
    holdings = pd.read_csv(pathlib.Path(__file__).parent / holdings_csv_file)
    # download holdings, if not done already
    pfolio_df = download_stock_prices(
        holdings,
        start_date=START_DATE,
        end_date=END_DATE,
        save_path=save_path,
        # Start Modification (12-Apr-24): downloads based on command line param
        force_download=args.force_download,
        # End Modification (12-Apr-24): downloads based on command line param
    )
    # logger.info(pfolio_df.iloc[:, -DAY_WINDOW:].head())
    # calculate totals by day, only if required
    df_values = calculate_values(pfolio_df, DAY_WINDOW)
    # logger.info(df_values)
    save_path = (
        Path(__file__).absolute().parents[0]
        / "pfolio"
        / (
            f"pfolio_mjb_{today}_vals.csv"
            if FOR_MJB
            else f"pfolio_sjb_{today}_vals.csv"
        )
    )
    df_values.to_csv(save_path, index=True, header=True)

    title = f"{'Manish' if FOR_MJB else 'Sunila'}'s Portfolio performance for past {DAY_WINDOW} days"
    window = MainWindow(df_values)
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon(str(pathlib.Path(__file__).parent / "stocks.png")))
    chocolaf.centerOnScreenWithSize(window, 0.75, 0.65)
    window.show()

    # show_plot("JIOFIN.NS")

    sys.exit(app.exec())
