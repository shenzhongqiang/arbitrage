import argparse
import sys
from utils import *

# parse CLI options
parser = argparse.ArgumentParser(
    description="Find option arbitrage opportunities")
parser.add_argument(
    '--symbol', help='equity symbol', required=True)
parser.add_argument(
    '--type', help='option type: [call|put]', required=True)
args = parser.parse_args()

options = get_options(args.symbol, args.type)

for exp_date in options.keys():
    print "================ exp %s ==================" % (exp_date)
    # sort options by acending strike price
    contracts = options[exp_date]
    contracts.sort(key=lambda x: x['strike'])

    # find arbitrage opportunity
    for i in xrange(len(contracts) - 2):
        strike1 = contracts[i]['strike']
        strike2 = contracts[i+1]['strike']
        strike3 = contracts[i+2]['strike']
        price1 = contracts[i]['price']
        price2 = contracts[i+1]['price']
        price3 = contracts[i+2]['price']
        if cmp_float(strike1 + strike3, strike2 * 2) == 0\
            and cmp_float(price1 + price3, price2 * 2) == -1:
            profit = price2 - (price1 + price3) / 2
            print "%s(%f) %s(%f) <=> %s(%f) %f" % (
                contracts[i]['code'],
                price1,
                contracts[i+2]['code'],
                price3,
                contracts[i+1]['code'],
                price2,
                profit)

