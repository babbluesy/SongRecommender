import tensorflow as tf
from datetime import datetime

shape = (int(10000), int(10000))

startTime = datetime.now()

with tf.device("/gpu:0"):
    random_matrix = tf.random.uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)

print("\n" * 2)
print("Time taken(GPU):", datetime.now() - startTime)
print("\n" * 2)

startTime = datetime.now()

with tf.device("/cpu:0"):
    random_matrix = tf.random.uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)

print("\n" * 2)
print("Time taken(CPU):", datetime.now() - startTime)
print("\n" * 2)

