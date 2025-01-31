import pdb 
import numpy as np
import pandas as pd

from math import ceil

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, 
                             precision_score, 
                             recall_score, 
                             accuracy_score, 
                             f1_score, 
                             roc_curve,
                             auc)


from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE

####################################################################

def get_genre_subset(df, genre_list):
    """
    Subsets a dataframe on multiple Super_genres
    """
    subset = df[df.Super_genre == genre_list[0]]
    for i in range(1, len(genre_list)):
        subset = pd.concat([subset, df[df.Super_genre == genre_list[i]]])
    
    return subset


def run_multinomial_log_reg(df, genres, features, solver="lbfgs"):
    """
    Runs a multinomial logistic regression on the provided target genres
    """
    subset = get_genre_subset(df, genres)
    
    X = subset[features]
    y = subset.Super_genre
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)
    
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_sample(X_train, y_train)

    multi_logreg = LogisticRegression(random_state=42, solver=solver, multi_class="multinomial")
    multi_logreg.fit(X_train, y_train)
    
    return multi_logreg.score(X_test,y_test)


def plot_roc(df, genre1, genre2, axis):
    """
    Accepts a dataframe with columns for fpr and tpr.
    subsets those columns and plots the ROC 
    """
    genre_comparison = df[(df.genre_1 == genre1) & (df.genre_2 == genre2)]
    tpr = genre_comparison.tpr[genre_comparison.index[0]]
    fpr = genre_comparison.fpr[genre_comparison.index[0]]

    AUC = genre_comparison.AUC[genre_comparison.index[0]]

    sns.lineplot(fpr,tpr, ax=axis)
    plt.title(f"{genre1.title()} & {genre2.title()} (AUC: {round(AUC,3)})", fontsize=24)

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")

    # plt.show()
    return genre_comparison.AUC[genre_comparison.index[0]]


def plot_roc_group(df, genre_pairs):
    
    fig = plt.figure(figsize=(16,8))

    for i, pair in enumerate(genre_pairs):
        ax = fig.add_subplot(ceil(len(genre_pairs) / 2), 2, i + 1)

        plot_roc(df, pair[0], pair[1], ax)

    plt.tight_layout()
    plt.show()