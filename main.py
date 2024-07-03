from datetime import datetime, timedelta
import json

from configs.config import TRUST_ACCOUNT_NUMBER, TICKERS_OF_IV_50_70, TICKERS_OF_IV_70_100, TICKERS_OF_IV_100_and_above
from trading.stock_screener import StockScreener
from trading.trade_options import TradeOptions
from options.options import Options, OptionInstruction, OptionType
from options.stocks import Stocks

TICKERS_TO_SELL_OPTION_DICT = {"put": ["UPST", "DUOL"],
                               "call": ["UPST", "DUOL"]}


if __name__ == '__main__':
    trade_options = TradeOptions()
    # # buy one share of UUUU at limit price $5.0
    # stock_order = Stocks.create_a_stock_order(ticker="UUUU", quantity=1, price=5.0)
    # # send the order to a specific account;
    # trade_options.trade_an_order(TRUST_ACCOUNT_NUMBER, stock_order)

    # # sell to open a put option for UPST with strike price $22, expiration date 2024-06-21
    # option_order = Options.create_an_option_order(ticker="UPST",
    #                                                strike_price=22,
    #                                                expiration_date=datetime(2024, 7, 19),
    #                                                quantity=1,
    #                                                option_price=3.5,
    #                                                option_type=OptionType.PUT,
    #                                                instruction=OptionInstruction.SELL_TO_OPEN)
    # option_order = {'orderType': 'NET_CREDIT', 
    #                 'session': 'NORMAL', 
    #                 'duration': 'DAY', 
    #                 'orderStrategyType': 'SINGLE', 
    #                 'complexOrderStrategyType': 'CUSTOM', 
    #                 'price': 3.0, 
    #                 'orderLegCollection': [{
    #                     'orderLegType': 'OPTION', 'legId': 1, 'instruction': 'BUY_TO_CLOSE', 'quantity': 1.0, 'instrument': {'assetType': 'OPTION', 'symbol': 'PDD   240712P00138000'}}, 
    #                     {'orderLegType': 'OPTION', 'legId': 2, 'instruction': 'SELL_TO_OPEN', 'quantity': 1.0, 'instrument': {'assetType': 'OPTION', 'symbol': 'PDD   240816P00135000'}}]}
    # trade_options.trade_an_order(TRUST_ACCOUNT_NUMBER, option_order)

    # quote_json = trade_options.client.quote("DUOL").json()
    # stock = Stocks.initialize_from_quote_json("DUOL", quote_json)
    # stock.get_price_history(trade_options.client, datetime.now() - timedelta(days=30), datetime.now())


    # # get a stock quote and price history
    # print("|\n|client.quote(\"DUOL\").json()", end="\n|")
    # print(trade_options.client.quote("DUOL").json())
    # print("|\n|client.price_history(\"DUOL\").json()", end="\n|")
    # price_history_json = trade_options.client.price_history(symbol="DUOL", 
    #                         periodType='month', 
    #                         period=1, 
    #                         frequencyType='daily',
    #                         frequency=1,
    #                         startDate=datetime.strptime('5/17/2024', "%m/%d/%Y"),
    #                         endDate=datetime.strptime('6/17/2024', "%m/%d/%Y")
    #                         ).json()    
    # # # save the json to a file
    # with open("duol_price_history.json", "w", encoding="utf-8") as f:
    #     json.dump(price_history_json, f, ensure_ascii=False, indent=4)
    #     f.close()

    # # get an option chain
    # print("|\n|client.option_chains(\"DUOL\").json()", end="\n|")
    # option_chain_json = trade_options.client.option_chains("DUOL").json()
    # # save the json to a file
    # with open("duol_option_chains.json", "w", encoding="utf-8") as f:
    #     json.dump(option_chain_json, f, ensure_ascii=False, indent=4)
    #     f.close()

    # Scan through all positions of all accounts and rollout the winning and losing options;
    trade_options.trade_all_accounts()

    # Scan through high IV stocks and sell options if the day, week, or month change is larger than x percent
    tickers_to_scan = TICKERS_OF_IV_50_70 + TICKERS_OF_IV_70_100 + TICKERS_OF_IV_100_and_above
    stock_screener = StockScreener(client=trade_options.client, tickers_to_scan=tickers_to_scan)
    tickers_to_sell_option_dict = stock_screener.day_change_larger_than_x_percent(5)
    print("Day change > 5%", tickers_to_sell_option_dict)
    tickers_to_sell_option_dict = stock_screener.week_change_larger_than_x_percent(10)
    print("Week change > 10%", tickers_to_sell_option_dict)
    tickers_to_sell_option_dict = stock_screener.month_change_larger_than_x_percent(20)
    print("Month change > 20%", tickers_to_sell_option_dict)
    tickers_to_sell_option_dict = {
        "put": stock_screener.put_sell_candidates,
        "call": stock_screener.call_sell_candidates
    }
    trade_options.sto_given_tickers(TRUST_ACCOUNT_NUMBER, tickers_to_sell_option_dict)
    

    trade_options.display_all_orders()