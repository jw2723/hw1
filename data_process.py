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

oldest_species.to_csv(r"/Users/jingqiwang/Desktop/In Progress/Cornell University/INFO 5311 visualization/hw1/oldest_species.csv", index=False)

print(oldest_species)

# get names of the 7 species got earlier from "oldest_species" calculations
oldest_species_names = oldest_species['Species'].tolist()

# get the rows with those 7 species
oldest_species_trees = df[df['Species'].isin(oldest_species_names)]

# filter out data for location to use on map(species name, address, latitude & longitude)
species_address_data = oldest_species_trees[['Species', 'qAddress', 'Latitude', 'Longitude']]

species_address_data.to_csv("/Users/jingqiwang/Desktop/In Progress/Cornell University/INFO 5311 visualization/hw1/oldest_species_addresses.csv", index=False)