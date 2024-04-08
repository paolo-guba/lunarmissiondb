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

