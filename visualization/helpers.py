import json
import pandas as pd
import streamlit as st
import requests
import json
import time
import pandas as pd
import plotly.graph_objs as go


def to_df(json_text):

    data = json.loads(json_text)
    # print(data)

    # Extract the list of rows from the response
    rows = data['data']

    # Convert the rows to a DataFrame
    df = pd.DataFrame([rows])

    return df


# helpers.py
import matplotlib.pyplot as plt

class LiveGraph:
    def __init__(self, xlabel='Time', ylabel='Value', title='Live Graph'):
        # Enable interactive mode
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        
        # Initialize empty lists for two sets of data
        self.x_data1, self.y_data1 = [], []
        self.x_data2, self.y_data2 = [], []
        
        # Create two line objects
        self.line1, = self.ax.plot([], [], 'b-o', label='Line 1')
        self.line2, = self.ax.plot([], [], 'r-s', label='Line 2')
        
        # Show legend
        self.ax.legend()
    
    def update_graph(self, point1, point2):
        """
        Add new points for both lines and update the display.
        
        Parameters:
            point1 (tuple): (new_x1, new_y1) for the first line
            point2 (tuple): (new_x2, new_y2) for the second line
        """
        # Append new data points
        new_x1, new_y1 = point1
        new_x2, new_y2 = point2
        
        self.x_data1.append(new_x1)
        self.y_data1.append(new_y1)
        self.x_data2.append(new_x2)
        self.y_data2.append(new_y2)
        
        # Update line data
        self.line1.set_data(self.x_data1, self.y_data1)
        self.line2.set_data(self.x_data2, self.y_data2)
        
        # Rescale axes to fit the new data
        self.ax.relim()
        self.ax.autoscale_view()
        
        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()




def render_live_price_chart(symbol="PERP_SOL_USDC", max_points=100):
    """
    Renders a live price chart inside Streamlit using session state to preserve history.
    Automatically updates if page refreshes (or use st_autorefresh in main app).
    """

    url = f"https://api-evm.orderly.org/v1/public/futures/{symbol}"
    
    # Initialize session state
    if 'price_history' not in st.session_state:
        st.session_state.price_history = []

    # Get current timestamp
    current_time = time.time()
    if 'start_time' not in st.session_state:
        st.session_state.start_time = current_time

    elapsed = round(current_time - st.session_state.start_time, 2)

    # Fetch price
    try:
        response = requests.get(url)
        data = response.json()['data']
        mark_price = data['mark_price']
        index_price = data['index_price']
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    # Store data
    st.session_state.price_history.append({
        "Time": elapsed,
        "Mark Price": mark_price,
        "Index Price": index_price
    })

    # Trim history to keep size manageable
    if len(st.session_state.price_history) > max_points:
        st.session_state.price_history = st.session_state.price_history[-max_points:]

    # Plot
    df = pd.DataFrame(st.session_state.price_history)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Mark Price"], mode='lines', name='Futures Price'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Index Price"], mode='lines', name='Spot Price'))
    fig.update_layout(title=f"{symbol} Price Chart", xaxis_title="Time (s)", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)


def get_orderly_price(symbol):
    import requests
    try:
        url = f"https://api-evm.orderly.org/v1/public/futures/{symbol}"
        response = requests.get(url)
        data = response.json()["data"]
        return data["mark_price"], data["index_price"]
    except:
        return None, None