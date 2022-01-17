import pandas as pd
import requests

def get_items_df(base_url = 'https://python.zgulde.net'):
    response = requests.get(base_url)
    data = response.json()
    current_page = data['payload']['page']
    max_page = data['payload']['max_page']
    next_page = data['payload']['next_page']
    items = pd.DataFrame(data['payload']['items'])
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    current_page = data['payload']['page']
    max_page = data['payload']['max_page']
    next_page = data['payload']['next_page']
    items = pd.concat([items, pd.DataFrame(data['payload']['items'])]).reset_index(drop=True)
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()

    current_page = data['payload']['page']
    max_page = data['payload']['max_page']
    next_page = data['payload']['next_page']
    items = pd.concat([items, pd.DataFrame(data['payload']['items'])]).reset_index(drop=True)

    return items


def get_stores_df(base_url = 'https://python.zgulde.net'):
    stores_response = requests.get(base_url)
    stores_data = stores_response.json()
    stores_current_page = stores_data['payload']['page']
    stores_max_page = stores_data['payload']['max_page']
    stores_next_page = stores_data['payload']['next_page']
    stores = pd.DataFrame(stores_data['payload']['stores']).reset_index(drop=True)
    return stores


def get_sales_df():
    # first, create the response variable by requesting the url
    response = requests.get('https://python.zgulde.net/api/v1/sales')
    # turn the response into json
    data = response.json()
    # sales keys = ['payload', 'status']
    # payload keys = ['sales', 'max_page', 'next_page', 'page', 'previous_page']
    payload = data['payload'] # payload is the key containing the sales key
    # define the next page
    next_page = payload['next_page']
    # for use in DRY coding later, if i can get to it
    endpoint = 'sales'
    # create the initial dataframe from the sales on the first page
    sales = pd.DataFrame(payload[endpoint])
    # while loop to get data from all the subsequent pages and concatenate them to the sales df
    while next_page != None:
        # define the url for use below (like switching to the next page to get its contents)
        url = host + next_page
        # create the response for the next page url
        response = requests.get(url)
        # turn it into json
        data= response.json()
        # define a payload page
        payload = data['payload']
        # turn the sales content ('endpoint') into a df
        page_contents = pd.DataFrame(payload[endpoint])
        # concatenate the page_contents to the original sales df
        sales = pd.concat([sales,page_contents]).reset_index(drop=True)
        # resetting next_page
        next_page = payload["next_page"]
        # a short statement so i can watch as the data are acquired from one page to the next
        print("Sales data acquired")
    return sales 

def merge_dfs(sales, stores, items):
    sales_stores = pd.merge(sales, 
                        stores,
                        how="left",
                        left_on="store",
                        right_on="store_id")
    df = pd.merge(sales_stores,
                        items,
                        how="left",
                        left_on="item",
                        right_on="item_id")
    return df


def reproducibility():
    items = get_items_df(base_url = 'https://python.zgulde.net')
    stores = get_stores_df(base_url = 'https://python.zgulde.net')
    sales = get_sales_df()
    df = merge_dfs(sales, stores, items)
    return df


def get_power_data():
    if os.path.isfile('opsd_germany_daily_data.csv') == False:
        print("Data is not cached. Acquiring new power data.")
        opsd = new_power_data()
    else:
        print("Data is cached. Reading data from .csv file.")
        opsd = pd.read_csv('opsd_germany_daily_data.csv')
    print("Acquisition complete")
    return opsd