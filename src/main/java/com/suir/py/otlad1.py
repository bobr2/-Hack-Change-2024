import joblib
import pandas as pd
import sys
import json
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.spatial.distance import cdist


def standart(dataset):
    dataset.drop(["clientId", "currentMethod", "organizationId", "availableMethods", "claims"], axis=1, inplace=True)
    dataset.loc[dataset['segment'] == 'Средний бизнес', 'segment'] = 1
    dataset.loc[dataset['segment'] == 'Малый бизнес', 'segment'] = 0
    dataset.loc[dataset['segment'] == 'Крупный бизнес', 'segment'] = 2
    dataset.loc[dataset['role'] == 'Сотрудник', 'role'] = 0
    dataset.loc[dataset['role'] == 'ЕИО', 'role'] = 1

    return dataset

    

def tree(ask):
    ask = ask.loc[0].to_dict()
    
    if ask["role"] == "ЕИО":
        probab = np.array([[0.2, 0.4, 0.4]])
        weight = 0.2
    
    #отношение мобилка к вебу
    mobile = ask["signatures.common.mobile"] + ask["signatures.special.mobile"]
    web = ask["signatures.common.web"] + ask["signatures.special.web"]
    comman = (ask["signatures.common.mobile"] +  + ask["signatures.common.web"])//5 
    special = ask["signatures.special.mobile"] + ask["signatures.special.web"]

    if web > mobile:
        ko = 1 / (web / mobile)
        ko = 1 - ko
        probab = np.array([[ko, (1 - ko)*0.5, (1 - ko)*0.5]])
        weight = ko
    else:
        ko = (web / mobile)
        ko = 1 - ko

        probab = np.array([[ko*0.5, (1 - ko*0.5)*0.5, (1- ko*0.5)*0.5]])
        
        weight = ko

        if comman > special:
            ko_s = comman / special
            probab = np.array([[ko*0.5, (1 - ko*0.5)*0.5/ko_s, (1- ko*0.5)*0.5*ko_s]])
        else:
            ko_s = comman / special
            probab = np.array([[ko*0.5, (1 - ko*0.5)*0.5/ko_s, (1- ko*0.5)*0.5*ko_s]])    
    

    

    
    weight_ml = 1 - weight
    return probab, weight, weight_ml



# загрузка первого дата сета



def predict_from_file(file_path):

    result = {"class": "",
              "app" : "",
              "avail_methods" : ""
              }


    # Загрузка данных
    with open(file_path, 'r', encoding='utf-8') as f:
        ask = json.load(f)
    ask = pd.json_normalize(ask)  # Или другой формат, если нужно

    ask_dict = ask.loc[0].to_dict()
    

    result['avail_methods'] = ask_dict["availableMethods"]
    if ask_dict["mobileApp"] == False:
        result["app"] = "Вы ещё не пользуетесь приложением Альфа-Бизнес. Хотите установить?"
    else:
        result["app"] = "У вас уже есть наше приложение. Попробуйте подписание документов через Альфа-Бизнес "


    #нужно вызвать трии
    tree_prob, weight_tree, weight_ml = tree(ask)

    ask_s = standart(ask)
    # new_row = ask.values

    new_row = ask_s.loc[0].to_dict()

    dataset.loc[len(dataset)] = new_row

    scaler1 = StandardScaler()
    scaled_data1 = scaler1.fit_transform(dataset)

    tsne = TSNE(n_components=2, max_iter=1000, random_state=1)
    X_tsne = tsne.fit_transform(scaled_data1)

    X_tsne = [X_tsne[len(X_tsne) - 1]][0].reshape((1, 2))

    predictions = model.predict(X_tsne)  # Делаем предсказания

    # Печатаем предсказания в формате JSON predictions[len(predictions) - 1].item()
    
    cluster_centers = model.cluster_centers_

    # Вычисление расстояний от каждого объекта до центров кластеров
    distances = cdist(X_tsne, cluster_centers, metric='euclidean')

    # Нормализация расстояний для интерпретации как "вероятность"
    probabilities = 1 / (distances + 1e-100)  # Добавлено малое число для избежания деления на ноль
    probabilities /= probabilities.sum(axis=1, keepdims=True)

    probabilities = np.around(probabilities, decimals=2)
    
    
    resultition = []
    for i in range(3):

        answer = weight_ml * probabilities[0][i] + weight_tree * tree_prob[0][i]
        resultition.append(answer)

    resultition = np.array(resultition)
    indx = np.argmax(resultition)
    
    if indx == 0:
        result['class'] = "КЭП на токене"
    elif indx == 1:
        result['class'] = "КЭП в приложении"
    else:
        result['class'] = "Приложение Альфа-Бизнес"




    print(json.dumps(result))


if __name__ == "__main__":

    # Получаем путь к файлу из аргументов
    file_path = sys.argv[1]
    #

    with open(".\src\main\java\com\suir\suir\sdata.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    dataset = pd.json_normalize(data)
    dataset = standart(dataset)
    f.close()

    # Загрузка модели
    model = joblib.load('.\src\main\java\com\suir\suir\super_model3.pkl')

    predict_from_file(file_path)

