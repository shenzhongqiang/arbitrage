import os.path
import sys

# compare two float numbers
def cmp_float(f1, f2):
    if f1 - f2 < -10**-10:
        return -1
    elif f1 - f2 > 10**-10:
        return 1
    else:
        return 0

# read data from file and return dictionay
def get_options(op_symbol, op_type):
    # generate filename from CLI options
    ROOT_DIR = os.path.dirname(
        os.path.realpath(__file__))
    filename = "%s.%s" % (op_symbol, op_type)
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
    return options
