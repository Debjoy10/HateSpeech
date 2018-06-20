import re
import os
import random
import tarfile
import codecs
from torchtext import data
SEED = 1

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


class ED(data.Dataset):

    @staticmethod
    def sort_key(ex):
        return len(ex.text)

    def __init__(self, text_field, label_field, id_field, path=None, examples=None, **kwargs):
        """Create an Emotion Dataset instance given a path and fields.
        Arguments:
            text_field: The field that will be used for text data.
            label_field: The field that will be used for label data.
            path: Path to the data file.
            examples: The examples contain all the data.
            Remaining keyword arguments: Passed to the constructor of
                data.Dataset.
        """
        # text_field.preprocessing = data.Pipeline(clean_str)
        fields = [('text', text_field), ('label', label_field), ('id', id_field)]
        if examples is None:
            path = self.dirname if path is None else path
            examples = []
            with codecs.open(os.path.join(path, 'captions.amusement'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'amusement', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.anger'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'anger', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.awe'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'awe', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.contentment'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'contentment', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.disgust'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'disgust', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.excitement'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'excitement', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.fear'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'fear', line.split(',')[0]], fields) for line in f]
            with codecs.open(os.path.join(path, 'captions.sadness'),'r','utf8') as f:
                examples += [
                    data.Example.fromlist([line.split(',',1)[1], 'sadness', line.split(',')[0]], fields) for line in f]
        super(ED, self).__init__(examples, fields, **kwargs)

    @classmethod
    def splits(cls, text_field, label_field, id_field, shuffle=True ,root='.',path="../../datasets/EmotionDataset/lstm_data/noisy/", **kwargs):
        """Create dataset objects for splits of the MR dataset.
        Arguments:
            text_field: The field that will be used for the sentence.
            label_field: The field that will be used for label data.
            dev_ratio: The ratio that will be used to get split validation dataset.
            shuffle: Whether to shuffle the data before split.
            root: The root directory that the dataset's zip archive will be
                expanded into; therefore the directory in whose trees
                subdirectory the data files will be stored.
            train: The filename of the train data. Default: 'train.txt'.
            Remaining keyword arguments: Passed to the splits method of
                Dataset.
        """
        examples = cls(text_field, label_field, id_field, path=path, **kwargs).examples
        dev_examples = []
        random.shuffle(examples)

        print('train:',len(examples),'dev:',len(dev_examples)) #,'test:',len(test_examples))
        return cls(text_field, label_field, id_field, examples=examples), cls(text_field, label_field, id_field, examples=dev_examples)
                #cls(text_field, label_field, examples=test_examples),)

# load ED dataset
def load_ed(text_field, label_field, id_field, batch_size):
    print('loading data')
    train_data, dev_data = ED.splits(text_field, label_field, id_field)
    text_field.build_vocab(train_data, dev_data)
    label_field.build_vocab(train_data, dev_data)
    id_field.build_vocab(train_data, dev_data)

    # print('building batches')
    # train_iter, dev_iter = data.Iterator.splits(
    #     (train_data, dev_data), batch_sizes=(batch_size, len(dev_data)),repeat=False, shuffle=False,
    #     device = -1

    print('building batches')
    train_iter, dev_iter = data.Iterator.splits(
        (train_data, dev_data), batch_sizes=(batch_size, batch_size),repeat=False, shuffle=False,
        device = -1
    )

    return train_iter #, test_iter
#
# text_field = data.Field(lower=True)
# label_field = data.Field(sequential=False)
# train_iter, dev_iter , test_iter = load_mr(text_field, label_field, batch_size=50)
