
# Group 4 Forecasting Tool

This forecasting tool is designed to assist in analyzing and predicting event registrations using time series data. Built with Python and utilizing a tkinter graphical interface, this tool provides an easy-to-use platform for uploading data, performing ARIMA-based forecasts, and visualizing results interactively.

## Features

- **Data Upload:** Supports `.csv` and `.xlsx` file formats for data input.
- **Data Processing:** Automatically parses and prepares data for time series analysis.
- **Forecasting:** Implements an ARIMA model to forecast future event registrations.
- **Visualization:** Displays both actual data and forecasts in an interactive Plotly graph.
- **User Interface:** Provides a simple and clear GUI for easy operation.

## Installation

To set up the forecasting tool on your local machine, follow these steps:

### Prerequisites

Ensure you have Python installed on your system. Python 3.6 or later is recommended. You can download it from [python.org](https://www.python.org/downloads/).

### Required Python Libraries

Install the following Python libraries using pip:

```bash
pip install pandas plotly statsmodels tkcalendar
```

### Download

Clone the repository or download the source code:

```bash
git clone https://github.com/your-repository/group4-forecasting-tool.git
cd group4-forecasting-tool
```

## Usage

To start the application, run the Python script from your command line:

```bash
python forecasting_tool.py
```

Follow the GUI instructions for operation:
1. **Select the Forecast End Date:** Use the date picker to choose the end date for the forecast.
2. **Upload File and Forecast:** Click this button to upload your data file and start the forecasting process.
3. **View Results:** The forecast and actual data will be displayed on an interactive graph.

## File Formats

The tool accepts data in the following formats:
- **Excel files:** `.xlsx`
- **CSV files:** `.csv`

Ensure that your data files have at least the following columns:
- `Created Date`: The date of event registration.
- `BookingReference`: A unique identifier for each registration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your features or corrections.

## Support

For support, please open an issue on the project's GitHub issue tracker.

## Authors

- **Your Name** - _Initial work_ - [YourGithubProfile](https://github.com/YourUsername)

