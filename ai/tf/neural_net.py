import os

import tensorflow as tf

from . import (
    INPUT_SIZE,
    OUTPUT_SIZE,
    LEARNING_RATE,
    NEURON_COUNT,
    managers
)

layers = managers.LayerManager()

# None is corresponds to the fact that this is a placeholder. It means to
# accept all possible samples but each sample should only have 1 element
# in it (x_data is a list of lists that each have a length of 1).
with tf.name_scope('inputs'):
    keep_prob = tf.placeholder(
        tf.float32,
        name='keep_prob'
    )

    x_inputs = tf.placeholder(
        tf.float32,
        shape=[None, INPUT_SIZE], # 1 x 1
        name='x_inputs'
    )

    y_inputs = tf.placeholder(
        tf.float32,
        shape=[None, OUTPUT_SIZE], # 1 x 1
        name='y_inputs'
    )


hidden_layer = layers.add(
    inputs=x_inputs,
    in_size=INPUT_SIZE,
    out_size=NEURON_COUNT,
    activation_func=tf.nn.relu,
    keep_prob=keep_prob
)


# This represents the layer with 1 output value which is the
# prediction made by the neural net
output_layer = layers.add(
    inputs=hidden_layer,
    in_size=NEURON_COUNT,
    out_size=OUTPUT_SIZE,
    activation_func=None,
    keep_prob=keep_prob
)


# Compute square error between the prediction and real data
# Sum all of the predictions for all the samples
# Take the mean value of that sum
# This is the loss for ALL samples and ALL features
with tf.name_scope('loss'):
    cross_entropy = tf.reduce_mean(
        tf.reduce_sum(
            tf.square(
                y_inputs - output_layer,
                name='square'
            ),
            reduction_indices=[1],
            name='reduce_sum'
        ),
        name='loss_op'
    )
    tf.summary.scalar(
        'loss',
        tensor=cross_entropy
    )


with tf.name_scope('train'):
    optimizer_op = tf.train.GradientDescentOptimizer(
        learning_rate=LEARNING_RATE,
        name='optimizer_op'
    )
    training_op = optimizer_op.minimize(
        cross_entropy,
        name='training_op'
    )


class NN:
    def __init__(self, n_steps, input_size, output_size, cell_size, batch_size):
        self.n_steps = n_steps
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size
        self.batch_size = batch_size

        with tf.name_scope('inputs'):
            # keep_prob = tf.placeholder(
            #     tf.float32,
            #     name='keep_prob'
            # )

            x_inputs = tf.placeholder(
                tf.float32,
                shape=[None, n_steps, input_size],
                name='x_inputs'
            )

            y_inputs = tf.placeholder(
                tf.float32,
                shape=[None, n_steps, output_size],
                name='y_inputs'
            )


def run(queue, training_steps, x_train, y_train):
    train_writer = tf.summary.FileWriter(
        logdir='logs/train',
        graph=tf.get_default_graph()
    )
    test_writer = tf.summary.FileWriter(
        logdir='logs/test',
        graph=tf.get_default_graph()
    )

    run_options = tf.RunOptions(
        trace_level=tf.RunOptions.FULL_TRACE
    )

    run_metadata = tf.RunMetadata()
    merged = tf.summary.merge_all()

    with tf.Session() as sess:
        sess.run(
            tf.global_variables_initializer()
        )

        for step in range(training_steps):
            sess.run(
                training_op,
                feed_dict={
                    x_inputs : x_train,
                    y_inputs : y_train,
                    keep_prob: keep_prob
                },
                options=run_options,
                run_metadata=run_metadata
            )

            # predicted_value = sess.run(
            #     output_layer,
            #     feed_dict={
            #         x_inputs: x_train
            #     },
            #     options=run_options,
            #     run_metadata=run_metadata
            # )
            #
            # error_rate = sess.run(
            #     cross_entropy,
            #     feed_dict={
            #         x_inputs: x_train,
            #         y_inputs: y_train
            #     },
            #     options=run_options,
            #     run_metadata=run_metadata
            # )
            #
            # queue.put([
            #     predicted_value,
            #     error_rate
            # ])

            if step % 100 == 0:
                train_writer.add_summary(
                    summary=sess.run(
                        merged,
                        feed_dict={
                            x_inputs: x_train,
                            y_inputs: y_train,
                            keep_prob: 1
                        },
                    ),
                    global_step=step
                )
                test_writer.add_summary(
                    summary=sess.run(
                        merged,
                        feed_dict={
                            x_inputs: x_test,
                            y_inputs: y_test,
                            keep_prob: 1
                        },
                    ),
                    global_step=step
                )

                train_writer.add_run_metadata(
                    run_metadata,
                    tag=f'step{step}',
                    global_step=step
                )
                test_writer.add_run_metadata(
                    run_metadata,
                    tag=f'step{step}',
                    global_step=step
                )


def load(restore_dp, restore_name=None):
    saver = tf.train.Saver()

    if restore_name is None:
        for fn in os.listdir(restore_dp):
            name, ext = os.path.splitext(fn)
            if ext == '.ckpt':
                restore_name = fn
                break

    with tf.Session() as sess:
        saver.restore(
            sess=sess,
            save_path=os.path.join(
                restore_dp,
                restore_name
            )
        )
        sess.run(
            tf.global_variables_initializer()
        )


def save(save_dp, save_name):
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(
            tf.global_variables_initializer()
        )

        os.makedirs(save_dp, exist_ok=True)
        name, ext = os.path.splitext(save_name)

        return saver.save(
            sess=sess,
            save_path=os.path.join(
                save_dp,
                name + ext if ext else '.ckpt'
            )
        )
