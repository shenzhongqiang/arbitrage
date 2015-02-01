import argparse
import matplotlib.pyplot as plt
from utils import *

# parse CLI options
parser = argparse.ArgumentParser(
    description="plot strike/price chart")
parser.add_argument(
    '--symbol', help='equity symbol', required=True)
parser.add_argument(
    '--type', help='option type: [call|put]', required=True)
args = parser.parse_args()

options = get_options(args.symbol, args.type)

strikes = []
prices = []
for exp_date in options.keys():
    # sort options by acending strike price
    contracts = options[exp_date]
    contracts.sort(key=lambda x: x['strike'])

    strikes = map(lambda x: x['strike'], contracts)
    prices = map(lambda x: x['price'], contracts)
    break

plt.plot(strikes, prices, 'rx')
plt.plot(strikes, prices, 'g')
plt.xlabel('strike')
plt.ylabel('price')
#plt.set_title('Option strike/price plot')
plt.show()
