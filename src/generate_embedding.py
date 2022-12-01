import pandas as pd
import numpy as np
import tensorflow as tf
from keras import backend as K
from tensorflow.keras.models import Model


protein_encoding = {
    "A": "0",
    "B": "19",
    "C": "1",
    "D": "2",
    "E": "3",
    "F": "4",
    "G": "5",
    "H": "6",
    "I": "7",
    "J": "19",
    "K": "8",
    "L": "9",
    "M": "10",
    "N": "11",
    "O": "19",
    "P": "12",
    "Q": "13",
    "R": "14",
    "S": "15",
    "T": "16",
    "U": "19",
    "V": "17",
    "W": "18",
    "X": "19",
    "Y": "20",
    "Z": "21"
}



def encode_seq(line):
    length = len(line)
    encoded = []
    for i in range(0, length):
        encoded.append(int(protein_encoding[line[i]]))
    while length < 2000:
        encoded.append(22)
        length += 1
    return encoded

def generate_embedding(encdoded, lv_layer):
    emb = []
    for i in range(len(encoded)):
        tmp_encode = encoded[i].reshape(1, encoded[i].shape[0])
        feature_vector = lv_layer(tmp_encode)
        feature_vector = feature_vector.numpy()[0]
        t = []
        t.append(gene_names[i])
        for j in range(len(feature_vector)):
            t.append(feature_vector[j])
        emb.append(t)
    
    embedding_df = pd.DataFrame(emb)
    
    # Saving human genes embedding
    embedding_df.to_csv("output/Embedding_human_proteins.csv", index=False)



# Loading all human genes names and sequences
proteins = pd.read_csv("data/gene_names_with_sequences.csv")
gene_names = proteins['Gene_name'].tolist()
protein_sequences = proteins['Protein_sequence'].tolist()

encoded = []
encoded_idx = []

for i in range(len(protein_sequences)):
    # The autoencoder was built to have a gene sequence maximum length of 2000 amino acids
    
    if(len(protein_sequences[i]) <=2000):
        encoded.append(encode_seq(str(protein_sequences[i])))
    elif(len(protein_sequences[i]) > 2000):
        encoded.append(encode_seq(str(protein_sequences[i][:2000])))

## Load the trained autoencoder ###
autoencoder = tf.keras.models.load_model('proae.hdf5')

encoded = np.array(encoded)

## use the latent space layer in order to retrieve embeddings of each input
lv_layer = tf.keras.Model(inputs=autoencoder.input,
                          outputs=autoencoder.get_layer('latent_vector').output)

generate_embedding(encdoded, lv_layer)
