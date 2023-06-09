# This file implements a Naive Bayes Classifier
import math

class BayesClassifier():
    """
    Naive Bayes Classifier
    file length: file length of training file
    sections: sections for incremental training
    """
    def __init__(self):
        self.positive_word_counts = {}
        self.negative_word_counts = {}
        self.percent_positive_sentences = 0
        self.percent_negative_sentences = 0
        self.file_length = 499
        self.file_sections = [self.file_length // 4, self.file_length // 3, self.file_length // 2]


    def train(self, train_data, train_labels, vocab):
        """
        This function builds the word counts and sentence percentages used for classify_text
        train_data: vectorized text
        train_labels: vectorized labels
        vocab: vocab from build_vocab
        """

        total_sentences = len(train_labels)
        positive_sentences = sum(train_labels)
        self.percent_positive_sentences = positive_sentences / total_sentences
        self.percent_negative_sentences = 1 - self.percent_positive_sentences

        self.positive_word_counts = dict.fromkeys(vocab, 0)
        self.negative_word_counts = dict.fromkeys(vocab, 0)


        for i in range(total_sentences):
            for j, word in enumerate(vocab):
                if train_labels[i] == 1:
                    self.positive_word_counts[word] += train_data[i][j]
                else:
                    self.negative_word_counts[word] += train_data[i][j]
        return 1
    

    def classify_text(self, vectors, vocab):
            predictions = []
            # print(self.negative_word_counts)
            # print(self.positive_word_counts)
            for vector in vectors:

                log_prob_positive = math.log(self.percent_positive_sentences)
                log_prob_negative = math.log(self.percent_negative_sentences)

                num_vocab = len(vocab)
                self.delete_zero_keys(self.negative_word_counts)
                self.delete_zero_keys(self.positive_word_counts)
                for i in range(len(vector)):
                    
                    if vector[i] == 1: # The word is present
                        word = vocab[i]
                        if self.positive_word_counts.get(word, 0) == 0:

                            log_prob_positive += math.log(1/(num_vocab+ self.percent_positive_sentences* self.file_length))
                        else:
                            log_prob_positive += math.log(self.positive_word_counts.get(word, 0)/len(self.positive_word_counts))
                         
                        if self.negative_word_counts.get(word, 0) == 0:
                            log_prob_negative += math.log(1/(num_vocab + self.percent_negative_sentences* self.file_length))
                        else:
                            log_prob_negative += math.log(self.negative_word_counts.get(word, 0)/len(self.negative_word_counts))
                        
                if log_prob_positive > log_prob_negative:
                    predictions.append(1) 
                else:
                    predictions.append(0)
            return predictions
    

    def delete_zero_keys(self, dictionary):
        keys_to_delete = [key for key, value in dictionary.items() if value == 0]
        
        for key in keys_to_delete:
            del dictionary[key]