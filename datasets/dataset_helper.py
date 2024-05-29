import pandas as pd

# # Load the dataset
# df = pd.read_csv('indian_attractions_final.csv')

# # Drop the 'Country' column
# df = df.drop('Country', axis=1)

# # Save the updated dataframe back to the same CSV file
# df.to_csv('indian_attractions_final.csv', index=False)

# # Print the updated dataframe
# print(df)


# Load the dataset with error handling
df = pd.read_csv('final-us.csv', on_bad_lines='skip')

# Remove duplicates based on the 'Name' and 'City' columns
df = df.drop_duplicates(subset=['Name', 'City'])

# Save the updated dataframe back to the same CSV file
df.to_csv('final-us.csv', index=False)

# Print the updated dataframe
print(df)


# # Load the cleaned dataset
# df_cleaned = pd.read_csv('final-us-cleaned.csv')

# # Load the original dataset
# df_original = pd.read_csv('final-us.csv')

# # Compare missing values by name
# missing_values = df_original[~df_original['Name'].isin(df_cleaned['Name'])]

# # Print the missing values
# print(missing_values)