import pandas as pd
from datetime import datetime

# load dataset
df = pd.read_csv('/Users/jingqiwang/Desktop/In Progress/Cornell University/INFO 5311 visualization/hw1/Street_Tree_List-2022-01-30_FILTERED.csv')

# handle 'PlantDate', remove time, convert to datetime
df['PlantDate'] = pd.to_datetime(df['PlantDate'].str.split(' ').str[0], format='%m/%d/%y', errors='coerce')

# calculate tree ages
df['TreeAge'] = df['PlantDate'].apply(lambda x: (datetime.now() - x).days / 365.25 if pd.notnull(x) else None)

# extract species name after " :: "
# rows with missing info are excluded
df['Species'] = df['qSpecies'].apply(lambda x: x.split(' :: ')[-1] if isinstance(x, str) and ' :: ' in x else None)
df = df[df['Species'].notna()]

# calculate species' average age
grouped = df.groupby('Species')['TreeAge'].mean().reset_index()

# select the top 7 oldest species based on average
oldest_species = grouped.sort_values(by='TreeAge', ascending=False).head(7)

# oldest_species.to_csv(r"/Users/jingqiwang/Desktop/In Progress/Cornell University/INFO 5311 visualization/hw1/oldest_species.csv", index=False)

print(oldest_species)

# Get the names of the 7 oldest species
oldest_species_names = oldest_species['Species'].tolist()

# Filter the original dataframe to get only rows belonging to these species
oldest_species_trees = df[df['Species'].isin(oldest_species_names)]

# Extract relevant columns (species name and address)
species_address_data = oldest_species_trees[['Species', 'qAddress']]

# Save this data to a CSV file
species_address_data.to_csv("/Users/jingqiwang/Desktop/In Progress/Cornell University/INFO 5311 visualization/hw1/oldest_species_addresses.csv", index=False)