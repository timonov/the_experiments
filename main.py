from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier as Rfc
from sklearn.ensemble import GradientBoostingClassifier as Gbc
from sklearn.naive_bayes import BernoulliNB as Bnb
from sklearn.naive_bayes import MultinomialNB as Mnb
from sklearn.cross_validation import KFold
from plot import *
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
# import numpy as np

# download matrix ############################################################################################


def swap(index1, index2, iterable):
    for x in iterable:
        x[index1], x[index2] = x[index2], x[index1]


def download_matrix(path):
    raw_data = open(path)
    data_set = np.loadtxt(raw_data, delimiter=",")
    matrix_from_file = data_set[:, :]
    swap(0, 6, matrix_from_file)
    return matrix_from_file

##############################################################################################################


def prepare_matrix_for_feature_engineering(matrix_from_file, step):
    x_all = matrix_from_file[:, 1:]
    y_all = matrix_from_file[:, 0]
    x_train = matrix_from_file[0:step, 1:]
    y_train = matrix_from_file[0:step, 0]
    x_test = matrix_from_file[step:194, 1:]
    y_test = matrix_from_file[step:194, 0]
    return x_train, y_train, x_test, y_test, x_all, y_all


def naive_bayes_bnb(x_train, y_train, x_test, y_test):
    model = Bnb()
    model.fit(x_train, y_train)
    expected = y_test
    predicted = model.predict(x_test)
    return expected, predicted


def naive_bayes_mnb(x_train, y_train, x_test, y_test):
    model = Mnb()
    model.fit(x_train, y_train)
    expected = y_test
    predicted = model.predict(x_test)
    return expected, predicted


def random_forest_classifier(x_train, y_train, x_test, y_test, tree):
    model = Rfc(n_estimators=tree, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1,
                min_weight_fraction_leaf=0.0, max_features="auto", max_leaf_nodes=None, bootstrap=False,
                oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False, class_weight=None)
    model.fit(x_train, y_train)
    predicted = model.predict(x_test)
    expected = y_test
    return expected, predicted

# def random_forest_classifier(x_train, y_train, x_test, y_test):
#     model = Rfc(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1,
#                 min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, bootstrap=True,
#                 oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False, class_weight=None)
#     model.fit(x_train, y_train)
#     predicted = model.predict(x_test)
#     expected = y_test
#     return expected, predicted


def gradient_boosting_classifier(x_train, y_train, x_test, y_test, num_tree):
    model = Gbc(loss='deviance', learning_rate=0.2, n_estimators=num_tree, subsample=1.0, min_samples_split=2,
                min_samples_leaf=10, min_weight_fraction_leaf=0.0, max_depth=5, init=None, random_state=None,
                max_features=None, verbose=0, max_leaf_nodes=None, warm_start=False)
    model.fit(x_train, y_train)
    expected = y_test
    predicted = model.predict(x_test)
    return expected, predicted

# def gradient_boosting_classifier(x_train, y_train, x_test, y_test):
#     model = Gbc(loss='deviance', learning_rate=0.1, n_estimators=10, subsample=1.0, min_samples_split=2,
#                 min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=1, init=None, random_state=None,
#                 max_features=None, verbose=0, max_leaf_nodes=None, warm_start=False)
#     model.fit(x_train, y_train)
#     expected = y_test
#     predicted = model.predict(x_test)
#     return expected, predicted

##############################################################################################################


def run_cross_validation(x, y, clf_class, **kwargs):
    kf = KFold(len(y), n_folds=10, shuffle=True)
    y_prediction = y.copy()

    for train_index, test_index in kf:
        x_train, x_test = x[train_index], x[test_index]
        y_train = y[train_index]
        clf = clf_class(**kwargs)
        clf.fit(x_train, y_train)
        y_prediction[test_index] = clf.predict(x_test)
    return y_prediction


def accuracy(y_true, y_prediction):
    return np.mean(y_true == y_prediction)

##############################################################################################################

if __name__ == "__main__":
    _matrix_from_file = download_matrix("./dataset.txt")

