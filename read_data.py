import pandas as pd

# Wczytanie danych z pliku testowego
raw_data = pd.read_csv('data/test_data.csv')

# Pozyskanie dnaych o kraju i recenzji 
df_country_reviews = raw_data[['country', 'description']]
print(df_country_reviews)