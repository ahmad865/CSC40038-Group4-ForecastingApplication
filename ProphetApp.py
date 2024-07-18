import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import pandas as pd
from prophet import Prophet
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def predict_registrations():
    # Get the event start date from the UI
    event_start_date_str = date_entry.get()
    event_start_date = datetime.strptime(event_start_date_str, '%d/%m/%Y')
    
    # Get the file path for the new event CSV
    file_path = file_entry.get()
    
    # Load and process partial data for the new event
    partial_data = pd.read_csv(file_path)
    partial_data['Created Date'] = pd.to_datetime(partial_data['Created Date'], format='%d/%m/%Y')
    partial_aggregated = partial_data.groupby('Created Date').size().reset_index(name='registrations')
    
    # Combine historical and partial data
    combined_data = pd.concat([historical_aggregated, partial_aggregated])
    
    # Calculate the number of days to predict
    last_partial_date = partial_aggregated['Created Date'].max()
    days_to_event_start = (event_start_date - last_partial_date).days
    
    # Prepare data for Prophet
    df = combined_data.rename(columns={'Created Date': 'ds', 'registrations': 'y'})
    
    # Train the model
    model = Prophet()
    
    model.fit(df)
    
    # Make future dataframe
    future_dates = model.make_future_dataframe(periods=days_to_event_start, freq='D')
    
    # Forecast
    forecast = model.predict(future_dates)
    
    # Ignore negative values in forecast
    forecast['yhat'] = forecast['yhat'].apply(lambda x: max(0, x))
    
    # Display the forecasted registrations
    total_predicted_registrations = forecast['yhat'].tail(days_to_event_start).sum()
    result_label.config(text=f'Total predicted registrations: {int(total_predicted_registrations)}')
    
    # Display the disclaimer
    disclaimer_label.pack(pady=5)
    
    # Plot the forecast with historical data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['ds'], df['y'], 'b.', label='Historical Data')
    ax.plot(forecast['ds'], forecast['yhat'], 'r.', label='Forecast')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2)
    ax.axvline(x=last_partial_date, color='gray', linestyle='--', label='Last Partial Date')
    ax.axvline(x=event_start_date, color='blue', linestyle='--', label='Event Start Date')
    ax.legend()
    ax.set_xlabel('Date')
    ax.set_ylabel('Registrations')
    ax.set_title('Registration Forecast Using Prophet')
    
    # Clear the previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()
    
    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    toolbar = NavigationToolbar2Tk(canvas, plot_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()
    canvas.draw()

# Load and combine historical data
historical_files = ['D19.csv', 'D21.csv', 'GP21.csv', 'NP21.csv', 'MSE21.csv', 'SRM22.csv', 'SRM23.csv']
historical_data = pd.concat([pd.read_csv(file) for file in historical_files])
historical_data['Created Date'] = pd.to_datetime(historical_data['Created Date'], format='%d/%m/%Y')
historical_aggregated = historical_data.groupby('Created Date').size().reset_index(name='registrations')

# Create the main window
window = tk.Tk()
window.title("Event Registrations Predictions")

# Header
header_label = ttk.Label(window, text="Event Registrations Predictions", font=("Helvetica", 16, "bold"))
header_label.pack(pady=10)

# Event start date
date_label = ttk.Label(window, text="Select Event Start Date:")
date_label.pack(pady=5)
date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
date_entry.pack(pady=5)

# CSV file for new event
file_label = ttk.Label(window, text="Select CSV file for New Event:")
file_label.pack(pady=5)
file_entry = ttk.Entry(window, width=50)
file_entry.pack(pady=5)
file_button = ttk.Button(window, text="Browse", command=lambda: file_entry.insert(0, filedialog.askopenfilename()))
file_button.pack(pady=5)

# Predict button
predict_button = ttk.Button(window, text="Predict", command=predict_registrations)
predict_button.pack(pady=10)

# Result label
result_label = ttk.Label(window, text="", font=("Helvetica", 14, "bold"))
result_label.pack(pady=10)

# Plot frame
plot_frame = ttk.Frame(window)
plot_frame.pack(pady=10)

# Disclaimer label (hidden initially)
disclaimer_label = ttk.Label(window, text="This is Just an estimate. Actual Number can be +/- 20% of this Number")

# Ensure the program exits when the window is closed
window.protocol("WM_DELETE_WINDOW", window.quit)

# Run the application
window.mainloop()
