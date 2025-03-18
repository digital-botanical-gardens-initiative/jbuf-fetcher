import datacompy
import pandas as pd

# cvs
df1 = pd.read_csv(
    "/mnt/c/Users/Heloise Coen/OneDrive - Université de Fribourg/Bureau/uni/TravailBachelor/jbuf-fetcher-1/species_list_croisee_treated_upper_taxo_test.csv"
)
"""df2 = pd.read_csv(
    "/mnt/c/Users/Heloise Coen/OneDrive - Université de Fribourg/Bureau/uni/TravailBachelor/jbuf-fetcher-1/species_list_croisee_upper_taxo_test.csv"
)"""


# Convert JSON to DataFrame
# df_json = pd.DataFrame(list_directus)

df_json = pd.read_json("../data/directus_data.json")
# print(df_json.columns)

# Nettoyer les noms de colonnes (supprimer les espaces potentiels)
df1.columns = df1.columns.str.strip()
# df2.columns = df2.columns.str.strip()
df_json.columns = df_json.columns.str.strip()

# vérifier si colonne existe
if "sample_name" not in df_json.columns:
    raise ValueError()

# debug
if "_merge" in df1.columns:
    df1.drop(columns=["_merge"], inplace=True)

df_json["organism_otol_unique_name"] = df_json["sample_name"]
compare = datacompy.Compare(
    df1[["organism_otol_unique_name"]],
    # df2,
    df_json[["organism_otol_unique_name"]],
    join_columns="organism_otol_unique_name",  # You can also specify a list of columns
    abs_tol=0.0001,
    rel_tol=0,
    # df1_name="treated",
    # df2_name="nontreated",
)

print(compare.report())
