import tensorflow as tf
import pandas as pd
import pickle
import sys

from numpy import load
import warnings
import numpy as np
#from IPython.core.interactiveshell import InteractiveShell
from app.utils_2 import format_text, remove_spaces#, make_sequences, create_train_valid
from tensorflow.keras.models import Sequential, load_model
import os
from app import APP_STATIC

idx_word = load(os.path.join(APP_STATIC, 'dictionaries/idx_word.npy'), allow_pickle=True).tolist()

titles=[]
    
def load_and_evaluate(model_dir1, model_name, return_model=False):
    model = load_model('{}/{}.h5'.format(model_dir1 ,model_name))
    if return_model:
        return model
        
def stringToInts(input1):
    input2 = format_text(input1)
    array = input2.split(' ')
    #print(array)
    output = []
    for word in array:
        found = False
        for x, y in idx_word.items():
            if y == word:
                output.append(x)
                found=True
                break
        if not found:        
            print(str(word) + " not found in dict")
    return output
    
def generate_poem(poemData):
    models=[]
    print(poemData)
    seed = poemData["seed"].lower()
    genLength = numWords=poemData["numWords"]
    author = poemData["poet"]
    # Set up IPython to show all outputs from a cell
    #InteractiveShell.ast_node_interactivity = 'all'
    
   

    #model_name = 'whitman'
    model_dir = os.path.join(APP_STATIC, 'models')
    
    print("importing models: ")
    for file in os.listdir(model_dir):
        if file.endswith(".h5"):
            titles.append(file[:-3])
            print(os.path.join(model_dir, file))
            if file[:-3] == author:
                print("!!!" + author +"!!!")
                model = load_and_evaluate(model_dir, file[:-3], return_model=True)
                models.append(model)
    titles
    len(models)
    

    output = mesh_authors(models, 0, 0, seed, new_words=int(genLength),diversity=1,auth1WEIGHT=1, auth=author)
    print(output)
    
    del models
    return output
    
    
    
def alliterate(word, prevWords):
    for otherword in prevWords:
        if word[0] == otherword[0]:
            return 1
    return 0

def rhymeswith(word, prevWords):
    return 0

def mesh_authors(model, author1, author2, 
                    sequences,
                    training_length=50,
                    new_words=100,
                    diversity=1,
                    return_output=False,
                    n_gen=1, auth1WEIGHT = .5, auth=""):

    gen_list = []
    output_text = []
    print("generating output from " + titles[author1]+" and "+ titles[author2])
    for n in range(n_gen):
        # Extract the seed sequence
        seed = stringToInts(sequences)
        comprehended_words=[]
        for i in seed:
            comprehended_words.append(idx_word.get(i, ''))
        
        generated = seed[:] + ['#']
        # Find the actual entire sequence
        actual = generated[:]
        output = []

        # Keep adding new words
        for i in range(new_words):
            
            # predict next word for author 1
            pred1 = model[author1].predict(np.array(seed).reshape(1, -1))[0].astype(
                np.float64)
            # predict next word for author 2
            pred2 = model[author2].predict(np.array(seed).reshape(1, -1))[0].astype(
                np.float64)
            
                
            # Diversify
            pred1 = np.log(pred1) / diversity
            exp_preds = np.exp(pred1)
            # Softmax
            pred1 = exp_preds / sum(exp_preds)

            pred2 = np.log(pred2) / diversity
            exp_preds = np.exp(pred2)
            # Softmax
            pred2 = exp_preds / sum(exp_preds)
            
            
            
            #combine probability vectors
            pred1 = pred1 * auth1WEIGHT
            pred2 = pred2 * (1-auth1WEIGHT)
            
            preds = pred1 + pred2
            idx_word[1]
            preds[1] *=200; #up probability of \n for effect
            for pos in range(1,len(idx_word)):
                word = idx_word[pos]
                if rhymeswith(word, output_text[-40:]):
                    preds[pos] *=1;
            
                if auth == 'seuss' and alliterate(word, output_text[-2:]):
                    preds[pos] *=4;
            preds=preds/np.sum(preds)
            
            # Choose the next word
            probas = np.random.multinomial(1, preds, 1)[0]
            next_idx = np.argmax(probas)

            # New seed adds on old word
            seed = seed[1:] + [next_idx]
            generated.append(next_idx)
            output.append(next_idx)
            output_text.append(idx_word.get(next_idx, ''))
        # Showing generated and actual abstract
        
           
            
    return remove_spaces(' '.join(output_text))

    

