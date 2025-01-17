import pandas as pd 
import pycountry

def load_dataset():
    df = pd.read_csv("moonbucks_dataset.csv")
    df = df.drop(["country", "phone_number_1", "phone_number_2", "fax_1", "fax_2", "email_1", "email_2", "website", "facebook", "twitter", "instagram", "pinterest", "youtube"], axis=1)
    df = df.rename(columns={"state": "country_code"})
    df["country"] = df.apply(lambda row: pycountry.countries.get(alpha_2=row["country_code"]).name, axis=1)
    df = df[["name", "url", "street_address", "city", "zip_code", "country_code", "country", "open_hours", "latitude", "longitude"]]
    return df

def get_country_dict(df):
    country_names = df["country"].unique()
    country_codes = df["country_code"].unique()
    countries = {}
    for name, code in zip(country_names, country_codes):
        countries[code] = {"name": name, "n_stores": len(df.loc[df["country_code"] == code])}
    return countries

def get_local_stores(df, country_code=None, country_name=None):
    if country_code != None:
        local_df = df.loc[df["country_code"] == country_code].reset_index(drop=True)
    elif country_name != None:
        local_df = df.loc[df["country"] == country_name].reset_index(drop=True)
    else:
        raise Exception("Please enter either country_code or country_name.")
    return local_df
