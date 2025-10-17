import ccxt
import time
import os
import sys

exchange = ccxt.binance({
        'rateLimit': 600,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',  # 使用币安期货市场
        },
    })
exchange.apiKey = ''
exchange.secret = ''

# 设置交易对
symbol = '1000BONK/USDT'

# 挂单分钟数值
order_minute = 0

# 初始倍数 Initial multiple
im = 1.20

# 累加参数 Cumulative parameter
# im = 1.20，cp = 0.02，挂单范围：1.20～1.58
cp = 0.02

while True:
    # 获取当前本地时间的分钟数值
    current_minute = time.localtime().tm_min

    # 检查是否为00分
    if current_minute % 10 == order_minute :
        try:
            # 全部撤单
            cancel_order = exchange.cancel_all_orders(symbol)
            print(symbol, '     全部撤单')

            # 获取最近的K线数据
            klines = exchange.fetch_ohlcv(symbol, '1m', limit=10)

            # 获取前1根K线的收盘价
            latest_kline = klines[-2][4]
            print(symbol, '     前1根K线的收盘价       ', '\033[1;32m {} \033[0m'.format(latest_kline))

            # 卖单参数
            for i in range(20):
                price = latest_kline * (im + cp * i)
                amount = ((i * 700 + 2800) - 10) / price

                sell_order = exchange.create_limit_sell_order(symbol, amount=amount, price=price, params={'timeInForce': 'GTX', 'reduceOnly': False, 'postOnly': True})

            print(symbol, '     挂单完成，等待1分钟', '     时间:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(60)

        except ccxt.ExchangeError as e:
            print(f"交易所错误: {e}", file=sys.stderr)
            os.system('say "交易所错误、交易所错误、交易所错误、交易所错误、交易所错误、交易所错误"')
            continue

        except ccxt.NetworkError as e:
            print(f"网络错误: {e}", file=sys.stderr)
            os.system('say "网络错误、网络错误、网络错误、网络错误、网络错误、网络错误"')
            continue

        except Exception as e:
            print(f"未知错误: {e}", file=sys.stderr)
            os.system('say "未知错误、未知错误、未知错误、未知错误、未知错误、未知错误"')
            continue
    else:
        # 如果不是整点，则休眠1秒并继续检查
        time.sleep(1)
