import matplotlib.pyplot as plt
import torch


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


if __name__ == '__main__':
    names = get_names_list()
    print(names)
    pass
