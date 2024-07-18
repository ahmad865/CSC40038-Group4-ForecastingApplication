import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from tkinter import *
import tkinter as tk
from tkinter import Label, Button, filedialog, Text
from tkcalendar import DateEntry
import os

# Create the main window for the application
root = Tk()
root.title("Group 4 Forecasting Tool")

# Adjust the size of the main window
height = 600
width = 600
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Function to load data and perform forecasting
def load_data_and_forecast(data, forecast_end, file_name):
    print("Starting data processing and forecasting...")
    
    # Convert 'Created Date' to datetime object and sort the data by this column
    data['Created Date'] = pd.to_datetime(data['Created Date'], dayfirst=True)
    data = data.sort_values('Created Date')

    # Generate a time series based on the count of BookingReference per day
    time_series = data['Created Date'].value_counts().sort_index()

    # Resample the series to fill in missing days with 0 bookings
    time_series = time_series.resample('D').sum()

    # Display first and last few records of the series
    print(f"Time series head:\n{time_series.head()}")
    print(f"Time series tail:\n{time_series.tail()}")

    # Fit the ARIMA model with specified orders
    model = ARIMA(time_series, order=(5, 1, 0))
    model_fit = model.fit()

    # Start forecasting from the earliest date in the data
    forecast_start = time_series.index.min().strftime("%Y-%m-%d")

    # Predict future values up to the specified end date
    forecast = model_fit.predict(start=forecast_start, end=forecast_end, typ='levels')

    # Replace any negative forecast values with zero
    forecast[forecast < 0] = 0

    # Display the initial and final few predictions
    print(f"Forecast head:\n{forecast.head()}")
    print(f"Forecast tail:\n{forecast.tail()}")

    # Calculate total actual and forecasted registrations
    last_date_in_data = time_series.index[-1]
    total_forecasted_registrations = forecast[last_date_in_data:].sum()
    total_Event_registrations = time_series.sum() + total_forecasted_registrations
    print(f"Total Registrations for the Event Forecasted+Acutal: {total_Event_registrations}")
    print(f"Total forecasted registrations from {last_date_in_data.strftime('%Y-%m-%d')} to {forecast_end}: {total_forecasted_registrations}")

    # Plotting the actual data and forecasts
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_series.index,
        y=time_series.values,
        mode='lines+markers',
        name='Actual',
        line=dict(color='blue'),
        marker=dict(size=5)
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index,
        y=forecast.values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red'),
        marker=dict(size=5),
        hovertemplate='%{x}<br>Number of Bookings: %{y:.0f}<extra></extra>'
    ))

    # Add annotations for total registration summary
    fig.add_annotation(
        text=f"Event total Registrations Acutal + Predictions: <b>{total_Event_registrations:.0f}</b>",
        xref="paper",
        yref="paper",
        x=1,
        y=0.95,
        showarrow=False,
        font=dict(size=12, color="black"),
        align="right"
    )
    fig.add_annotation(
        text=f"Total Forecasted Registrations: <b>{total_forecasted_registrations:.0f}</b>",
        xref="paper",
        yref="paper",
        x=1,
        y=0.9,
        showarrow=False,
        font=dict(size=12, color="black"),
        align="right"
    )

    # Update plot layout
    fig.update_layout(
        title=f'Actual and Forecasted Number of Bookings - {file_name}',
        xaxis_title='Date',
        yaxis_title='Number of Bookings',
        hovermode='closest',
        template='plotly_white'
    )

    # Display the plot
    print("Displaying the plot...")
    fig.show()

# Function to upload a data file
def upload_file():
    # Open a file dialog to select a data file
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if file_path:
        print(f"File selected: {file_path}")
        # Load data from the selected file
        if file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)

        forecast_end = cal_end.get_date().strftime("%Y-%m-%d")
        print(f"Forecast end date: {forecast_end}")

        # Extract the filename for labeling purposes
        file_name = os.path.basename(file_path)

        load_data_and_forecast(data, forecast_end, file_name)

        # Close the application once the processing is complete
        root.destroy()
    else:
        print("No file selected.")

# User interface elements
Label(root, text="Select Forecast End Date:").grid(row=0, column=0, padx=20, pady=10)
cal_end = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
cal_end.grid(row=0, column=1, padx=10, pady=10)

Button(root, text="Upload File and Forecast", bg="#127ba7", command=upload_file).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

instruction_text = Text(root, height=10, width=50, wrap=WORD)
instruction_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
instruction_text.insert(END, "Instructions:\n1. Select the Forecast End Date.\n2. Click 'Upload File and Forecast' to upload your data file and generate the forecast.\n3. The supported file formats are .xlsx and .csv.")
instruction_text.config(state=DISABLED)  # Make the text box read-only

# Start the Tkinter event loop
root.mainloop()
