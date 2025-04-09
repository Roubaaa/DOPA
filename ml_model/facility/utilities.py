import matplotlib.pyplot as plt
import tensorflow as tf
import os

def show_image(image, mask):
  """Visualize a member of dataset"""
  plt.figure()

  plt.subplot(1, 2, 1)
  plt.imshow(tf.keras.preprocessing.image.array_to_img(image))
  plt.axis('off')

  plt.subplot(1, 2, 2)
  plt.imshow(tf.squeeze(mask))
  plt.axis('off')

def plot_training_metrics(history, model_epochs, save_dir=None):
  """
  Plot training and validation metrics and loss from model training history.
  Saves the figures instead of displaying them.
  
  Args:
    history: Training history object
    model_epochs: Number of epochs trained
    save_dir: Directory to save the figures (default: None, uses current directory)
  """
  # Extract metrics and loss values from history
  training_acc = history.history['dice_loss']
  validation_acc = history.history['val_dice_loss']
  
  training_loss = history.history['loss']
  validation_loss = history.history['val_loss']
  
  # Create x-axis values (epochs)
  epochs = range(1, model_epochs+1)
  
  # Set save directory
  if save_dir is None:
    save_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(save_dir, 'results')
    os.makedirs(save_dir, exist_ok=True)
  
  # Plot Dice Loss metrics
  plt.figure(figsize=(8, 8))
  plt.plot(epochs, training_acc, 'bo', label='Training Metric')
  plt.plot(epochs, validation_acc, 'ro', label='Validation Metric')
  plt.title('Training and validation metrics (Dice Loss)')
  plt.legend()
  plt.xlabel('Epochs')
  plt.ylabel('Metric value')
  
  # Save the first figure
  metrics_path = os.path.join(save_dir, 'dice_loss_metrics.png')
  plt.savefig(metrics_path, dpi=300, bbox_inches='tight')
  plt.close()
  
  # Plot combined loss (BCE + Dice)
  plt.figure(figsize=(8, 8))
  plt.plot(epochs, training_loss, 'b', label='Training loss')
  plt.plot(epochs, validation_loss, 'r', label='Validation loss')
  plt.title('Training and validation loss (BCE + Dice)')
  plt.legend()
  plt.xlabel('Epochs')
  plt.ylabel('Loss value')
  
  # Save the second figure
  loss_path = os.path.join(save_dir, 'combined_loss.png')
  plt.savefig(loss_path, dpi=300, bbox_inches='tight')
  plt.close()

  return metrics_path, loss_path