import argparse
import sys
import timeit
from utils import *

def get_slope(contracts, i1, i2):
    slope = (contracts[i2]['price'] - \
        contracts[i1]['price']) / (i2 - i1)
    return slope

def find_max_profit(contracts, mid):
    right_i = mid + 1
    left_i = mid - 1

    best_right_i = right_i
    best_left_i = left_i
    max_slope = get_slope(contracts, left_i, right_i)

    for i in xrange(left_i):
        slope = get_slope(contracts, i, right_i)
        if slope > max_slope:
            max_slope = slope
            best_left_i = i

    min_slope = max_slope
    for i in xrange(right_i + 2, len(contracts)):
        slope = get_slope(contracts, best_left_i, i)
        if slope < min_slope:
            min_slope = slope
            best_right_i = i

    return (best_left_i, best_right_i)

def trade(options, debug=False):
    for exp_date in options.keys():
        if debug == True:
            print "================ exp %s ==================" % (exp_date)

        # sort options by acending strike price
        contracts = options[exp_date]
        contracts.sort(key=lambda x: x['strike'])

        # find arbitrage opportunity
        best_start = 0
        best_mid = 0
        best_end = 0
        maxp = 0
        for i in xrange(len(contracts) - 2):
            strike1 = contracts[i]['strike']
            strike2 = contracts[i+1]['strike']
            strike3 = contracts[i+2]['strike']
            price1 = contracts[i]['price']
            price2 = contracts[i+1]['price']
            price3 = contracts[i+2]['price']
            if cmp_float(strike1 + strike3, strike2 * 2) == 0\
                and cmp_float(price1 + price3, price2 * 2) == -1:
                mid = i + 1
                [start, end] = find_max_profit(contracts, mid)
                dist_left = mid - start
                dist_right = end - mid
                alpha = float(dist_right) / float(dist_left + dist_right)
                profit = contracts[mid]['price'] - (
                    alpha * contracts[start]['price'] +
                    (1 - alpha) * contracts[end]['price'])
                if profit > maxp:
                    maxp = profit
                    best_start = start
                    best_end = end
                    best_mid = mid


        if debug == True:
            print "%s(%f) %s(%f) <=> %s(%f) %f" % (
                contracts[best_start]['code'],
                contracts[best_start]['price'],
                contracts[best_end]['code'],
                contracts[best_end]['price'],
                contracts[best_mid]['code'],
                contracts[best_mid]['price'],
                maxp)

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

# parse CLI options
parser = argparse.ArgumentParser(
    description="Find option arbitrage opportunities")
parser.add_argument(
    '--date', help='trading date', required=True)
parser.add_argument(
    '--symbol', help='equity symbol', required=True)
parser.add_argument(
    '--type', help='option type: [call|put]', required=True)
parser.add_argument(
    '--debug', help='turn on debug mode', action='store_true')
args = parser.parse_args()

options = get_options(args.date, args.symbol, args.type)
wrapped = wrapper(trade, options, debug=args.debug)
elapsed = timeit.Timer(wrapped).timeit(number=100000)
print "elapsed: %f" % (elapsed)
