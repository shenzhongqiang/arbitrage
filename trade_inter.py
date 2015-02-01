import argparse
import os.path
import sys
from utils import *

# find max profit point when start and end is fixed
def find_max_profit_range(contracts, start, end):
    maxp = 0
    max_mid = 0
    for mid in xrange(start + 1, end):
        dist_left = mid - start
        dist_right = end - mid
        alpha = float(dist_right) / float(dist_left + dist_right)
        profit = contracts[mid]['price'] - (
            alpha * contracts[start]['price'] +
            (1 - alpha) * contracts[end]['price'])
        if profit > maxp:
            maxp = profit
            max_mid = mid
    return (max_mid, maxp)

def find_max_profit(contracts, start):
    maxp = 0
    max_mid = 0
    max_end = 0
    for end in xrange(start + 2, len(contracts)):
        [mid, profit] = find_max_profit_range(contracts, start, end)
        if profit > maxp:
            maxp = profit
            max_mid = mid
            max_end = end
    return (max_mid, max_end, maxp)

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
    max_start = 0
    max_mid = 0
    max_end = 0
    maxp = 0
    for i in xrange(len(contracts) - 2):
        [mid, end, profit] = find_max_profit(contracts, i)
        if profit > maxp:
            max_start = i
            max_mid = mid
            max_end = end
            maxp = profit


    print "%s(%f) %s(%f) <=> %s(%f) %f" % (
        contracts[max_start]['code'],
        contracts[max_start]['price'],
        contracts[max_end]['code'],
        contracts[max_end]['price'],
        contracts[max_mid]['code'],
        contracts[max_mid]['price'],
        maxp)


