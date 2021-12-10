order_buy = client.create_order(
    symbol='DOTBUSD',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.5,
    price='25')
    
    
    
order_sell = client.create_order(
    symbol='DOTBUSD',
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.5,
    price='48')
    
orders = client.get_open_orders(symbol='DOTBUSD')

order_status = client.get_order(
    symbol='DOTBUSD',
    orderId=str(orders[0]['orderId']))

result = client.cancel_order(
    symbol='DOTBUSD',
    orderId=str(orders[0]['orderId']))

fees = client.get_trade_fee(symbol='DOTBUSD')
    

Get all open orders
orders_allopens = client.get_open_orders(symbol='DOTBUSD')
