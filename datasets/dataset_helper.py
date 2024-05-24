import pandas as pd

# Load the dataset
df = pd.read_csv('indian_attractions_final.csv')

# Drop the 'Country' column
df = df.drop('Country', axis=1)

# Save the updated dataframe back to the same CSV file
df.to_csv('indian_attractions_final.csv', index=False)

# Print the updated dataframe
print(df)