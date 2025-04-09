import os
from data import WellpadDataset
from utilities import show_image, plot_training_metrics
from datasplitter import DatasetSplitter
from unet import UNet
from datetime import date
from augmentation import aug, visualize_multiple_augmentations
from keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger

# Today's date.
today = str(date.today())
dir = 'C:/Users/User/OneDrive/ML'  # Link to the directory containing the images: https://1drv.ms/f/c/774cc792b602f58c/EhsIOD--_rRDhUISOW_uS2YBk02ZGYbITX2jVrkO_GCZZw?e=LTYRdB

# Create results directory if it doesn't exist
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_result = os.path.join(base_dir, 'results')
os.makedirs(dir_result, exist_ok=True)

files = os.listdir(dir) 
files = [f'{dir}/{fn}' for fn in files]
data = WellpadDataset().get(files).shuffle(5000)
splitter = DatasetSplitter(data)
splitter.summary()

# Usage:
unet = UNet()
unet.summary()
unet.plot_model()

# View an Image and Mask
# NOTE: Some images do not contain a 
"""
for img, msk in data.take(1):
  show_image(img,msk)
"""
# Visualize Augmentation
test_batch = splitter.evaluation.take(1)
original_image, original_mask = next(iter(test_batch.take(1)))
visualize_multiple_augmentations(original_image, original_mask, num_versions=5)

# Callback for CSV logging
csv_logger = CSVLogger(f'{dir_result}/{today}_metrics.csv', separator=',', append=False)

# Callback for saving the best model
save_model_path = f'{dir_result}/{today}_wellpad_model_.keras'
model_checkpoint = ModelCheckpoint(
    filepath=save_model_path,
    monitor='val_loss',
    mode='min',
    save_best_only=True
)

early_stopping = EarlyStopping(
    monitor='val_loss',        
    patience=30,               
    restore_best_weights=True  
)
# Set number of epochs
model_epochs = 100

history = unet.model.fit(
    x = splitter.training,
    epochs = model_epochs,
    steps_per_epoch = splitter.TRAIN_STEPS,
    validation_data = splitter.evaluation,
    validation_steps = splitter.EVAL_STEPS,
    callbacks = [aug(),model_checkpoint, csv_logger, early_stopping])

plot_training_metrics(history, model_epochs, save_dir=dir_result)

# Get the final accuracy for training and validation
overall_training_accuracy = history.history['accuracy'][-1]
overall_validation_accuracy = history.history['val_accuracy'][-1]

# Print the overall accuracy
print(f"Overall Training Accuracy: {overall_training_accuracy}")
print(f"Overall Validation Accuracy: {overall_validation_accuracy}")