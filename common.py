import codecs
import logging

import numpy as np

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.setLevel(logging.DEBUG)


def load_binary_embeddings(embeddings_file, vocab=None, normalize=False):
    """
    Load binary word embeddings, stored in two files: a numpy binary file (.npy)
    and a vocabulary file (.vocab).
    :param embeddings_file: the embedding files prefix
    :param vocab: a limited vocabulary
    :return: the word vectors and list of words
    """
    wv = np.load(embeddings_file + '.npy')

    with codecs.open(embeddings_file + '.vocab') as f_in:
        words = [line.strip() for line in f_in]

    # Limit the vocabulary
    if vocab is not None:
        words, vectors = zip(*[(word, wv[i, :]) for i, word in enumerate(words) if word in vocab])
        wv = np.vstack(vectors)
        logger.info('Loaded {} words'.format(len(words)))

    # Normalize each row (word vector) in the matrix to sum-up to 1
    if normalize:
        row_norm = np.sum(np.abs(wv) ** 2, axis=-1) ** (1. / 2)
        wv /= row_norm[:, np.newaxis]

    return wv, words


def save_binary_embeddings(embeddings_file, wv, words):
    """
    Save binary word embeddings, stored in two files: a numpy binary file (.npy)
    and a vocabulary file (.vocab).
    :param embeddings_file: the out embedding files prefix
    :param wv: the word matrix
    :param words (list): vocabulary
    """
    np.save(embeddings_file, wv)
    with codecs.open('{}.vocab'.format(embeddings_file), 'w', 'utf-8') as f_out:
        for word in words:
            f_out.write(word + '\n')
