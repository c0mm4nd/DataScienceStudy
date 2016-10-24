from sklearn.svm import SVC
import numpy as np


class SVMClassifier:

    def __init__(self, train_data, train_labels, best_words, C):
        train_data = np.array(train_data)
        train_labels = np.array(train_labels)
        self.best_words = best_words
        self.clf = SVC(C=C)  # clf => classifier
        self.__train(train_data, train_labels)

    def words2vector(self, all_data):
        vectors = []
        for data in all_data:
            vector = []
            for feature in self.best_words:
                vector.append(data.count(feature))
            vectors.append(vector)
        vectors = np.array(vectors)
        return vectors

    def __train(self, train_data, train_labels):
        print("SVMClassifier is training ...... ")
        train_vectors = self.words2vector(train_data)
        self.clf.fit(train_vectors, np.array(train_labels))
        print("SVMClassifier trains over!")

    def classify(self, data):
        vector = self.words2vector([data])
        prediction = self.clf.predict(vector)
        return prediction[0]
