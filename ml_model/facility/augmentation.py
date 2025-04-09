import tensorflow as tf
import tensorflow.math as Math
import matplotlib.pyplot as plt

def color_augmentation(img):
  """
  Applies color augmentations suitable for false color imagery.
  Focuses on red channel scaling and color transformations.
  """
  # Random red channel scaling (since it's false color)
  red_scale = tf.random.uniform(shape=[], minval=0.8, maxval=1.2)
  
  # Split channels
  r, g, b = tf.split(img, 3, axis=-1)
  
  # Apply red channel scaling
  r = r * red_scale
  
  # Optional: Add slight random adjustments to other channels
  g_scale = tf.random.uniform(shape=[], minval=0.9, maxval=1.1)
  b_scale = tf.random.uniform(shape=[], minval=0.9, maxval=1.1)
  g = g * g_scale
  b = b * b_scale
  
  # Recombine channels
  img = tf.concat([r, g, b], axis=-1)
  
  # Apply brightness adjustment
  brightness_factor = tf.random.uniform(shape=[], minval=0.7, maxval=1.3)
  img = img * brightness_factor
  
  # Ensure values stay in valid range
  img = tf.clip_by_value(img, 0.0, 1.0)
  
  return img

def augmentation(img, msk):
  """
  Applies random data augmentation to image and mask pairs for deep learning training.
  This function performs several types of augmentations to increase dataset diversity:
  1. Random horizontal and vertical flips (50% probability each)
  2. Random 90-degree rotations (0°, 90°, 180°, or 270°)
  3. Random translations (up to 10% of image dimensions)
  4. Color augmentations for false color imagery
  """
  # Store original shape
  original_shape = tf.shape(img)
  original_height = original_shape[1]
  original_width = original_shape[2]

  # Independent random parameters
  flip_lr = tf.random.uniform(shape=[], minval=0, maxval=1) > 0.5
  flip_ud = tf.random.uniform(shape=[], minval=0, maxval=1) > 0.5
  k = tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.int32)  # 0-3 for 90° rotations
  dx = tf.random.uniform(shape=[], minval=-0.1, maxval=0.1) * tf.cast(original_width, tf.float32)
  dy = tf.random.uniform(shape=[], minval=-0.1, maxval=0.1) * tf.cast(original_height, tf.float32)

  # Apply color augmentation
  img = color_augmentation(img)

  # Apply flips independently
  img = tf.cond(flip_lr, lambda: tf.image.flip_left_right(img), lambda: img)
  msk = tf.cond(flip_lr, lambda: tf.image.flip_left_right(msk), lambda: msk)
  img = tf.cond(flip_ud, lambda: tf.image.flip_up_down(img), lambda: img)
  msk = tf.cond(flip_ud, lambda: tf.image.flip_up_down(msk), lambda: msk)

  # Rotate by 90° increments
  img = tf.image.rot90(img, k=k)
  msk = tf.image.rot90(msk, k=k)

  # Translation via dynamic padding and cropping
  pad_size = tf.cast(tf.maximum(tf.abs(dx), tf.abs(dy)) + 5, tf.int32)
  dx_int = tf.cast(dx, tf.int32)
  dy_int = tf.cast(dy, tf.int32)

  # Pad - use CONSTANT for mask
  img = tf.pad(img, [[0,0], [pad_size,pad_size], [pad_size,pad_size], [0,0]], mode='REFLECT')
  msk = tf.pad(msk, [[0,0], [pad_size,pad_size], [pad_size,pad_size], [0,0]], mode='CONSTANT', constant_values=0)

  # Crop
  offset_height = pad_size + dy_int
  offset_width = pad_size + dx_int
  img = tf.image.crop_to_bounding_box(img, offset_height, offset_width, original_height, original_width)
  msk = tf.image.crop_to_bounding_box(msk, offset_height, offset_width, original_height, original_width)

  return img, msk

def generate_multiple_augmentations(img, msk, num_versions=5):
  """
  Generates multiple augmented versions of an image and mask pair.
  """
  augmented_images = []
  augmented_masks = []
  
  for _ in range(num_versions):
    aug_img, aug_msk = augmentation(img, msk)
    augmented_images.append(aug_img)
    augmented_masks.append(aug_msk)
  
  # Stack all augmented versions along the batch dimension
  stacked_images = tf.stack(augmented_images, axis=0)
  stacked_masks = tf.stack(augmented_masks, axis=0)
  
  return stacked_images, stacked_masks

class aug(tf.keras.callbacks.Callback):
  """Callback for data augmentation."""
  def __init__(self, num_versions=5):
    super(aug, self).__init__()
    self.num_versions = num_versions
    
  def on_training_batch_begin(self, batch, logs=None):
    # Apply multiple augmentations to each image in the batch
    def augment_batch(x, y):
      # Unbatch the dataset to process individual samples
      aug_images, aug_masks = generate_multiple_augmentations(x, y, self.num_versions)
      return aug_images, aug_masks
    
    # Apply augmentation to the batch
    batch = batch.map(augment_batch, num_parallel_calls=5)
    
    # Flatten the batch to get all augmented versions
    batch = batch.unbatch()
    
    # Shuffle the augmented samples
    batch = batch.shuffle(10 * self.num_versions)

def visualize_multiple_augmentations(image, mask, num_versions=5):
  """Visualize multiple augmented versions of an image and its mask."""
  # Generate multiple augmented versions
  aug_images, aug_masks = generate_multiple_augmentations(image, mask, num_versions)
  
  # Create figure with subplots
  fig, axes = plt.subplots(2, num_versions + 1, figsize=(20, 8))
  
  # Plot original image and mask
  # Handle the original image shape
  orig_img = image[0] if len(image.shape) == 4 else image
  orig_msk = mask[0] if len(mask.shape) == 4 else mask
  
  axes[0, 0].imshow(orig_img)
  axes[0, 0].set_title("Original Image")
  axes[0, 0].axis('off')
  
  axes[1, 0].imshow(tf.squeeze(orig_msk), cmap='jet')
  axes[1, 0].set_title("Original Mask")
  axes[1, 0].axis('off')
  
  # Plot augmented versions
  for i in range(num_versions):
    # Augmented image - handle the shape
    # The shape is (num_versions, batch, height, width, channels)
    # We need to extract the first batch item
    aug_img = aug_images[i, 0] if len(aug_images.shape) == 5 else aug_images[i]
    aug_msk = aug_masks[i, 0] if len(aug_masks.shape) == 5 else aug_masks[i]
    
    # Augmented image
    axes[0, i+1].imshow(aug_img)
    axes[0, i+1].set_title(f"Augmented {i+1}")
    axes[0, i+1].axis('off')
    
    # Augmented mask
    axes[1, i+1].imshow(tf.squeeze(aug_msk), cmap='jet')
    axes[1, i+1].set_title(f"Mask {i+1}")
    axes[1, i+1].axis('off')
  
  plt.tight_layout()
  plt.show()