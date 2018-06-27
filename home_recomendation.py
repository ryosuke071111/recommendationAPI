import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, jsonify

app = Flask(__name__)

ratings = pd.read_csv('rating.csv')
homes = pd.read_csv('homes.csv')

x = ["Unnamed: 9", "Unnamed: 8", "Unnamed: 7"]
homes.drop(x, axis=1)

#メンバー順で並べ替え
homes.sort_values('members', ascending= False)[:10]

#メンバーの多いものだけ抽出
homes = homes[homes['members'] > 10000]
homes.isnull().sum()
ratings = ratings[ratings.rating >= 0]

mergeddf = ratings.merge(homes, left_on = 'home_id', right_on = 'home_id', suffixes= ['_user', ''])

mergeddf = mergeddf[['user_id','name','rating_user']]
mergeddf = mergeddf.drop_duplicates(['user_id','name'])

home_pivot = mergeddf.pivot(index= 'name',columns='user_id',values='rating_user').fillna(0)

##疎行列を非ゼロ要素だけにして学習する
home_pivot_sparse = csr_matrix(home_pivot.values)

knn = NearestNeighbors(n_neighbors=9,algorithm= 'brute', metric= 'cosine')

# 前処理したデータセットでモデルを訓練
model_knn = knn.fit(home_pivot_sparse)

# パラメータ受け取って代入
@app.route('/<name>', methods=['GET'])
def match(name):
  home = (name)
  distance, indice = model_knn.kneighbors(home_pivot.iloc[home_pivot.index == home].values.reshape(1,-1),n_neighbors=11)
  return('{0}{1}{2}'.format(distance,"|", indice ))

if __name__ == '__main__':
    app.run(debug=True)
