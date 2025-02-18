import ifcopenshell
import pandas as pd


def load_ifc_file(ifc_path: str):
    """
    Load and return an IFC file using ifcopenshell.
    """
    model = ifcopenshell.open(ifc_path)
    return model

def get_pset_property(pset, property_name: str):
    """
    Returns a property's value from a property set (pset) by the given property_name.
    If it's a boolean (IfcBoolean), returns True/False. Otherwise returns the raw value.
    If the property is not found, returns an empty string.
    """
    for prop in pset.HasProperties:
        if prop.Name == property_name:
            nominal_value = prop.NominalValue
            if nominal_value is None:
                return ''
            # Handle boolean
            if nominal_value.is_a('IfcBoolean'):
                return nominal_value.wrappedValue
            else:
                return nominal_value.wrappedValue
    return ''

def get_building_storey(space):
    """
    Find the IfcBuildingStorey that contains this IfcSpace.
    Returns the storey name if found, otherwise an empty string.
    """
    for rel in space.Decomposes:
        if rel.is_a('IfcRelAggregates') and rel.RelatingObject.is_a('IfcBuildingStorey'):
            return rel.RelatingObject.Name
    return ''

def extract_space_data(ifc_file) -> pd.DataFrame:
    """
    Extracts IfcSpace data from an IFC file and returns it as a pandas DataFrame.
    Columns: [Alan Şeması, Mahal Adı, Alan, BagimsizBolumNo, BlokNo, EmsalAlanTipi, Eklenti/Degil, Seviye].
    """
    spaces = ifc_file.by_type("IfcSpace")
    data = []

    for space in spaces:
        object_type = space.ObjectType if space.ObjectType else ''
        name = space.Name if space.Name else ''
        long_name = space.LongName if space.LongName else ''

        area = ''
        bagimsiz_bolum_no = ''
        blok_no = ''
        emsal_alan_tipi = ''
        eklenti_degil = ''

        # Read property sets
        for definition in space.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                pset = definition.RelatingPropertyDefinition
                if pset.is_a('IfcPropertySet'):
                    if pset.Name == 'Qto_Area':
                        area = get_pset_property(pset, 'Area')
                    elif pset.Name == 'Pset_BagimsizBolum':
                        bagimsiz_bolum_no = get_pset_property(pset, 'BagimsizBolumNo')
                        blok_no = get_pset_property(pset, 'BlokNo')
                    elif pset.Name == 'Pset_EmsalAlanTipi':
                        emsal_alan_tipi = get_pset_property(pset, 'EmsalAlanTipi')
                    elif pset.Name == 'Pset_NetAlanTipi':
                        eklenti_degil = get_pset_property(pset, 'Eklenti/Degil')

        building_storey = get_building_storey(space)

        data.append([
            object_type,
            long_name,
            area,
            bagimsiz_bolum_no,
            blok_no,
            emsal_alan_tipi,
            eklenti_degil,
            building_storey
        ])

    df = pd.DataFrame(
        data,
        columns=[
            'Alan Şeması',
            'Mahal Adı',
            'Alan',
            'BagimsizBolumNo',
            'BlokNo',
            'EmsalAlanTipi',
            'Eklenti/Degil',
            'Seviye'
        ]
    )
    return df

def split_dataframes_by_object_type(df: pd.DataFrame):
    """
    Splits the input DataFrame by unique 'Alan Şeması' values and returns
    a dictionary of DataFrames keyed by the object type (e.g. 'Net Alan', 'Brüt Alan', etc.).
    """
    object_types = df['Alan Şeması'].unique()
    dfs = {}
    for obj_type in object_types:
        dfs[obj_type] = df[df['Alan Şeması'] == obj_type].copy()
    return dfs

