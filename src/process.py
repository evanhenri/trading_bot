#!/usr/bin/env python3.6
import argparse
import decimal
import functools
import logging
import multiprocessing
import subprocess
import sys

import matplotlib.pyplot as plt
import numpy as np

# from trader.process import neural_net

from trader.process import train
from trader.store import db

import settings


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(
    logging.StreamHandler(sys.stdout)
)


# def get_training_data(training_steps):
#     # Make an array of 300 samples values starting with -1 and ending with 1
#     sample_data = np.linspace(-1, 1, training_steps)
#
#     # Restructure our sample data so each value is in it's own array instead of
#     # having all values in the same giant array. 1d -> 2d
#     x_train = sample_data[:, np.newaxis]
#
#     # Create a normal distribution to introduce noise into the sample data
#     #   mean = 0
#     #   standard deviation = 0.05
#     #   shape = same as our x_data's shape
#     noise = np.random.normal(0, 0.05, x_train.shape)
#     y_train = np.square(x_train) - 0.5 + noise
#
#     return x_train, y_train
#
#
# def get_plot(x_data, y_data, show_plot=False):
#     class Plot:
#         def __init__(self, _x_data, _y_data, _show_plot):
#             self._show_plot = _show_plot
#
#             if self._show_plot:
#                 fig = plt.figure()
#
#                 self._x_data = _x_data
#                 self._y_data = _y_data
#                 self._plot_lines = []
#
#                 # 1 plot on a grid with 1 row and 1 column
#                 self._grid = fig.add_subplot(1, 1, 1)
#                 self._grid.scatter(
#                     self._x_data,
#                     self._y_data
#                 )
#                 self._plot = functools.partial(
#                     self._grid.plot,
#                     color='r',
#                     linestyle='-',
#                     linewidth=5
#                 )
#
#         def update(self, predicted_value):
#             if self._show_plot:
#                 if self._plot_lines:
#                     self._grid.lines.remove(self._plot_lines[0])
#
#                 self._plot_lines = self._plot(
#                     self._x_data,
#                     predicted_value,
#                 )
#
#                 plt.pause(
#                     interval=0.1
#                 )
#
#     return Plot(x_data, y_data, show_plot)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    train_parser = subparsers.add_parser('train')
    train_parser.add_argument('--elapsed_trades', default=5, type=int)
    train_parser.add_argument('--market', required=True)
    train_parser.add_argument('--usd_threshold', default=100, type=decimal.Decimal)


    # parser.add_argument('training_steps', default=1000, nargs='?', type=int)
    # parser.add_argument('--dashboard', action='store_true')
    # parser.add_argument('--plot', action='store_true')

    return parser.parse_args()


def main():
    args = parse_args()
    log.debug(args)

    dsn = db.DatabaseDSN(
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )

    import time
    time.sleep(
        999999999
    )

    # trainer = train.Trainer(
    #     dsn=dsn,
    #     market=args.market,
    #     elapsed_trades=args.elapsed_trades,
    #     usd_threshold=args.usd_threshold
    # )
    #
    # for order_book_activity, target_trade in trainer:
    #     log.debug(f'{len(order_book_activity)}, {target_trade}')


    # training_steps = args.training_steps
    #
    # x_train, y_train = get_training_data(training_steps)
    # queue = multiprocessing.Queue()
    #
    # if args.dashboard:
    #     proc = subprocess.Popen(
    #         ['tensorboard', '--host=127.0.0.1', '--logdir=logs', '--port=8080'],
    #         stdout=subprocess.PIPE
    #     )
    #
    # multiprocessing.Process(
    #     target=neural_net.run,
    #     args=(
    #         queue,
    #         training_steps,
    #         x_train,
    #         y_train,
    #     )
    # ).start()
    #
    # # plot = get_plot(x_train, y_train, show_plot=args.plot)
    #
    # # for i in range(training_steps):
    # #     predicted_value, error_rate = queue.get()
    # #     if i % 50 == 0:
    # #         plot.update(predicted_value)
    # #         print(f'{i}/{training_steps}) Error Rate: {error_rate}')
    #
    # input('Done!')
    #
    # try:
    #     proc.kill()
    # except NameError:
    #     pass


if __name__ == '__main__':
    main()
