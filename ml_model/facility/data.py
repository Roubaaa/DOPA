import tensorflow as tf

class WellpadDataset:
    """Dataset class for handling satellite imagery data for wellpad detection."""
    
    def __init__(self):
        """The dataset is configured to work with RGB (Red, Green, Blue) satellite imagerybands"""
        self.bands = ['R','G','B']

    def get(self, pattern):
        """
        Load and preprocess a dataset from TFRecord files.
        
        This method performs the following steps:
        1. Defines the feature schema for parsing TFRecords
        2. Loads TFRecord files matching the specified pattern
        3. Parses the records into tensors
        4. Converts the tensors into (image, mask) tuples
        5. Normalizes the images if needed
        6. Caches the dataset for improved performance
        """
        self.__describe_features()
        # Find all TFRecord files matching the pattern
        glob = tf.io.gfile.glob(pattern)
        # Create a TFRecordDataset from the files (using GZIP compression)
        ds = tf.data.TFRecordDataset(glob, compression_type='GZIP')

        # Apply preprocessing pipeline with parallel processing
        ds = ds.map(self.__parse_tfrecord, num_parallel_calls=5)
        ds = ds.map(self.__to_tuple, num_parallel_calls=5)
        ds = ds.map(self.__resize, num_parallel_calls=5)
        
        # Cache the dataset to avoid reloading it on subsequent epochs
        ds = ds.cache()
        
        return ds
    
    def __describe_features(self):
        """Creates a dictionary mapping feature names to TensorFlow FixedLenFeature objects,
        which describe the shape and type of each feature in the input dataset."""
        label = 'Label'
        self.featureNames = self.bands + [label]

        # Create FixedLenFeature objects for each band and the label
        cols = [tf.io.FixedLenFeature(shape=[256,256], dtype=tf.float32) for band in self.featureNames]
        
        # Create a dictionary mapping feature names to their descriptions
        self.features = dict(zip(self.featureNames, cols))

        return self.features

    def __parse_tfrecord(self, ex):
        """Parse a single TFRecord example into a dictionary of tensors.
"""
        return tf.io.parse_single_example(ex, self.features)

    def __to_tuple(self, inputs):
        """Convert parsed tensors to (image, mask) tuples."""
        inputsList = [inputs.get(key) for key in self.featureNames]

        # Stack tensors along a new axis to create a 3D tensor
        stacked = tf.stack(inputsList, axis=0)
        # Transpose from [bands, height, width] to [height, width, bands]
        stacked = tf.transpose(stacked, [1, 2, 0])
        
        # Split into image (RGB) and mask (Label)
        return stacked[:,:,:len(self.bands)], stacked[:,:,len(self.bands):]

    def __resize(self, image, mask):
        """Normalize the image if needed while preserving the mask."""
        max_value = tf.reduce_max(image)
        image = tf.cond(max_value > 1.0, lambda: image / max_value, lambda: image)

        return image, mask