def format_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    For all numeric columns in df, format the values to two decimals as strings.
    """
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: f"{x:.2f}")
    return df

def turkish_lower(text: str) -> str:
    """
    Converts text to lowercase with proper Turkish character handling.
    """
    return text.replace("İ", "i").replace("I", "ı").lower()

def calculate_dataframes(ifc_file, room_data_path: str):
    """
    Orchestrates the entire pipeline:
      1. Uses the IFC model passed in (ifc_file).
      2. Extracts space data into DataFrame.
      3. Splits data by Alan Şeması (object type).
      4. Computes required pivot tables and summary DataFrames.
      5. Returns the main results for further usage or exporting.
    """
    # 1. We already have the IFC file/model from caller

    # 2. Extract Data
    df_main = extract_space_data(ifc_file)

    # 3. Split DataFrames by ObjectType
    dfs = split_dataframes_by_object_type(df_main)
    df_EmsalAlan = dfs.get('Emsal Alan', pd.DataFrame()).copy()
    df_BrutAlan = dfs.get('Brüt Alan', pd.DataFrame()).copy()
    df_NetAlan = dfs.get('Net Alan', pd.DataFrame()).copy()

    # 4. Example of saving a CSV if needed
    df_BrutAlan.to_csv('df_BrutAlan.csv', index=False)

    # ---- Perform all transformations below ----
    # 4a. Prepare DataFrames
    df_BrutAlan = df_BrutAlan.copy()
    df_NetAlan = df_NetAlan.copy()
    df_EmsalAlan = df_EmsalAlan.copy()

    # 4b. Create BlokBagimsizBolumNo and pivot in df_NetAlan
    df_NetAlan = df_NetAlan[df_NetAlan['BagimsizBolumNo'].notna() & (df_NetAlan['BagimsizBolumNo'] != '')]
    df_NetAlan['BlokBagimsizBolumNo'] = df_NetAlan['BlokNo'] + df_NetAlan['BagimsizBolumNo'].astype(str)

    df_NetAlan_ozet = df_NetAlan.pivot_table(
        index=['BlokNo', 'BagimsizBolumNo', 'Eklenti/Degil', 'BlokBagimsizBolumNo'],
        values='Alan',
        aggfunc='sum'
    ).reset_index()

    # 4c. Convert 'Eklenti/Degil' to real boolean
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].map({
        'TRUE': True,
        'FALSE': False,
        True: True,
        False: False
    })
    df_NetAlan_ozet.loc[df_NetAlan_ozet['Eklenti/Degil'].isna(), 'Eklenti/Degil'] = False
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].astype(bool)

    # 4d. Add BlokBagimsizBolumNo in df_BrutAlan
    df_BrutAlan['BlokBagimsizBolumNo'] = df_BrutAlan['BlokNo'] + df_BrutAlan['BagimsizBolumNo'].astype(str)

    # 4e. Basic Area Summaries
    insaat_alani_toplam = df_BrutAlan['Alan'].sum()
    df_EmsalAlan['Alan'] = pd.to_numeric(df_EmsalAlan['Alan'], errors='coerce')
    emsal_harici_toplam = df_EmsalAlan['Alan'].dropna().sum()
    emsal_kullanilan_toplam = insaat_alani_toplam - emsal_harici_toplam

    # 4f. Create Emsal Pivot Table
    df_emsal_filtered = df_EmsalAlan[
        df_EmsalAlan['EmsalAlanTipi'].notna() & (df_EmsalAlan['EmsalAlanTipi'] != '')
    ]
    emsal_ozet_tablo = df_emsal_filtered.pivot_table(
        index='Seviye',
        columns='EmsalAlanTipi',
        values='Alan',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Add computed columns
    emsal_ozet_tablo['TOPLAM EMSAL DIŞI'] = (
        emsal_ozet_tablo.get('%30 KAPSAMINDA EMSAL DIŞI', 0) +
        emsal_ozet_tablo.get('DOĞRUDAN EMSAL DIŞI', 0)
    )

    insaat_alan_bylevel = df_BrutAlan.pivot_table(
        index='Seviye',
        values='Alan',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    emsal_ozet_tablo_all = pd.merge(
        emsal_ozet_tablo,
        insaat_alan_bylevel,
        on='Seviye',
        how='left'
    ).rename(columns={'Alan': 'İNŞAAT ALANI'}).fillna(0)

    emsal_ozet_tablo_all['EMSAL ALANI'] = (
        emsal_ozet_tablo_all['İNŞAAT ALANI'] -
        emsal_ozet_tablo_all['TOPLAM EMSAL DIŞI']
    )

    desired_order = [
        'Seviye',
        'İNŞAAT ALANI',
        'TOPLAM EMSAL DIŞI',
        '%30 KAPSAMINDA EMSAL DIŞI',
        'DOĞRUDAN EMSAL DIŞI',
        'EMSAL ALANI'
    ]
    emsal_ozet_tablo_all = emsal_ozet_tablo_all[desired_order]

    # 4g. Summaries per level+name (optional)
    df_area_sum = df_EmsalAlan.groupby(["Seviye", 'Mahal Adı', 'EmsalAlanTipi'])['Alan'].sum().reset_index()

    # 4h. NET / EKLENTİ / BRÜT Calculations
    net_alan = (
        df_NetAlan_ozet[~df_NetAlan_ozet['Eklenti/Degil']]
        .groupby('BlokBagimsizBolumNo')['Alan']
        .sum()
        .reset_index()
        .rename(columns={'Alan': 'NetAlan'})
    )

    eklenti_net_alan = (
        df_NetAlan_ozet[df_NetAlan_ozet['Eklenti/Degil']]
        .groupby('BlokBagimsizBolumNo')['Alan']
        .sum()
        .reset_index()
        .rename(columns={'Alan': 'EklentiNetAlan'})
    )

    brut_alan = (
        df_BrutAlan[df_BrutAlan['Mahal Adı'] == 'BAĞIMSIZ BÖLÜM']
        .groupby('BlokBagimsizBolumNo')['Alan']
        .sum()
        .reset_index()
        .rename(columns={'Alan': 'BrutAlan'})
    )

    eklenti_brut_alan = (
        df_BrutAlan[df_BrutAlan['Mahal Adı'] == 'EKLENTİ ALAN']
        .groupby('BlokBagimsizBolumNo')['Alan']
        .sum()
        .reset_index()
        .rename(columns={'Alan': 'EklentiBrutAlan'})
    )

    unique_blok_bagimsiz_bolum_no = pd.DataFrame(
        df_BrutAlan.loc[df_BrutAlan['Mahal Adı'] == 'BAĞIMSIZ BÖLÜM', 'BlokBagimsizBolumNo'].unique(),
        columns=['BlokBagimsizBolumNo']
    )

    final_df = (
        unique_blok_bagimsiz_bolum_no
        .merge(net_alan, on='BlokBagimsizBolumNo', how='left')
        .merge(eklenti_net_alan, on='BlokBagimsizBolumNo', how='left')
        .merge(brut_alan, on='BlokBagimsizBolumNo', how='left')
        .merge(eklenti_brut_alan, on='BlokBagimsizBolumNo', how='left')
        .fillna(0)
    )

    # 4i. Calculate Shared Areas (Ortak Alan)
    metrekare_cetveli = final_df[final_df['BlokBagimsizBolumNo'] != ''].copy()
    sum_of_ortak_alan_area = df_BrutAlan[df_BrutAlan['Mahal Adı'] == 'ORTAK ALAN']['Alan'].sum()
    total_brut_alan = metrekare_cetveli['BrutAlan'].sum()
    distribution_factor = sum_of_ortak_alan_area / total_brut_alan if total_brut_alan != 0 else 0

    metrekare_cetveli['OrtakAlan'] = metrekare_cetveli['BrutAlan'] * distribution_factor
    metrekare_cetveli['ToplamBrutAlan'] = metrekare_cetveli['BrutAlan'] + metrekare_cetveli['EklentiBrutAlan']
    metrekare_cetveli['GenelBrutAlan'] = metrekare_cetveli['ToplamBrutAlan'] + metrekare_cetveli['OrtakAlan']

    # 4j. Otopark Katsayisi
    def calculate_otopark_katsayisi(brut_alan_value):
        if brut_alan_value < 80:
            return 0.33
        elif brut_alan_value < 120:
            return 0.50
        elif brut_alan_value < 180:
            return 1.0
        else:
            return 2.0

    metrekare_cetveli['OtoparkKatsayisi'] = metrekare_cetveli['BrutAlan'].apply(calculate_otopark_katsayisi)
    total_otopark_ihtiyaci = metrekare_cetveli['OtoparkKatsayisi'].sum()

    # 4k. Sığınak İhtiyacı (using room_data)
    room_data = pd.read_csv(room_data_path)
    room_data["Mahal Adı"] = room_data["Mahal Adı"].astype(str).apply(turkish_lower)
    room_data_dict = dict(zip(room_data["Mahal Adı"], room_data["Etiket"]))

    df_NetAlan["Mahal Adı Normalized"] = df_NetAlan["Mahal Adı"].astype(str).apply(turkish_lower)
    df_NetAlan["Room Label"] = df_NetAlan["Mahal Adı Normalized"].map(room_data_dict)

    # Count "oda" and "salon"
    room_counts = (
        df_NetAlan[df_NetAlan["Room Label"].isin(["oda", "salon"])]
        .groupby(["BlokBagimsizBolumNo", "Room Label"])
        .size()
        .unstack(fill_value=0)
    )

    # Ensure "oda" and "salon" columns exist
    room_counts = room_counts.reindex(columns=["oda", "salon"], fill_value=0)
    room_counts["Tipi"] = room_counts["oda"].astype(str) + "+" + room_counts["salon"].astype(str)

    # Merge with metrekare_cetveli
    metrekare_cetveli = metrekare_cetveli.merge(room_counts, on="BlokBagimsizBolumNo", how="left").fillna(0)

    # Convert columns to int
    metrekare_cetveli["oda"] = metrekare_cetveli["oda"].astype(int)
    metrekare_cetveli["salon"] = metrekare_cetveli["salon"].astype(int)

    # Calculate "SiginakIhtiyaci"
    def calc_siginak(oda_count):
        if oda_count == 1:
            return 2
        elif oda_count == 2:
            return 3
        elif oda_count >= 3:
            return 4
        else:
            return 0

    metrekare_cetveli["SiginakIhtiyaci"] = metrekare_cetveli["oda"].apply(calc_siginak)
    total_siginak_ihtiyaci = metrekare_cetveli["SiginakIhtiyaci"].sum()

    # 4l. Drop columns we don't need in final output
    metrekare_cetveli = metrekare_cetveli.drop(columns=['OtoparkKatsayisi', 'oda', 'salon', 'SiginakIhtiyaci'])

    # 4m. Format numeric columns
    metrekare_cetveli = format_numeric_columns(metrekare_cetveli)
    emsal_ozet_tablo_all = format_numeric_columns(emsal_ozet_tablo_all)
    # Convert numpy types to native Python types
    total_siginak_ihtiyaci = int(total_siginak_ihtiyaci)  # Assuming this is a numpy.int64
    total_otopark_ihtiyaci = int(total_otopark_ihtiyaci)
    # Return a dictionary of final results so the caller can use them.
    return {
        "df_NetAlan": df_NetAlan,
        "df_BrutAlan": df_BrutAlan,
        "df_EmsalAlan": df_EmsalAlan,
        "df_NetAlan_ozet": df_NetAlan_ozet,
        "emsal_ozet_tablo_all": emsal_ozet_tablo_all,
        "metrekare_cetveli": metrekare_cetveli,
        "insaat_alani_toplam": insaat_alani_toplam,
        "emsal_harici_toplam": emsal_harici_toplam,
        "emsal_kullanilan_toplam": emsal_kullanilan_toplam,
        "total_otopark_ihtiyaci": total_otopark_ihtiyaci,   
        "total_siginak_ihtiyaci": total_siginak_ihtiyaci
    }

def main():
    """
    Example usage where we load the IFC model before passing it to calculate_dataframes.
    """
    ifc_path = r"D:\OneDrive\PermitGenerator_r25.ifc"  # or read from config
    room_data_path = "room_data.csv"                  # or read from config

    # Load the IFC model outside of calculate_dataframes
    ifc_model = load_ifc_file(ifc_path)

    # Pass the loaded model
    results = calculate_dataframes(ifc_model, room_data_path)

    # Example usage of returned DataFrames:
    df_emsal_ozet = results["emsal_ozet_tablo_all"]
    df_metrekare = results["metrekare_cetveli"]

    # Print or export as needed
    print(df_emsal_ozet.head())
    print(df_metrekare.head())

if __name__ == "__main__":
    main()
