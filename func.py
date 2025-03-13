from ifcopenshell import open as ifc_open
import pandas as pd



def load_ifc_file(ifc_path: str):
    """Load and return an IFC file using ifcopenshell."""
    return ifc_open(ifc_path)


def extract_space_data(ifc_file) -> pd.DataFrame:
    """
    Extracts IfcSpace data from an IFC file and returns it as a pandas DataFrame.
    Optimized version that collects all properties in a single pass per space.
    """
    spaces = ifc_file.by_type("IfcSpace")
    data = []
    
    for space in spaces:
        # Initialize with default values
        space_data = {
            'Alan Şeması': space.ObjectType or '',
            'Mahal Adı': space.LongName or '',
            'Alan': '',
            'BagimsizBolumNo': '',
            'BlokNo': '',
            'EmsalAlanTipi': '',
            'Eklenti/Degil': '',
            'Seviye': ''
        }
        
        # Process property sets in a single pass
        for definition in space.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                pset = definition.RelatingPropertyDefinition
                if not pset.is_a('IfcPropertySet'):
                    continue
                    
                pset_name = pset.Name
                
                # Extract properties based on property set name
                if pset_name == 'Qto_Area':
                    space_data['Alan'] = get_property_value(pset, 'Area')
                elif pset_name == 'Pset_BagimsizBolum':
                    space_data['BagimsizBolumNo'] = get_property_value(pset, 'BagimsizBolumNo')
                    space_data['BlokNo'] = get_property_value(pset, 'BlokNo')
                elif pset_name == 'Pset_EmsalAlanTipi':
                    space_data['EmsalAlanTipi'] = get_property_value(pset, 'EmsalAlanTipi')
                elif pset_name == 'Pset_NetAlanTipi':
                    space_data['Eklenti/Degil'] = get_property_value(pset, 'Eklenti/Degil')
        
        # Find building storey in a more efficient way
        space_data['Seviye'] = get_building_storey(space)
        data.append(list(space_data.values()))

    columns = list(space_data.keys())
    return pd.DataFrame(data, columns=columns)


def get_property_value(pset, property_name: str):
    """
    Returns a property's value from a property set (pset) by the given property_name.
    If the property is not found or its value is None, returns an empty string.
    """
    for prop in pset.HasProperties:
        if prop.Name == property_name:
            nominal_value = prop.NominalValue
            return '' if nominal_value is None else nominal_value.wrappedValue
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


def split_dataframes_by_object_type(df: pd.DataFrame):
    """
    Splits the input DataFrame by unique 'Alan Şeması' values.
    Returns a dictionary of DataFrames with views instead of copies where possible.
    """
    return {obj_type: group for obj_type, group in df.groupby('Alan Şeması')}


def turkish_lower_vectorized(series):
    """
    Vectorized version of turkish_lower function for Series objects.
    """
    return series.str.replace("İ", "i").str.replace("I", "ı").str.lower()


