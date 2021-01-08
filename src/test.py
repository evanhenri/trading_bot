import argparse
import decimal


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    training_parser = subparsers.add_parser('training')
    training_parser.add_argument('--elapsed_trades', default=int)
    training_parser.add_argument('--market', required=True)
    training_parser.add_argument('--usd_threshold', default=100, type=decimal.Decimal)


    # parser.add_argument('training_steps', default=1000, nargs='?', type=int)
    # parser.add_argument('--dashboard', action='store_true')
    # parser.add_argument('--plot', action='store_true')

    return parser.parse_args()


def main():
    print(parse_args())


if __name__ == '__main__':
    main()