# section one: increase _x_train and calculate accuracy score
    _x_train_steps = []
    accuracy_score_bnb = []
    accuracy_score_rfc = []
    accuracy_score_gbc = []
    for i in range(30, 174, 20):
        _x_train_steps.append(i)
        _x_train, _y_train, _x_test, _y_test, _x_all, _y_all = \
            prepare_matrix_for_feature_engineering(_matrix_from_file, i)
        expected_bnb, predicted_bnb = naive_bayes_bnb(_x_train, _y_train, _x_test, _y_test)
        expected_rfc, predicted_rfc = random_forest_classifier(_x_train, _y_train, _x_test, _y_test, 25)
        expected_gbc, predicted_gbc = gradient_boosting_classifier(_x_train, _y_train, _x_test, _y_test, 25)

        accuracy_score_bnb.append(accuracy_score(expected_bnb, predicted_bnb))
        accuracy_score_rfc.append(accuracy_score(expected_rfc, predicted_rfc))
        accuracy_score_gbc.append(accuracy_score(expected_gbc, predicted_gbc))

        if i == 90:
            print("--- Simple run ---")
            print("BernoulliNB: %.3f" % accuracy_score_bnb[3])
            print("RandomForestClassifier: %.3f" % accuracy_score_rfc[3])
            print("GradientBoostingClassifier: %.3f" % accuracy_score_gbc[3])
    default_plot_report(_x_train_steps, accuracy_score_bnb, accuracy_score_rfc, accuracy_score_gbc)

# section two: plot confusion matrix of the classifier
    _x_train, _y_train, _x_test, _y_test, _x_all, _y_all = \
        prepare_matrix_for_feature_engineering(_matrix_from_file, 90)
    expected_bnb, predicted_bnb = naive_bayes_bnb(_x_train, _y_train, _x_test, _y_test)
    expected_rfc, predicted_rfc = random_forest_classifier(_x_train, _y_train, _x_test, _y_test, 25)
    expected_gbc, predicted_gbc = gradient_boosting_classifier(_x_train, _y_train, _x_test, _y_test, 25)

    confusion_matrix_bnb = confusion_matrix(expected_bnb, predicted_bnb)
    confusion_matrix_frc = confusion_matrix(expected_rfc, predicted_rfc)
    confusion_matrix_gbc = confusion_matrix(expected_gbc, predicted_gbc)
    plot_classification_report(confusion_matrix_bnb)
    plot_classification_report(confusion_matrix_frc)
    plot_classification_report(confusion_matrix_gbc)

# section three: run cross validation and print results
    _x_all = _matrix_from_file[:, 1:]
    _y_all = _matrix_from_file[:, 0]
    scaler = StandardScaler()
    _x_all = scaler.fit_transform(_x_all)
    print ("--- Cross validation ---")
    print ("BernoulliNB: %.3f" % accuracy(_y_all, run_cross_validation(_x_all, _y_all, Bnb)))
    print ("RandomForestClassifier: %.3f" % accuracy(_y_all, run_cross_validation(_x_all, _y_all, Rfc)))
    print ("GradientBoostingClassifier: %.3f" % accuracy(_y_all, run_cross_validation(_x_all, _y_all, Gbc)))

# section four: plot_diff_num_tree
    _x_train, _y_train, _x_test, _y_test, _x_all, _y_all = prepare_matrix_for_feature_engineering(_matrix_from_file, 90)

    expected_bnb, predicted_bnb = naive_bayes_bnb(_x_train, _y_train, _x_test, _y_test)
    expected_mnb, predicted_mnb = naive_bayes_mnb(_x_train, _y_train, _x_test, _y_test)
    expected_rfc, predicted_rfc = random_forest_classifier(_x_train, _y_train, _x_test, _y_test, 25)
    expected_gbc, predicted_gbc = gradient_boosting_classifier(_x_train, _y_train, _x_test, _y_test, 25)

    classification_report_bnb = classification_report(expected_bnb, predicted_bnb)
    plot_classification_report_for_each_method(classification_report_bnb, 'Classification report for BernoulliNB')

    classification_report_mnb = classification_report(expected_mnb, predicted_mnb)
    plot_classification_report_for_each_method(classification_report_mnb, 'Classification report for MultinomialNB')

    classification_report_rfc = classification_report(expected_rfc, predicted_rfc)
    plot_classification_report_for_each_method(classification_report_rfc,
                                               'Classification report for RandomForestClassifier')

    classification_report_gbc = classification_report(expected_gbc, predicted_gbc)
    plot_classification_report_for_each_method(classification_report_gbc,
                                               'Classification report for GradientBoostingClassifier')
    num_tree = []
    accuracy_score_rfc = []
    accuracy_score_gbc = []
    for i in range(1, 200, 10):
        num_tree.append(i)
        expected_rfc, actual_rfc = random_forest_classifier(_x_train, _y_train, _x_test, _y_test, i)
        expected_gbc, actual_gbc = gradient_boosting_classifier(_x_train, _y_train, _x_test, _y_test, i)
        accuracy_score_rfc.append(accuracy(expected_rfc, actual_rfc))
        accuracy_score_gbc.append(accuracy(expected_gbc, actual_gbc))
    plot_diff_num_tree(num_tree, accuracy_score_rfc, accuracy_score_gbc)
