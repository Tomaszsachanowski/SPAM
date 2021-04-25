import pandas as pd

# Wczytanie danych z pliku testowego
raw_data = pd.read_csv('data/test_data.csv')

# Pozyskanie dnaych o kraju i recenzji 
df = raw_data[['country', 'description']]
# Połaczenie recenzji ze wspolnego kraju.
df_country_reviews = df.groupby(['country'])['description'].apply(lambda x: ' '.join(x.astype(str))).reset_index()
print(df_country_reviews)

# Sprawdzam czy recenzja dla US jest dobrze połączona.
US_reviews = df_country_reviews.loc[df_country_reviews['country'] == 'US']
print(US_reviews)
rewiew = US_reviews.iat[0, 1]
print(rewiew)

# Pozyskanie nazw krajów.
country = list(df_country_reviews['country'])
# Pozyskanie recenzji dla krajów
reviews = list(df_country_reviews['description'])

print(country)
print(reviews[0])
