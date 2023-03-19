import pandas as pd
import numpy as np
import streamlit as st
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80")

new_df = pd.read_csv('https://media.githubusercontent.com/media/weiaun96/ecommerce-recommendation-web-app/main/reviews2.csv', on_bad_lines='skip')

#Import Libraries for matrix factorization
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

n_ratings = len(new_df)
n_products = len(new_df['product_id'].unique())
n_customers = len(new_df['customer_id'].unique())

user_freq = new_df[['customer_id', 'product_id']].groupby('customer_id').count().reset_index()
user_freq.columns = ['customer_id', 'n_ratings']

# Now, we create customer-product matrix using scipy csr matrix
def create_matrix(df):
      
    N = len(new_df['customer_id'].unique())
    M = len(new_df['product_id'].unique())
      
    # Map Ids to indices
    user_mapper = dict(zip(np.unique(new_df["customer_id"]), list(range(N))))
    product_mapper = dict(zip(np.unique(new_df["product_id"]), list(range(M))))
    
    # Map indices to IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(new_df["customer_id"])))
    product_inv_mapper = dict(zip(list(range(M)), np.unique(new_df["product_id"])))
      
    user_index = [user_mapper[i] for i in new_df['customer_id']]
    product_index = [product_mapper[i] for i in new_df['product_id']]
  
    X = csr_matrix((new_df["recommend_score"], (product_index, user_index)), shape=(M, N))
      
    return X, user_mapper, product_mapper, user_inv_mapper, product_inv_mapper
  
X, user_mapper, product_mapper, user_inv_mapper, product_inv_mapper = create_matrix(new_df)

# Find similar products using KNN
def find_similar_products(product_id, X, k, metric='cosine', show_distance=False):
      
    neighbour_ids = []
      
    product_ind = product_mapper[product_id]
    product_vec = X[product_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    product_vec = product_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(product_vec, return_distance=show_distance)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(product_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids

product_titles = dict(zip(new_df['product_id'], new_df['product_title']))

st.title('E-Commerce Recommendations')
st.header('Outdoors Category')
searchTerm = st.text_area('Finding an outdoors product?', value='', height=None, max_chars=None, key=None)

if st.button('**Search Now**'):
    if searchTerm.lower() == "exit":
        st.write('Thanks for shopping with us, have a nice day!')

    else:
        searchResult = new_df[new_df['product_title'].str.contains((searchTerm),case=False)]
        searchdupl = searchResult.drop_duplicates(subset='product_title')
        searchResultSorted = searchdupl.sort_values(by=['recommend_score','product_title'],ascending=False).reset_index()
        searchResultSorted.index = np.arange(1, len(searchResultSorted) + 1)
        final_result = searchResultSorted.loc[:,['product_id', 'product_title','recommend_score']].head(10)

        #Replace average VADER score column as recommendation score
        final_result = final_result.rename(columns={'product_id': 'Product ID','product_title': 'Product Title',
                                                    'recommend_score': 'Recommendation Score'})
        if len(final_result.index) < 1:
            st.write("\nSorry! No results is found, please search again")
        else:
            st.table(final_result.head(10))
            product_id = final_result.iloc[0,0]
            similar_ids = find_similar_products(product_id, X, k=10)
            product_title = product_titles[product_id]
            
            st.subheader(f"Since you found the no.1 product: {product_title},")
            st.write("\n**You may also like these:**\n")
            for i in similar_ids:
                  st.write(product_titles[i])
