# CS331 Sentiment Analysis Assignment 3
# This file contains the processing functions
import string
import classifier
import csv

def process_text(text):
    text = text.lower()
    preprocessed_text = ""

    for i in text:
        # only space and 0 and 1, and letters are allowed
        if ord(i) in range(97, 123) or ord(i) in (32, 48 , 49):
            preprocessed_text += i
        else:
            preprocessed_text += ""
    preprocessed_text = preprocessed_text.split()

    return preprocessed_text


def build_vocab(preprocessed_text):
    words = []
    for sentence in preprocessed_text:
        words.extend(sentence)
    unique_words = set(words)
    vocab = list(unique_words)
    vocab.sort()
    vocab = vocab[2:]
    return vocab


def vectorize_text(text_with_labels, vocab):

    word_index = {word: i for i, word in enumerate(vocab)}
    vectorized_text = []
    labels = []
    with open('result.txt', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(vocab + ["Class Label"])  # Write headers

        for sentence in text_with_labels:
            vector = [0] * len(vocab)
            for word in sentence[:-1]: 
                if word in word_index:
                    vector[word_index[word]] = 1
            
            vector.append(int(sentence[-1]))  # Add the label to the vector
            writer.writerow(vector)
            vectorized_text.append(vector[:-1])
            labels.append(int(sentence[-1]))  

    return vectorized_text, labels





def accuracy(predicted_labels, true_labels):
    """
    predicted_labels: list of 0/1s predicted by classifier
    true_labels: list of 0/1s from text file
    return the accuracy of the predictions
    """
    correct_predictions = sum(p == t for p, t in zip(predicted_labels, true_labels))

    total_predictions = len(predicted_labels)
    accuracy_score = correct_predictions / total_predictions
    return accuracy_score


def test(raw_train_data, raw_test_data):
    preprocessed_train_data = [process_text(text) for text in raw_train_data]
    preprocessed_test_data = [process_text(text) for text in raw_test_data]
    # Build the vocabulary from the training data
    vocab = build_vocab(preprocessed_train_data)
    # print (vocab)
    # Vectorize the training and test data
    # print(preprocessed_train_data)
    train_data, train_labels = vectorize_text(preprocessed_train_data, vocab)
    # print (train_data)
    # print (train_labels)
    test_data, test_labels = vectorize_text(preprocessed_test_data, vocab)
    # # # Initialize and train the classifier
    classifier_set = classifier.BayesClassifier()
    classifier_set.train(train_data, train_labels, vocab)
    # # # Classify the test data and calculate the accuracy
    predicted_labels = classifier_set.classify_text(test_data, vocab)
    test_accuracy = accuracy(predicted_labels, test_labels)

    # # Print the test accuracy
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")

def main():
    # Load the training and test data
    with open("trainingSet.txt", "r") as file:
        og_raw_train_data = file.readlines()
        # part = len(raw_train_data) // 1 
        # raw_train_data = raw_train_data[:part]  
    with open("testSet.txt", "r") as file:
        og_raw_test_data = file.readlines()

    # Preprocess the training and test data
    print("\n\nResults #1: \ntraining: trainingSet.txt"+
           "\ntesting: trainingSet.txt")
    for i in range(4,0,-1):
        part = len(og_raw_train_data) // i
        raw_train_data = og_raw_train_data[:part]
        test(raw_train_data, og_raw_train_data)

    print("\n\nResults #2: \ntraining: trainingSet.txt"+
           "\ntesting: testSet.txt")
    for i in range(4,0,-1):
        part = len(og_raw_train_data) // i
        raw_train_data = og_raw_train_data[:part]
        test(raw_train_data, og_raw_test_data)






    # For incremental learning, you might need to split your train_data and train_labels into chunks
    # and then call the train function on each chunk before testing the model

    # The final results should be saved in results.txt as specified in your instructions

if __name__ == "__main__":
    main()
