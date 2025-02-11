import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

### PLOT PARAMETERS
figure(figsize=(15, 6), dpi=120)
PLOTTITEL = "Wahrscheinlichkeitsverteilung der DTAG Funktionalen Anforderungen <--> CIS-Anforderung:\n"
YLABEL = "Wahrscheinlichkeit"
XLABEL = "DTAG Funktionale Anforderung"

### READ DATA from CSV
df = pd.read_csv("BigDataTemplate4.txt", names=['CIS-Req', 'label'], sep='\t')
cis_requirements = df['CIS-Req'].values
funktionale_requirements = df['label'].values

# Wie viele CIS_Reqs sind den Funktionalen jeweils zugeordnet? :
# print("label\tcount")
# print(df['label'].value_counts())


### MEINE TESTDATEN
list_X = ["Heute ist das Wetter nicht gut", "Heute ist das Wetter gut", "Heute das Wetter ist nicht gut",
          "Das Wetter ist heute gut", "Kopfschmerzen sind schlimm!", "Heute habe ich Kopfschmerzen wegen dem Wetter"]
list_Y = ["0", "1", "0", "1", "Kopfschmerzen",
          "Kopfschmerzen"]  # 0 --> schlechtes Wetter, 1 --> gutes Wetter, 3 --> Kopfschmerzen

### global verfügbare Objekte
VECTORIZER = CountVectorizer(max_df=0.25, ngram_range=(1,1))  # Muss global verfügbar sein # FEATURE ENGINEERING DURCH PARAMETER
# CLASSIFIER = SVC()
# CLASSIFIER = LogisticRegression()
CLASSIFIER = RandomForestClassifier()
# CLASSIFIER = GradientBoostingClassifier()


def prepare_trainingsdata(cis_list, funktional_list):
    """
    Die Funktion macht das preprocessing mit der Hilfe von X und Y Liste. Zurückgegeben werden Daten die der Classifier versteht
    :param cis_list: Die X-Werte --> example: ["Ensure mounting of df is disabled", "No ssh root must be used", "Dont use lorem ipsum", ...]
    :param funktional_list: Die zugehörigen Y-Werte sind die Label: example: [0, 1, 0, 1, 2, 2]
    :return: cis_requirement_vectorized --> scipy.sparse.csr.csr_matrix
    :return: funktional_list            --> eigentlich unnötig
    :return: vectorizer                 --> der verwendete CountVectorizer. --> WICHTIG: Man muss immer den selben Count Vectorizer verwenden
    """
    VECTORIZER.fit(cis_list)
    cis_requirement_vectorized = VECTORIZER.transform(cis_list)
    return cis_requirement_vectorized, funktional_list


def predict_funktionale_Anforderung(neuer_y_string):
    """
    Funktion bestimmt das zugehörige Label. Sie verwendet den globalen Vectorizer und den übergebenen classifier.
    :param neuer_y_string: Ein String zu dem das Label gefunden werden soll
    :param classifier: Der verwendete Classifier
    :return: Gibt den Wert des Labels zurück
    """
    X_test = VECTORIZER.transform([neuer_y_string])
    predicted_label = CLASSIFIER.predict(X_test)
    print("[+] " + neuer_y_string + "\t\t-->\t\t" + str(predicted_label[0]))
    return predicted_label[0]


def print_mapping(X, Y, filter):
    '''
    Gibt das Mapping von X und Y in Konsole aus. Mit filter auf "no" wird alles ausgegeben
    :param X: CIS_Requirement
    :param Y: funktionale
    :param filter: "no" --> alles, int --> filtert Y
    :return: None
    '''
    for i in range(0, len(X)):
        if filter == "no":
            print(X[i] + "\t\t-->\t\t" + str(Y[i]))
            continue
        if Y[i] == filter:
            print(X[i] + "\t\t-->\t\t" + str(Y[i]))


def save_persistent_model(pickle_file_name):
    with open(pickle_file_name, "wb") as file:
        pickle.dump(CLASSIFIER, file, protocol=pickle.HIGHEST_PROTOCOL)


def use_persistent_model(pickle_file_name):
    with open(pickle_file_name, 'rb') as handle:
        classifier_from_pickle = pickle.load(handle)
    return classifier_from_pickle


def get_prediction_probability_for_sample(sample):
    X_test = VECTORIZER.transform([sample])
    prediction_probability = CLASSIFIER.predict_proba(X_test)
    return prediction_probability[0]


def get_probability_plot(values, testdata_x):
    names = ["N/A"]
    for i in range(1, 35):
        names.append("f" + str(i))

    plt.bar(names, values)
    plt.title(PLOTTITEL + testdata_x)
    plt.ylabel(YLABEL)
    plt.xlabel(XLABEL)
    plt.show()


### TRAINING DES MODELLS
# CLASSIFIER = use_persistent_model("test1.pickle")
X, Y = prepare_trainingsdata(cis_requirements, funktionale_requirements)
CLASSIFIER.fit(X, Y)  # Hier wird das ausgewählte Modell mit den trainingsdaten trainiert

print_mapping(cis_requirements,funktionale_requirements,34)


# print_mapping(cis_requirements, funktionale_requirements, 33)


### TESTEN DES MODELLS
test_X = "ensure ldap server is not installed" # ensure rsyslog is used for remote log  vs.  ensure rsyslog is used for remote logging

prediction_probabilities = get_prediction_probability_for_sample(test_X)
print(prediction_probabilities)
get_probability_plot(prediction_probabilities, test_X)

predict_funktionale_Anforderung(test_X)
print("[+] Folgende Stopwords wurden entfernt:  " + str(VECTORIZER.stop_words_))

# save Classifier persistent as pickle file
# save_persistent_model("test1.pickle")
