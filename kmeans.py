import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df = pd.read_csv('datasets/final-uk.csv')

X = df[['Visitors', 'Rating', 'Historical', 'Natural', 'Amusement', 'Beach']]

kmeans = KMeans(n_clusters=5, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)

plt.scatter(df['Visitors'], df['Rating'], c=df['Cluster'], cmap='viridis')
plt.xlabel('Visitors')
plt.ylabel('Rating')
plt.title('K-means Clustering of UK Attractions')
plt.colorbar(label='Cluster')
plt.show()