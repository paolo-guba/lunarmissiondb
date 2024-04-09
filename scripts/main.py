import pandas as pd

from lunardb import DATA_DIR
from lunardb.lunardb.gcat_catalog import GCATCatalogSelector
from lunardb.lunardb.gcat_data_loader import GCATDataLoader

## Get the GCAT data
satcat = GCATDataLoader.get_satcat()
tmpcat = GCATDataLoader.get_catalog(GCATCatalogSelector.TMPCAT.value)
ftocat = GCATDataLoader.get_catalog(GCATCatalogSelector.FTOCAT.value)
auxcat = GCATDataLoader.get_catalog(GCATCatalogSelector.AUXCAT.value)
cso = GCATDataLoader.get_catalog(GCATCatalogSelector.CSOCAT.value)

##
# Unique OpOrbit

unique_op_orbit = satcat.dataframe['OpOrbit'].unique()

##
# Look for names that have "lunar" in them
lunar_missions = satcat.dataframe[satcat.dataframe['OpOrbit'] == "CLO"]
solar_missions = satcat.dataframe[satcat.dataframe['OpOrbit'] == "EEO"]
solar_missions_tmp = tmpcat.dataframe[tmpcat.dataframe['OpOrbit'] == "EEO"]
solar_missions_fto = ftocat.dataframe[ftocat.dataframe['OpOrbit'] == "EEO"]
solar_missions_aux = auxcat.dataframe[auxcat.dataframe['OpOrbit'] == "EEO"]
solar_missions_cso = cso.dataframe[cso.dataframe['OpOrbit'] == "EEO"]
lunar_misisons_tmp = tmpcat.dataframe[tmpcat.dataframe['OpOrbit'] == "CLO"]
lunar_misisons_fto = ftocat.dataframe[ftocat.dataframe['OpOrbit'] == "CLO"]
lunar_misisons_aux = auxcat.dataframe[auxcat.dataframe['OpOrbit'] == "CLO"]
lunar_misisons_cso = cso.dataframe[cso.dataframe['OpOrbit'] == "CLO"]

## Merge all solar missions
solar_missions_all = pd.concat([solar_missions, solar_missions_tmp, solar_missions_fto, solar_missions_aux, solar_missions_cso])

## Merge all lunar missions
lunar_missions_all = pd.concat([lunar_missions, lunar_misisons_tmp, lunar_misisons_fto, lunar_misisons_aux, lunar_misisons_cso])

## Merge all
all_missions = pd.concat([satcat.dataframe, tmpcat.dataframe, ftocat.dataframe, auxcat.dataframe, cso.dataframe])

## Load the moon db
filepath = DATA_DIR / "MoonDatabase.csv"
moon_db_original = pd.read_csv(filepath, sep=';')

##
nssdc_ids = moon_db_original['NSSDCID'].unique()
# exclude the ones that are not string do not have fformat YYYY-NNNX
clean_nssdc_ids = []
for nid in nssdc_ids:
    if isinstance(nid, str) and len(nid) in [8, 9]:
        clean_nssdc_ids.append(nid)

moon_db_with_clean_nssdc_ids = moon_db_original[moon_db_original['NSSDCID'].isin(clean_nssdc_ids)]

## Go through the lunar_missions and when the 'Piece' value is in the moon_db_with_clean_nssdc_ids['NSSDCID'] then we have a match. In this case, add to a new dataframe
all_missions_in_moon_db = all_missions[all_missions['Piece'].isin(moon_db_with_clean_nssdc_ids['NSSDCID'])]
moon_db_unique = moon_db_with_clean_nssdc_ids.drop_duplicates(subset=['NSSDCID'])
all_missions_unique = all_missions_in_moon_db.drop_duplicates(subset=['Piece'])

# create a new version of the moon db that has the #JCAT value from the all_missions_unique dataframe
moon_db_with_jcat = moon_db_unique.merge(all_missions_unique[['Piece', '#JCAT']], left_on='NSSDCID', right_on='Piece', how='left')

# recreate a moon_db, re
moon_db_original_new = moon_db_original.merge(moon_db_with_jcat[['NSSDCID', '#JCAT']], on='NSSDCID', how='left')
# move column as first
moon_db_original_new = moon_db_original_new[["#JCAT"] + [col for col in moon_db_original_new.columns if col != "#JCAT"]]

# save it as a csv
# moon_db_original_new.to_csv(DATA_DIR / "MoonDatabase_with_JCAT.csv", sep=';', index=False)
# add all the columns (without data) that are in all_missions_unique to the moon_db_original_new
all_missions_unique_columns = all_missions_unique.columns
moon_db_columns = moon_db_original_new.columns
moon_db_original_new = pd.concat([moon_db_original_new, pd.DataFrame(columns=all_missions_unique_columns)])
# order columns in alphabetical order
moon_db_original_new = moon_db_original_new.reindex(sorted(moon_db_original_new.columns), axis=1)

##

# create dataframe with objects from lunar_missions that are not in moon_db_with_jcat
lunar_missions_not_in_moon_db = lunar_missions_all[~lunar_missions_all['#JCAT'].isin(moon_db_with_jcat['#JCAT'])]

lunar_missions_not_in_moon_db = pd.concat([lunar_missions_not_in_moon_db, pd.DataFrame(columns=moon_db_columns)])
# order columns in alphabetical order
lunar_missions_not_in_moon_db = lunar_missions_not_in_moon_db.reindex(sorted(lunar_missions_not_in_moon_db.columns), axis=1)

# fill the columns that correspond with new rows in moon_db_original_new
for index, row in lunar_missions_not_in_moon_db.iterrows():
    moon_db_original_new = moon_db_original_new._append(row, ignore_index=True)


##
moon_db_original_new = moon_db_original_new.sort_values(by='#JCAT')

