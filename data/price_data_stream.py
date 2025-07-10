import requests
import helpers
import json
import time
from helpers import LiveGraph

symbol = 'PERP_SOL_USDC'
url = f"https://api-evm.orderly.org/v1/public/futures/{symbol}"

def get_price_info():
    response = requests.request("GET", url)
    info = json.loads(response.text)
    data = info['data']
    print('index_price: ', data['index_price'], '   mark_price: ', data['mark_price'])
    return data['mark_price'], data['index_price']  #target price quote


# Initialize the live graph
graph = LiveGraph(title='Live Data Plot')

start_time = time.time()


while True:
    mark_price, index_price = get_price_info()
    current_time = time.time() - start_time
    
    # Update the graph with the new data point
    graph.update_graph( (current_time, mark_price), (current_time, index_price) )

    time.sleep(0.2)




