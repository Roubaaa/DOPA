import tensorflow as tf
from tensorflow.keras import layers, losses, models

class UNet:
    """
    UNet is a deep learning architecture for image segmentation
    
    This implementation creates a U-Net model with the following characteristics:
    - Symmetric encoder-decoder architecture with skip connections
    - Configurable input shape and filter sizes
    - Uses batch normalization and dropout for regularization
    - Implements a combination of binary cross-entropy and dice loss for training
    
    The architecture consists of:
    1. Encoder path (downsampling): Extracts features through repeated convolution and pooling
    2. Bottleneck: Processes the most abstract features
    3. Decoder path (upsampling): Reconstructs the image using transposed convolutions and skip connections
    """
    def __init__(self, input_shape=(256, 256, 3), num_filters=[16, 32, 64, 128, 256]):
        self.input_shape = input_shape
        self.num_filters = num_filters
        self.model = self.build_unet()
    
    def __downward_conv(self, input_tensor, num_filters, activation='relu', padding='same'):
        """Downward convolution block"""
        down = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, padding=padding)(input_tensor)
        down = layers.BatchNormalization()(down)
        down = layers.Activation(activation)(down)
        down = layers.Dropout(0.15)(down)
        down = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, padding=padding)(down)
        down = layers.BatchNormalization()(down)
        down = layers.Activation(activation)(down)
        down = layers.Dropout(0.15)(down)
        pool = layers.MaxPool2D(pool_size=(2,2), strides=(2,2))(down)
        return down, pool
    
    def __bottleneck(self, input_tensor, num_filters, activation='relu', padding='same'):
        """Bottleneck block"""
        mid = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, padding=padding)(input_tensor)
        mid = layers.BatchNormalization()(mid)
        mid = layers.Activation(activation)(mid)
        mid = layers.Dropout(0.15)(mid)
        mid = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, activation=activation, padding=padding)(mid)
        mid = layers.BatchNormalization()(mid)
        mid = layers.Activation(activation)(mid)
        mid = layers.Dropout(0.15)(mid)
        return mid
    
    def __upward_conv(self, input_tensor, corresponding_down_tensor, num_filters, activation='relu', padding='same'):
        """Upward convolution block"""
        up = layers.Conv2DTranspose(filters=num_filters, kernel_size=(2,2), strides=(2,2), padding=padding)(input_tensor)
        up = layers.concatenate([corresponding_down_tensor, up], axis=-1)
        up = layers.BatchNormalization()(up)
        up = layers.Activation(activation)(up)
        up = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, padding=padding)(up)
        up = layers.BatchNormalization()(up)
        up = layers.Activation(activation)(up)
        up = layers.Dropout(0.15)(up)
        up = layers.Conv2D(filters=num_filters, kernel_size=(3,3), strides=1, padding=padding)(up)
        up = layers.BatchNormalization()(up)
        up = layers.Activation(activation)(up)
        up = layers.Dropout(0.15)(up)
        return up
    
    def build_unet(self):
        """" Build the U-Net model"""
        inputs = layers.Input(shape=self.input_shape)
        down1, pool1 = self.__downward_conv(inputs, self.num_filters[0])
        down2, pool2 = self.__downward_conv(pool1, self.num_filters[1])
        down3, pool3 = self.__downward_conv(pool2, self.num_filters[2])
        down4, pool4 = self.__downward_conv(pool3, self.num_filters[3])
        
        middle = self.__bottleneck(pool4, self.num_filters[4])
        
        up1 = self.__upward_conv(middle, down4, self.num_filters[3])
        up2 = self.__upward_conv(up1, down3, self.num_filters[2])
        up3 = self.__upward_conv(up2, down2, self.num_filters[1])
        up4 = self.__upward_conv(up3, down1, self.num_filters[0])
        
        output = layers.Conv2D(filters=1, kernel_size=(1,1), activation='sigmoid', padding='same')(up4)
        
        model = models.Model(inputs=inputs, outputs=output)
        
        model.compile(
            optimizer='adam',
            loss=self.bce_dice_loss,
            metrics=[self.dice_loss])
        
        return model
    
    @staticmethod
    def dice_coeff(y_true, y_pred):
        smooth = 1.0
        y_true_f = tf.reshape(y_true, [-1])
        y_pred_f = tf.reshape(y_pred, [-1])
        intersection = tf.reduce_sum(y_true_f * y_pred_f)
        return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)
    
    @staticmethod
    def dice_loss(y_true, y_pred):
        return 1 - UNet.dice_coeff(y_true, y_pred)
    
    @staticmethod
    def bce_dice_loss(y_true, y_pred):
        return losses.binary_crossentropy(y_true, y_pred) + UNet.dice_loss(y_true, y_pred)
    
    def summary(self):
        """Print model summary"""
        self.model.summary()
    
    def plot_model(self):
        """Plot model architecture"""
        tf.keras.utils.plot_model(self.model, show_shapes=True, show_layer_names=True)