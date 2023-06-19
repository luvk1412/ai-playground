import string

import matplotlib.pyplot as plt
import torch

default_stoi = {ch: i + 1 for i, ch in enumerate(string.ascii_lowercase)}
default_stoi['.'] = 0
default_itos = {v: k for k, v in default_stoi.items()}


def get_names_list():
    with open("names.txt", 'r') as f:
        return f.read().splitlines()


def get_bigrams(words):
    b = {}
    for word in words[:1]:
        words_chars = ['.'] + list(word) + ['.']
        for ch1, ch2 in zip(words_chars, words_chars[1:]):
            bigram = (ch1, ch2)
            b[bigram] = b.get(bigram, 0) + 1


def train_val_test_split(X, Y, train_percent, val_percent):
    n = len(X)
    train_len = int((train_percent / 100.0) * n)
    val_len = int(((train_percent + val_percent) / 100.0) * n)
    return X[:train_len], Y[:train_len], X[train_len:val_len], Y[train_len:val_len], X[val_len:], Y[val_len:]


def get_ngram_dataset(words, stoi=default_stoi, block_size=1):
    xs, ys = [], []
    for word in words:
        context = [0] * block_size
        for ch in word + '.':
            xs.append(context[0] if block_size == 1 else context)
            ys.append(stoi[ch])
            context = context[1:] + [stoi[ch]]
    return torch.tensor(xs), torch.tensor(ys)


if __name__ == '__main__':
    names = get_names_list()
    print(get_bigrams_dataset(words=names)[1].shape)
    pass
