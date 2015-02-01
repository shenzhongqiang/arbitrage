import argparse
import os.path
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

# generate filename from CLI options
ROOT_DIR = os.path.dirname(
    os.path.realpath(__file__))
filename = "%s.%s" % (args.symbol, args.type)
filepath = os.path.join(ROOT_DIR, 'data', filename)

# if file does not exist, error
if not os.path.isfile(filepath):
    sys.stderr.write("no data for %s %s\n" % (
        args.symbol, args.type))
    sys.exit(1)

# read data from file
f = open(filepath, 'r')
contents = f.read()
f.close()
lines = contents.split('\n')
lines = lines[:-1]

options = {}
for line in lines:
    data = line.split()
    exp_date = data[7]
    code = data[1]
    strike = data[5]
    price = data[11]

    if not exp_date in options:
        options[exp_date] = []
    options[exp_date].append({'code': code,
        'strike': strike, 'price': price})

for exp_date in options.keys():
    # sort options by acending strike price
    contracts = options[exp_date]
    contracts.sort(key=lambda x: x['strike'])

    # find arbitrage opportunity
    for i in xrange(len(contracts) - 3):
        strike1 = float(contracts[i]['strike'])
        strike2 = float(contracts[i+1]['strike'])
        strike3 = float(contracts[i+2]['strike'])
        price1 = float(contracts[i]['price'])
        price2 = float(contracts[i+1]['price'])
        price3 = float(contracts[i+2]['price'])
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

