from keras.models import load_model
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, Embedding, Masking
from keras.optimizers import Adam
from keras.utils import Sequence
from keras.preprocessing.text import Tokenizer

from sklearn.utils import shuffle

from IPython.display import HTML

from itertools import chain
from keras.utils import plot_model
import numpy as np
import pandas as pd
import random
import json
import re
from keras.preprocessing.text import Tokenizer
RANDOM_STATE = 50
TRAIN_FRACTION = 0.7



            
def make_sequences(texts,
                   training_length=50,
                   lower=True,
                   filters='#$%&*+/<=>@[\\]^_`{|}~\t', target=0):
    """Turn a set of texts into sequences of integers"""
    # Create the tokenizer object and train on texts
    tokenizer = Tokenizer(lower=lower, filters=filters)
    tokenizer.fit_on_texts(texts)

    # Create look-up dictionaries and reverse look-ups
    word_idx = tokenizer.word_index
    idx_word = tokenizer.index_word
    num_words = len(word_idx) + 1
    word_counts = tokenizer.word_counts

    print("dictionary size: ")
    print(num_words)

    # Convert text to sequences of integers
    sequences = []
    sequence = tokenizer.texts_to_sequences(texts)[target]
    sequences.append(sequence)
    #print(len(sequences))
    #print(len(sequence))
    # Limit to sequences with more than training length tokens
    seq_lengths = [len(x) for x in sequences]
    over_idx = [
        i for i, l in enumerate(seq_lengths) if l > (training_length + 20)
    ]

    new_texts = []
    new_sequences = []

    # Only keep sequences with more than training length tokens
    for i in over_idx:
        new_texts.append(texts[i])
        new_sequences.append(sequences[i])

    training_seq = []
    labels = []

    # Iterate through the sequences of tokens
    for seq in new_sequences:

        # Create multiple training examples from each sequence
        for i in range(training_length, len(seq)):
            # Extract the features and label
            extract = seq[i - training_length:i + 1]

            # Set the features and label
            training_seq.append(extract[:-1])
            labels.append(extract[-1])

    print("trainingseqLength: ")
    print(len(training_seq))

    # Return everything needed for setting up the model
    return word_idx, idx_word, num_words, word_counts, new_texts, new_sequences, training_seq, labels



def format_text(text):
    """Add spaces around punctuation and remove references to images/citations."""
    text = re.sub(r'\n ?\n', '\n', text)
    text = re.sub(r'\n ?\n', '\n', text)
    text = re.sub(r'\n ?\n', '\n', text)
    text = re.sub(r'\n ?\n', '\n', text)
    
    
    text = re.sub(r"(\B'|'\B)", " ' ", text)
    text = re.sub(r'\n', ' \n ', text)
    
    text = re.sub(r'\r', '', text)
    
    text = re.sub(r'—', '--', text)
    text = re.sub(r'--', ' -- ', text)
    text = re.sub(r'!"', '! "', text)
    text = re.sub(r'\.\.\.', ' ...', text)
    
    
    text = re.sub(r'\(', '( ', text)
    text = re.sub(r'(?<=[^\s0-9])(?=[.)"(,;!?:])', r' ', text)
    text = re.sub(r'"', ' " ', text)
    text = re.sub(r'  ', ' ', text)
    
    return text

def remove_spaces(patent):
    """Remove spaces around punctuation"""
    patent = re.sub(r'\s+([.,;?!)])', r'\1', patent)
    patent = re.sub(r'\( ', r'(', patent)
    return patent



    
    
    
def create_train_valid(features, labels, num_words, train_fraction=TRAIN_FRACTION):
    """Create training and validation features and labels."""

    # Randomly shuffle features and labels
    features, labels = shuffle(features, labels, random_state=RANDOM_STATE)

    # Decide on number of samples for training
    train_end = int(train_fraction * len(labels))

    train_features = np.array(features[:train_end])
    valid_features = np.array(features[train_end:])

    train_labels = labels[:train_end]
    valid_labels = labels[train_end:]

    # Convert to arrays
    X_train, X_valid = np.array(train_features), np.array(valid_features)

    # Using int8 for memory savings
    y_train = np.zeros((len(train_labels), num_words), dtype=np.int8)
    y_valid = np.zeros((len(valid_labels), num_words), dtype=np.int8)

    # One hot encoding of labels
    for example_index, word_index in enumerate(train_labels):
        y_train[example_index, word_index] = 1

    for example_index, word_index in enumerate(valid_labels):
        y_valid[example_index, word_index] = 1

    # Memory management
    import gc
    gc.enable()
    del features, labels, train_features, valid_features, train_labels, valid_labels
    gc.collect()

    return X_train, X_valid, y_train, y_valid