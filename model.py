from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.tree import plot_tree

#Loading Heat_wave.csv
Heat_wave = pd.read_csv('Heat_wave.csv')

#Drop rows containing NaN values
df = Heat_wave.dropna(subset=['Heat_Stress'])

df.set_index('date_time', inplace=True)

X = df.drop('Heat_Wave', axis=1)
y = df['Heat_Wave']

x_train,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state=0)

#Training a DecisionTreeClassifier
dtc = DecisionTreeClassifier(criterion='entropy', max_depth=4, min_samples_split=5, 
                             min_samples_leaf=5,random_state=0)
dtc.fit(x_train, y_train)

#Using Test data to predict
y_pred = dtc.predict(x_test)

#Accuracy of predicted labels wrt actual ones
print("Accuracy: %f" % accuracy_score(y_test, y_pred))

# # To plot decision tree, use matplotlib versions before 3.7.2
# fig, ax = plt.subplots(figsize=(6, 6)) #figsize value changes the size of plot
# tree.plot_tree(dtc,ax=ax,feature_names=list(X.columns))
# plt.show()

# Function to make predictions when called from the data.py
def prediction(sample):
    pred = dtc.predict(sample)
    return pred