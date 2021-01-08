import tensorflow as tf

from . import BIAS


class LayerManager:
    def __init__(self):
        self.count = -1

    def __len__(self):
        return self.count

    def add(self, inputs, in_size, out_size, activation_func, keep_prob):
        self.count += 1
        layer_name = f'layer_{self.count}'

        with tf.name_scope(layer_name):
            with tf.name_scope('weights'):
                weights = tf.Variable(
                    tf.random_normal(
                        [in_size, out_size],
                        name='W'
                    )
                )
                tf.summary.histogram(
                    name=None,
                    values=weights
                )

            # initialize all bias values as being == 0.1
            # [1 row, 1 column (out_size == 1)]
            with tf.name_scope('biases'):
                biases =  tf.Variable(
                    tf.zeros(
                        [1, out_size],
                        name='b'
                    ) + BIAS
                )
                tf.summary.histogram(
                    name=None,
                    values=biases
                )

            with tf.name_scope('Wx_plus_b'):
                outputs = tf.nn.dropout(
                    x=tf.matmul(inputs, weights) + biases,
                    keep_prob=keep_prob
                )

            if callable(activation_func):
                outputs = activation_func(outputs)

                tf.summary.histogram(
                    name='activations',
                    values=outputs
                )

            tf.summary.histogram(
                name='outputs',
                values=outputs
            )

        return outputs
