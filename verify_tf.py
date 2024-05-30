import tensorflow as tf
print("TensorFlow version:", tf.__version__)
# Check if Metal device is available
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    print("TensorFlow Metal is installed and configured correctly.")
else:
    print("TensorFlow Metal installation may have encountered an issue.")


