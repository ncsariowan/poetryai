from app.utils_2 import format_text, remove_spaces
from numpy import load
import pandas as pd
import tensorflow as tf
import keras
import pickle
import sys
import warnings
import numpy as np
from keras.models import Sequential, load_model
import os
from app import APP_STATIC

# poemData = {
#         "seed": seed,
#         "numWords": numWords,
#         "author": author
#     }

model_dir = ''

model_name = os.path.join(APP_STATIC, 'testModel3')


def generate_poem(poemData):
    print(poemData)

    idx_word = load(os.path.join(APP_STATIC, 'idx_word.npy'),
                    allow_pickle=True).tolist()


    model_name = os.path.join(APP_STATIC, 'testModel3')

    model = load_and_evaluate(model_name, return_model=True)

    string = generate_output(
        model, poemData["seed"], 10, new_words=poemData["numWords"], diversity=1)

    return string


def load_and_evaluate(model_name, return_model=False):
    """Load in a trained model and evaluate with log loss and accuracy"""

    model = load_model('{}{}.h5'.format(model_dir, model_name))
    #r = model.evaluate(X_valid, y_valid, batch_size=2048, verbose=1)

    #valid_crossentropy = r[0]
    #valid_accuracy = r[1]

    #print('Cross Entropy: {}'.format(round(valid_crossentropy, 4)))
    #print('Accuracy: {}%'.format(round(100 * valid_accuracy, 2)))

    if return_model:
        return model


def stringToInts(input1):
    input2 = format_text(input1)
    array = input2.split(' ')
    print(array)
    output = []
    for word in array:
        found = False
        for x, y in idx_word.items():
            if y == word:
                output.append(x)
                found = True
                break
        if not found:
            print(str(word) + " not found in dict")
    return output


def generate_output(model,
                    sequences,
                    training_length=50,
                    new_words=100,
                    diversity=1,
                    return_output=False,
                    n_gen=1):
    """Generate `new_words` words of output from a trained model and format into HTML."""

    # Choose a random sequence
    #seq = random.choice(sequences)

    # Choose a random starting point
    seed_idx = 3  # random.randint(0, len(seq) - training_length - 1)
    # Ending index for seed
    end_idx = seed_idx + training_length

    gen_list = []

    for n in range(n_gen):
        # Extract the seed sequence
        seed = stringToInts(sequences)
        # seed = [6,179,7,3,230,326,13,2]#,1589,1,247,1,3,109,134,16,1,2,3,73,681,1426,134,16,1,1590,4682,6,4683,13,2,396,6,1179,20,2845,1,6,84,67,2845,1,2,396,6,4684,49,59,1,3556]
        n2 = []
        for i in seed:
            n2.append(idx_word.get(i, '< --- >'))

        # seq[seed_idx:end_idx]
        #original_sequence = [idx_word[i] for i in seed]
        generated = seed[:] + ['#']

        # Find the actual entire sequence
        actual = generated[:]
        output = []
        # Keep adding new words
        for i in range(new_words):

            # Make a prediction from the seed
            preds = model.predict(np.array(seed).reshape(1, -1))[0].astype(
                np.float64)

            # Diversify
            preds = np.log(preds) / diversity
            exp_preds = np.exp(preds)

            # Softmax
            preds = exp_preds / sum(exp_preds)

            # Choose the next word
            probas = np.random.multinomial(1, preds, 1)[0]

            next_idx = np.argmax(probas)

            # New seed adds on old word
            seed = seed[1:] + [next_idx]
            generated.append(next_idx)
            output.append(next_idx)

        # Showing generated and actual abstract
        n = []

        for i in output:
            n.append(idx_word.get(i, '< --- >'))

        gen_list.append(n)
        # print(gen_list)

        print("original")
        print(remove_spaces(' '.join(n2)))
        print("continuation:")
        print(n)

    a = []

    gen_list = [
        gen[training_length:training_length + len(a)] for gen in gen_list
    ]

    return remove_spaces(' '.join(n))
