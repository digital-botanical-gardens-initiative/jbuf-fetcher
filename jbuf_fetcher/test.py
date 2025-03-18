import datacompy
import pandas as pd

df1 = pd.read_csv(
    "/mnt/c/Users/Heloise Coen/OneDrive - Université de Fribourg/Bureau/uni/TravailBachelor/jbuf-fetcher-1/species_list_croisee_treated_upper_taxo_test.csv"
)
df2 = pd.read_csv(
    "/mnt/c/Users/Heloise Coen/OneDrive - Université de Fribourg/Bureau/uni/TravailBachelor/jbuf-fetcher-1/species_list_croisee_upper_taxo_test.csv"
)

# Nettoyer les noms de colonnes (supprimer les espaces potentiels)
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

if "_merge" in df1.columns:
    df1.drop(columns=["_merge"], inplace=True)

compare = datacompy.Compare(
    df1,
    df2,
    join_columns="organism_otol_unique_name",  # You can also specify a list of columns
    abs_tol=0.0001,
    rel_tol=0,
    df1_name="treated",
    df2_name="nontreated",
)

print(compare.report())