def calculate_dataframes(ifc_file, room_data_path: str):
    """
    Optimized processing pipeline:
      1. Extract space data from the IFC file.
      2. Split data by object type.
      3. Compute pivot tables, summaries, and additional metrics.
      4. Returns a dictionary of results.
    """
    # Extract data once and convert numeric columns immediately
    df_main = extract_space_data(ifc_file)
    numeric_cols = ['Alan']
    df_main[numeric_cols] = df_main[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Split by object type - no explicit copies
    dfs = split_dataframes_by_object_type(df_main)
    
    # Get dataframes by type, defaulting to empty DataFrame with correct columns
    empty_df = pd.DataFrame(columns=df_main.columns)
    df_EmsalAlan = dfs.get('Emsal Alan', empty_df)
    df_BrutAlan = dfs.get('Brüt Alan', empty_df)
    df_NetAlan = dfs.get('Net Alan', empty_df)

    # Create BlokBagimsizBolumNo field for all relevant dataframes at once
    for df in [df_NetAlan, df_BrutAlan]:
        df['BlokBagimsizBolumNo'] = df['BlokNo'] + df['BagimsizBolumNo'].astype(str)

    # Process df_NetAlan: Create filtered view
    net_alan_filtered = df_NetAlan[df_NetAlan['BagimsizBolumNo'].astype(bool)]
    
    # Create pivot table for Net Alan summary
    df_NetAlan_ozet = pd.pivot_table(
        net_alan_filtered,
        index=['BlokNo', 'BagimsizBolumNo', 'Eklenti/Degil', 'BlokBagimsizBolumNo'],
        values='Alan',
        aggfunc='sum'
    ).reset_index()

    # Convert 'Eklenti/Degil' to boolean using efficient mapping
    map_values = {'TRUE': True, 'FALSE': False, True: True, False: False}
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].map(map_values)
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].fillna(False)
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].astype(bool)
    # Calculate basic area summaries
    insaat_alani_toplam = df_BrutAlan['Alan'].sum()
    emsal_harici_toplam = df_EmsalAlan['Alan'].sum()
    emsal_kullanilan_toplam = insaat_alani_toplam - emsal_harici_toplam

    # Create Emsal pivot table more efficiently
    emsal_filtered = df_EmsalAlan[df_EmsalAlan['EmsalAlanTipi'].astype(bool)]
    emsal_ozet_tablo = pd.pivot_table(
        emsal_filtered,
        index='Seviye',
        columns='EmsalAlanTipi',
        values='Alan',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Calculate TOPLAM EMSAL DIŞI
    if '%30 KAPSAMINDA EMSAL DIŞI' in emsal_ozet_tablo.columns and 'DOĞRUDAN EMSAL DIŞI' in emsal_ozet_tablo.columns:
        emsal_ozet_tablo['TOPLAM EMSAL DIŞI'] = (
            emsal_ozet_tablo['%30 KAPSAMINDA EMSAL DIŞI'] +
            emsal_ozet_tablo['DOĞRUDAN EMSAL DIŞI']
        )
    else:
        # Handle missing columns case by providing defaults
        if '%30 KAPSAMINDA EMSAL DIŞI' not in emsal_ozet_tablo.columns:
            emsal_ozet_tablo['%30 KAPSAMINDA EMSAL DIŞI'] = 0
        if 'DOĞRUDAN EMSAL DIŞI' not in emsal_ozet_tablo.columns:
            emsal_ozet_tablo['DOĞRUDAN EMSAL DIŞI'] = 0
        emsal_ozet_tablo['TOPLAM EMSAL DIŞI'] = (
            emsal_ozet_tablo['%30 KAPSAMINDA EMSAL DIŞI'] +
            emsal_ozet_tablo['DOĞRUDAN EMSAL DIŞI']
        )

    # Get inşaat alanı by level in a more direct way
    insaat_alan_bylevel = df_BrutAlan.pivot_table(
        index='Seviye',
        values='Alan',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Merge tables efficiently
    emsal_ozet_tablo_all = pd.merge(
        emsal_ozet_tablo,
        insaat_alan_bylevel,
        on='Seviye',
        how='left'
    ).rename(columns={'Alan': 'İNŞAAT ALANI'}).fillna(0)

    # Calculate EMSAL ALANI
    emsal_ozet_tablo_all['EMSAL ALANI'] = (
        emsal_ozet_tablo_all['İNŞAAT ALANI'] -
        emsal_ozet_tablo_all['TOPLAM EMSAL DIŞI']
    )

    # Reorder columns
    desired_order = [
        'Seviye',
        'İNŞAAT ALANI',
        'TOPLAM EMSAL DIŞI',
        '%30 KAPSAMINDA EMSAL DIŞI',
        'DOĞRUDAN EMSAL DIŞI',
        'EMSAL ALANI'
    ]
    # Get only existing columns in the desired order
    existing_columns = [col for col in desired_order if col in emsal_ozet_tablo_all.columns]
    emsal_ozet_tablo_all = emsal_ozet_tablo_all[existing_columns]

    # Build metrekare_cetveli more efficiently with fewer intermediate dataframes
    # Prepare masks and groupby operations for better performance
    mask_bb = df_BrutAlan['Mahal Adı'] == 'BAĞIMSIZ BÖLÜM'
    mask_ek = df_BrutAlan['Mahal Adı'] == 'EKLENTİ ALAN'
    mask_oa = df_BrutAlan['Mahal Adı'] == 'ORTAK ALAN'
    
    # Use masks to filter and calculate in a single pass where possible
    brut_alan_df = df_BrutAlan[mask_bb].groupby('BlokBagimsizBolumNo')['Alan'].sum().reset_index(name='BrutAlan')
    eklenti_brut_alan_df = df_BrutAlan[mask_ek].groupby('BlokBagimsizBolumNo')['Alan'].sum().reset_index(name='EklentiBrutAlan')
    
    # Get unique BlokBagimsizBolumNo values for joining
    unique_blok = pd.DataFrame(
        df_BrutAlan.loc[mask_bb, 'BlokBagimsizBolumNo'].unique(),
        columns=['BlokBagimsizBolumNo']
    )
    
    # Calculate Net and Eklenti Net areas more efficiently
    mask_net = ~df_NetAlan_ozet['Eklenti/Degil']
    mask_eklenti = df_NetAlan_ozet['Eklenti/Degil']
    
    net_alan_df = df_NetAlan_ozet[mask_net].groupby('BlokBagimsizBolumNo')['Alan'].sum().reset_index(name='NetAlan')
    eklenti_net_alan_df = df_NetAlan_ozet[mask_eklenti].groupby('BlokBagimsizBolumNo')['Alan'].sum().reset_index(name='EklentiNetAlan')
    
    # Create the dataframe with a more efficient merge chain
    final_df = (unique_blok
                .merge(net_alan_df, on='BlokBagimsizBolumNo', how='left')
                .merge(eklenti_net_alan_df, on='BlokBagimsizBolumNo', how='left')
                .merge(brut_alan_df, on='BlokBagimsizBolumNo', how='left')
                .merge(eklenti_brut_alan_df, on='BlokBagimsizBolumNo', how='left')
                .fillna(0))
    
    # Ortak Alan Calculations
    metrekare_cetveli = final_df[final_df['BlokBagimsizBolumNo'] != ''].copy()
    sum_of_ortak_alan_area = df_BrutAlan[mask_oa]['Alan'].sum()
    total_brut_alan = metrekare_cetveli['BrutAlan'].sum()
    distribution_factor = sum_of_ortak_alan_area / total_brut_alan if total_brut_alan != 0 else 0
    
    # Vectorized calculation of derived columns
    metrekare_cetveli['OrtakAlan'] = metrekare_cetveli['BrutAlan'] * distribution_factor
    metrekare_cetveli['ToplamBrutAlan'] = metrekare_cetveli['BrutAlan'] + metrekare_cetveli['EklentiBrutAlan']
    metrekare_cetveli['GenelBrutAlan'] = metrekare_cetveli['ToplamBrutAlan'] + metrekare_cetveli['OrtakAlan']
    
    # Otopark Katsayisi - Vectorized implementation
    def calculate_otopark_katsayisi_vectorized(brut_series):
        # Initialize with default value
        result = pd.Series(0.33, index=brut_series.index)
        # Update values based on conditions
        result[brut_series >= 80] = 0.50
        result[brut_series >= 120] = 1.0
        result[brut_series >= 180] = 2.0
        return result
    
    metrekare_cetveli['OtoparkKatsayisi'] = calculate_otopark_katsayisi_vectorized(metrekare_cetveli['BrutAlan'])
    total_otopark_ihtiyaci = int(metrekare_cetveli['OtoparkKatsayisi'].sum())
    
    # Sığınak İhtiyacı calculations - more efficiently processing room data
    room_data = pd.read_csv(room_data_path, dtype={"Mahal Adı": str, "Etiket": str})
    
    # Vectorized string operations
    room_data["Mahal Adı"] = turkish_lower_vectorized(room_data["Mahal Adı"])
    room_data_dict = dict(zip(room_data["Mahal Adı"], room_data["Etiket"]))
    
    df_NetAlan["Mahal Adı Normalized"] = turkish_lower_vectorized(df_NetAlan["Mahal Adı"])
    df_NetAlan["Room Label"] = df_NetAlan["Mahal Adı Normalized"].map(room_data_dict)
    
    # Filter once and reuse the filtered dataframe
    filtered_rooms = df_NetAlan[df_NetAlan["Room Label"].isin(["oda", "salon"])]
    room_counts = filtered_rooms.groupby(["BlokBagimsizBolumNo", "Room Label"]).size().unstack(fill_value=0)
    
    # Ensure columns exist
    for col in ["oda", "salon"]:
        if col not in room_counts.columns:
            room_counts[col] = 0
    
    # Create Tipi column
    room_counts["Tipi"] = room_counts["oda"].astype(str) + "+" + room_counts["salon"].astype(str)
    
    # Merge with metrekare_cetveli
    metrekare_cetveli = metrekare_cetveli.merge(room_counts, on="BlokBagimsizBolumNo", how="left").fillna(0)
    metrekare_cetveli["oda"] = metrekare_cetveli["oda"].astype(int)
    metrekare_cetveli["salon"] = metrekare_cetveli["salon"].astype(int)
    
    # Vectorized Sığınak calculation
    def calc_siginak_vectorized(oda_series):
        result = pd.Series(0, index=oda_series.index)
        result[oda_series == 1] = 2
        result[oda_series == 2] = 3
        result[oda_series >= 3] = 4
        return result
    
    metrekare_cetveli["SiginakIhtiyaci"] = calc_siginak_vectorized(metrekare_cetveli["oda"])
    total_siginak_ihtiyaci = int(metrekare_cetveli["SiginakIhtiyaci"].sum())
    
    # Drop unnecessary columns and format numeric columns
    metrekare_cetveli.drop(columns=['OtoparkKatsayisi', 'oda', 'salon', 'SiginakIhtiyaci'], inplace=True)
    
    # Format numeric columns more efficiently
    def format_numeric_columns(df):
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            df[col] = df[col].apply(lambda x: f"{x:.2f}")
        return df
    
    metrekare_cetveli = format_numeric_columns(metrekare_cetveli)
    emsal_ozet_tablo_all = format_numeric_columns(emsal_ozet_tablo_all)
    
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
    ifc_path = r"model.ifc"  # update as needed
    room_data_path = "room_data.csv"                    # update as needed

    ifc_model = load_ifc_file(ifc_path)
    results = calculate_dataframes(ifc_model, room_data_path)

    print(results["emsal_ozet_tablo_all"].head())
    print(results["metrekare_cetveli"].head())


if __name__ == "__main__":
    main()