import math

class DatasetSplitter:
    """Class for splitting a dataset into training and evaluation sets."""
    
    def __init__(self, data, train_pct=0.7, batch_size=16, shuffle_buffer_size=10000):
        """Initialize the DatasetSplitter with the given data and parameters."""
        self.data = data
        self.train_pct = train_pct
        self.batch_size = batch_size
        self.shuffle_buffer_size = shuffle_buffer_size
        self.full_size = sum(1 for _ in data)
        self.split = int(self.full_size * self.train_pct)
        
        self._prepare_datasets()
        self._calculate_steps()
    
    def _prepare_datasets(self):
        # Shuffle before splitting to ensure proper distribution
        shuffled_data = self.data.shuffle(
            buffer_size=self.shuffle_buffer_size,
            reshuffle_each_iteration=False
        )
        
        self.training = shuffled_data.take(self.split)
        self.evaluation = shuffled_data.skip(self.split)
        
        # Batch after splitting
        self.training = self.training.batch(self.batch_size).repeat()
        self.evaluation = self.evaluation.batch(self.batch_size)
    
    def _calculate_steps(self):
        self.TRAIN_STEPS = math.ceil(self.split / self.batch_size)
        self.EVAL_STEPS = math.ceil((self.full_size - self.split) / self.batch_size)
    
    def summary(self):
        print(f'Full size of the dataset: {self.full_size}')
        print(f'Training samples: {self.split}')
        print(f'Evaluation samples: {self.full_size - self.split}')
        print(f'Training steps/epoch: {self.TRAIN_STEPS}')
        print(f'Evaluation steps: {self.EVAL_STEPS}')