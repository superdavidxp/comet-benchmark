# singularity

1. pytorch 
   * mnist

2. tensorflow
   * cifar10

3. theano

4. keras
   * mnist

Note:

* TensorFlow vs Keras
    * Keras is a high-level neural networks API that build on TensorFlow or Keras.
    * Keras is faster to deploy while TensorFlow is more flexible and powerful.
    * TensorFlow-1.9.0 enhanced Keras support. **tf.contrib.Keras + tf = all you ever gonna need**
* Pytorch vs Tensorflow
    * Pytorch dynamic vs TensorFlow static graph definition.
    * Pytorch is easy to debug.
    * Pytorch need 3rd party tool to visualize (matplotlib), TensorFlow has native tensorboard.
    * Pytorch can leverage multiple GPUs with almost no effort, TensorFlow defining parallelism is more manual.
* Multiple CPU Cores on Tensorflow and Keras
    * By default all CPUs available to the process are aggregated under "/cpu:0" device.
    * Only the different GPUs of one machine get indexed and viewed as separate devices.
