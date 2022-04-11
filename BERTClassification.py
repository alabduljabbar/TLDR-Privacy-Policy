# install ktrain using the following command
# pip install ktrain




import ktrain
from ktrain import text
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

# Download all predictors from the following link:
# https://drive.google.com/drive/folders/1vzGQSZGBqbbFDf_iA4KmM3-3svWvXNv7
    
    
for cat_number in range(9):
    all_paragraphs = pickle.load(open("Paragraphs.pkl", "rb"))
    reloaded_predictor = ktrain.load_predictor("predictor_cat"+str(cat_number+1))
    cat=[]
    cat_sum=[]
    for file in all_paragraphs:
        try:
          preds = reloaded_predictor.predict(file)
          preds= [int(i) for i in preds]
          cat.append(preds)
          cat_sum.append(sum(preds))
        except:
          preds=0
          cat.append(preds)
          cat_sum.append(preds)
    pickle.dump(cat, open("Classification_Output_cat"+str(cat_number+1)+".pkl", "wb"))
    pickle.dump(cat_sum, open("Classification_Output_cat"+str(cat_number+1)+"_sum.pkl", "wb"))
