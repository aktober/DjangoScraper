import datetime
import requests


def get_best_worse_currencies():
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=10')
    data = r.json()
    data_list = []
    for pair in data:
        item = []
        if pair["percent_change_7d"]:
            item.append(float(pair["percent_change_7d"]))
            item.append(pair["name"])
            item.append(float(pair["price_usd"]))
            data_list.append(item)

    data_list_sorted = sorted(data_list)
    list_len = len(data_list)
    worse = data_list_sorted[:3]
    best = list(reversed(data_list_sorted[list_len-3:]))

    return best, worse


def get_low_high_btc_week_price():
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    r = requests.get('http://api.coindesk.com/v1/bpi/historical/close.json?'
                     'currency=BTC'
                     '&start=' + week_ago_str +
                     '&end=' + today_str)
    data = r.json()
    prices = []
    for i in data['bpi']:
        prices.append(data['bpi'][i])

    prices.sort()
    low = prices[0]
    high = prices[len(prices) - 1]

    return low, high


def get_current_market_and_dominance():
    r = requests.get('https://api.coinmarketcap.com/v1/global/')
    data = r.json()
    market = data['total_market_cap_usd']
    dominance = data['bitcoin_percentage_of_market_cap']
    return market, dominance


def get_market_week_ago():
    r = requests.get('https://graphs.coinmarketcap.com/global/marketcap-total/')
    data = r.json()
    market_data = data['market_cap_by_available_supply']
    count = len(market_data)
    market_week_ago =  market_data[count - 1 - 7][1]
    return market_week_ago


def get_dominance_week_ago():
    r = requests.get('https://graphs.coinmarketcap.com/global/dominance/')
    data = r.json()
    dominance_data = data['bitcoin']
    count = len(dominance_data)
    dominance_week_ago =  dominance_data[count - 1 - 7][1]
    return dominance_week_ago


def get_value_diff(current, previous):
    full_percent = current * 100 / previous
    diff_percent = full_percent - 100
    return diff_percent


def get_current_btc():
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')
    data = r.json()
    return data[0]['price_usd']
