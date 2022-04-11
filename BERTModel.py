# install ktrain using the following command
# pip install ktrain

# import ktrain and the ktrain.text modules
import ktrain
from ktrain import text
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


# fetch the dataset using scikit-learn
allCategories = pickle.load(open("allCategories.pkl", "rb"))
all_paragraphs = pickle.load(open("all_files_paragraphs.pkl", "rb"))
all_paragraphs2=[]
for file in all_paragraphs:
  for p in file:
    all_paragraphs2.append(p)
    
    
    
    
from itertools import islice
lengths=pickle.load(open("lengths.pkl","rb"))
def splitDataDocument(x,y,lengths,ratio = 0.2):
    new_X = []
    new_Y = []
    new_Y_parts = []
    
    count = 0
    for i in range(len(lengths)):
        new_Y.append(0)
        new_X.append([])
        new_Y_parts.append([])
        for j in range(lengths[i]):
            new_X[-1].append(x[count])
            new_Y_parts[-1].append(y[count])
            new_Y[-1] = max(new_Y[-1],y[count])
            count += 1
    
    y_all = [new_Y.count(0),new_Y.count(1)]
    y_count = [0,0]
    x_train, y_train, x_test,y_test = [],[],[],[]
    for i in range(len(new_Y)):
        if y_count[new_Y[i]] <= y_all[new_Y[i]]*(1-ratio):
            for j in range(len(new_X[i])):
                x_train.append(new_X[i][j])
                y_train.append(new_Y_parts[i][j])
        else:
            for j in range(len(new_X[i])):
                x_test.append(new_X[i][j])
                y_test.append(new_Y_parts[i][j])
        y_count[new_Y[i]] += 1
    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    
    return x_train, y_train, x_test,y_test

def splitData(x,y,ratio = 0.2):
    y_all = [y.count(0),y.count(1)]
    y_count = [0,0]
    x_train, y_train, x_test,y_test = [],[],[],[]
    for i in range(len(y)):
        if y_count[y[i]] <= y_all[y[i]]*(1-ratio):
            x_train.append(x[i])
            y_train.append(y[i])
            y_count[y[i]] += 1
        else:
            x_test.append(x[i])
            y_test.append(y[i])
            y_count[y[i]] += 1
    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    
    return x_train, y_train, x_test,y_test



def get_y(cat_number):
    y=[]
    for file in allCategories:
        for paragraph in file:
            y.append(paragraph[cat_number])
    return y
x=all_paragraphs2
RFC_Table_scores_PRF=[]        
RFC_Table_scores=[]


for cat_number in range(9):
    PFR=[]
    y = get_y(cat_number)
    
    # x_train,y_train,x_test,y_test = splitData(x,y,ratio=0.2)
    x_train,y_train,x_test,y_test = splitDataDocument(x,y,lengths,ratio=0.2)
    (x_train,  y_train), (x_test, y_test), preproc = text.texts_from_array(x_train=x_train, y_train=y_train,
                                                                       x_test=x_test, y_test=y_test,
                                                                       class_names=['0', '1'],
                                                                       preprocess_mode='bert',
                                                                       maxlen=512, 
                                                                       max_features=1000)
    
    
    # Load the BERT Model and Instantiate a Learner object
    # you can disregard the deprecation warnings arising from using Keras 2.2.4 with TensorFlow 1.14.
    model = text.text_classifier('bert', train_data=(x_train, y_train), preproc=preproc)
    learner = ktrain.get_learner(model, train_data=(x_train, y_train), batch_size=6)
    
    
    
    # STEP 3: Train the Model
    # 5e-5, 3e-5, or 2e-5
    learner.fit_onecycle(2e-5, 10)
    learner.validate(val_data=(x_test, y_test), class_names=['0', '1'])
    predictor = ktrain.get_predictor(learner.model, preproc)
    predictor.save("predictor_cat"+str(cat_number+1))
