# CS331 Sentiment Analysis Assignment 3
# This file contains the processing functions
import string

def process_text(text):
    text = text.lower()
    preprocessed_text = ""

    for i in text:
        if ord(i) in range(97, 123) or ord(i) in (32, 48 , 49):
            preprocessed_text += i
        else:
            preprocessed_text += ""
    preprocessed_text = preprocessed_text.split()
    return preprocessed_text


def build_vocab(preprocessed_text):
    """
    Builds the vocab from the preprocessed text
    preprocessed_text: output from process_text
    Returns unique text tokens
    """
    # Flatten the list of sentences into a list of words
    words = [word for sentence in preprocessed_text for word in sentence]

    # Get unique words
    vocab = list(set(words))

    # Sort the vocabulary
    vocab.sort()

    return vocab



def vectorize_text(text_with_labels, vocab):
    """
    Converts the text into vectors
    text_with_labels: preprocess_text from process_text. Each element is a list of words, with the last element being the label.
    vocab: vocab from build_vocab
    Returns the vectorized text and the labels
    """

    # Create a dictionary that will hold the index of each word in the vocabulary
    word_index = {word: i for i, word in enumerate(vocab)}

    # Initialize an empty list that will hold our vectorized sentences and labels
    vectorized_text = []
    labels = []

    # Iterate over each sentence in the text
    for sentence in text_with_labels:

        # Initialize a vector for this sentence with zeros
        vector = [0] * len(vocab)

        # Iterate over each word in the sentence
        for word in sentence[:-1]:  # Exclude the last item, which is the label

            # If the word is in our vocabulary, set the corresponding position in the vector to 1
            if word in word_index:
                vector[word_index[word]] = 1

        # Add the vector and label to our lists
        vectorized_text.append(vector)
        labels.append(int(sentence[-1]))  # The last item is the label

    return vectorized_text, labels




# def accuracy(predicted_labels, true_labels):
#     """
#     predicted_labels: list of 0/1s predicted by classifier
#     true_labels: list of 0/1s from text file
#     return the accuracy of the predictions
#     """

#     return accuracy_score


def main():
    # Load the training and test data
    with open("trainingSet_test.txt", "r") as file:
        raw_train_data = file.readlines()

    with open("testSet.txt", "r") as file:
        raw_test_data = file.readlines()

    # Preprocess the training and test data
    preprocessed_train_data = [process_text(text) for text in raw_train_data]
    preprocessed_test_data = [process_text(text) for text in raw_test_data]

    # Build the vocabulary from the training data
    vocab = build_vocab(preprocessed_train_data)
    # print (vocab)

    # Vectorize the training and test data
    # print(preprocessed_train_data)

    train_data, train_labels = vectorize_text(preprocessed_train_data, vocab)

    print (train_data)
    
    print (train_labels)
    test_data, test_labels = vectorize_text(preprocessed_test_data, vocab)




    # # # Initialize and train the classifier
    # # classifier = BayesClassifier()
    # # classifier.train(train_data, train_labels, vocab)

    # # # Classify the test data and calculate the accuracy
    # # predicted_labels = classifier.classify_text(test_data, vocab)
    # # test_accuracy = accuracy(predicted_labels, test_labels)

    # # # Print the test accuracy
    # # print(f"Test Accuracy: {test_accuracy*100:.2f}%")






    # For incremental learning, you might need to split your train_data and train_labels into chunks
    # and then call the train function on each chunk before testing the model

    # The final results should be saved in results.txt as specified in your instructions

if __name__ == "__main__":
    main()
