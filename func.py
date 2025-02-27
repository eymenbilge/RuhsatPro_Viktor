import ifcopenshell
import pandas as pd


def load_ifc_file(ifc_path: str):
    """Load and return an IFC file using ifcopenshell."""
    return ifcopenshell.open(ifc_path)


def get_pset_property(pset, property_name: str):
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


def extract_space_data(ifc_file) -> pd.DataFrame:
    """
    Extracts IfcSpace data from an IFC file and returns it as a pandas DataFrame.
    """
    spaces = ifc_file.by_type("IfcSpace")
    data = []
    for space in spaces:
        object_type = space.ObjectType or ''
        long_name = space.LongName or ''
        area = ''
        bagimsiz_bolum_no = ''
        blok_no = ''
        emsal_alan_tipi = ''
        eklenti_degil = ''

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

    columns = [
        'Alan Şeması',
        'Mahal Adı',
        'Alan',
        'BagimsizBolumNo',
        'BlokNo',
        'EmsalAlanTipi',
        'Eklenti/Degil',
        'Seviye'
    ]
    return pd.DataFrame(data, columns=columns)


def split_dataframes_by_object_type(df: pd.DataFrame):
    """
    Splits the input DataFrame by unique 'Alan Şeması' values.
    Returns a dictionary of DataFrames keyed by object type.
    """
    return {obj_type: group.copy() for obj_type, group in df.groupby('Alan Şeması')}


def format_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    For all numeric columns in df, format the values to two decimals as strings
    using vectorized operations.
    """
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].applymap(lambda x: f"{x:.2f}")
    return df


def turkish_lower(text: str) -> str:
    """
    Converts text to lowercase with proper Turkish character handling.
    """
    return text.replace("İ", "i").replace("I", "ı").lower()


def calculate_dataframes(ifc_file, room_data_path: str):
    """
    Orchestrates the processing pipeline:
      1. Extract space data from the IFC file.
      2. Split data by object type.
      3. Compute pivot tables, summaries, and additional metrics.
      4. Returns a dictionary of results.
    """
    df_main = extract_space_data(ifc_file)
    dfs = split_dataframes_by_object_type(df_main)
    df_EmsalAlan = dfs.get('Emsal Alan', pd.DataFrame())
    df_BrutAlan = dfs.get('Brüt Alan', pd.DataFrame())
    df_NetAlan = dfs.get('Net Alan', pd.DataFrame())

    # Process df_NetAlan: filter and create composite key without extra copies
    df_NetAlan = df_NetAlan[df_NetAlan['BagimsizBolumNo'].astype(bool)]
    df_NetAlan['BlokBagimsizBolumNo'] = df_NetAlan['BlokNo'] + df_NetAlan['BagimsizBolumNo'].astype(str)

    df_NetAlan_ozet = df_NetAlan.pivot_table(
        index=['BlokNo', 'BagimsizBolumNo', 'Eklenti/Degil', 'BlokBagimsizBolumNo'],
        values='Alan',
        aggfunc='sum'
    ).reset_index()

    # Convert 'Eklenti/Degil' to boolean
    df_NetAlan_ozet['Eklenti/Degil'] = df_NetAlan_ozet['Eklenti/Degil'].map({
        'TRUE': True,
        'FALSE': False,
        True: True,
        False: False
    }).fillna(False).astype(bool)

    df_BrutAlan['BlokBagimsizBolumNo'] = df_BrutAlan['BlokNo'] + df_BrutAlan['BagimsizBolumNo'].astype(str)

    # Basic area summaries
    insaat_alani_toplam = df_BrutAlan['Alan'].sum()
    df_EmsalAlan['Alan'] = pd.to_numeric(df_EmsalAlan['Alan'], errors='coerce')
    emsal_harici_toplam = df_EmsalAlan['Alan'].dropna().sum()
    emsal_kullanilan_toplam = insaat_alani_toplam - emsal_harici_toplam

    # Emsal pivot table
    df_emsal_filtered = df_EmsalAlan[df_EmsalAlan['EmsalAlanTipi'].astype(bool)]
    emsal_ozet_tablo = df_emsal_filtered.pivot_table(
        index='Seviye',
        columns='EmsalAlanTipi',
        values='Alan',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

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

    # Group area sum per level, name, and type
    df_area_sum = df_EmsalAlan.groupby(["Seviye", "Mahal Adı", "EmsalAlanTipi"])['Alan'].sum().reset_index()

    # NET / EKLENTİ / BRÜT calculations
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

    unique_blok = pd.DataFrame(
        df_BrutAlan.loc[df_BrutAlan['Mahal Adı'] == 'BAĞIMSIZ BÖLÜM', 'BlokBagimsizBolumNo'].unique(),
        columns=['BlokBagimsizBolumNo']
    )

    final_df = unique_blok.merge(net_alan, on='BlokBagimsizBolumNo', how='left') \
        .merge(eklenti_net_alan, on='BlokBagimsizBolumNo', how='left') \
        .merge(brut_alan, on='BlokBagimsizBolumNo', how='left') \
        .merge(eklenti_brut_alan, on='BlokBagimsizBolumNo', how='left') \
        .fillna(0)

    # Calculate shared areas (Ortak Alan)
    metrekare_cetveli = final_df[final_df['BlokBagimsizBolumNo'] != ''].copy()
    sum_of_ortak_alan_area = df_BrutAlan[df_BrutAlan['Mahal Adı'] == 'ORTAK ALAN']['Alan'].sum()
    total_brut_alan = metrekare_cetveli['BrutAlan'].sum()
    distribution_factor = sum_of_ortak_alan_area / total_brut_alan if total_brut_alan != 0 else 0

    metrekare_cetveli['OrtakAlan'] = metrekare_cetveli['BrutAlan'] * distribution_factor
    metrekare_cetveli['ToplamBrutAlan'] = metrekare_cetveli['BrutAlan'] + metrekare_cetveli['EklentiBrutAlan']
    metrekare_cetveli['GenelBrutAlan'] = metrekare_cetveli['ToplamBrutAlan'] + metrekare_cetveli['OrtakAlan']

    # Otopark Katsayisi
    def calculate_otopark_katsayisi(brut_value):
        if brut_value < 80:
            return 0.33
        elif brut_value < 120:
            return 0.50
        elif brut_value < 180:
            return 1.0
        else:
            return 2.0

    metrekare_cetveli['OtoparkKatsayisi'] = metrekare_cetveli['BrutAlan'].apply(calculate_otopark_katsayisi)
    total_otopark_ihtiyaci = int(metrekare_cetveli['OtoparkKatsayisi'].sum())

    # Sığınak İhtiyacı (using room data)
    room_data = pd.read_csv(room_data_path, dtype={"Mahal Adı": str, "Etiket": str})
    room_data["Mahal Adı"] = room_data["Mahal Adı"].apply(turkish_lower)
    room_data_dict = dict(zip(room_data["Mahal Adı"], room_data["Etiket"]))

    df_NetAlan["Mahal Adı Normalized"] = df_NetAlan["Mahal Adı"].apply(turkish_lower)
    df_NetAlan["Room Label"] = df_NetAlan["Mahal Adı Normalized"].map(room_data_dict)

    room_counts = (
        df_NetAlan[df_NetAlan["Room Label"].isin(["oda", "salon"])]
        .groupby(["BlokBagimsizBolumNo", "Room Label"])
        .size()
        .unstack(fill_value=0)
    )
    room_counts = room_counts.reindex(columns=["oda", "salon"], fill_value=0)
    room_counts["Tipi"] = room_counts["oda"].astype(str) + "+" + room_counts["salon"].astype(str)
    metrekare_cetveli = metrekare_cetveli.merge(room_counts, on="BlokBagimsizBolumNo", how="left").fillna(0)
    metrekare_cetveli["oda"] = metrekare_cetveli["oda"].astype(int)
    metrekare_cetveli["salon"] = metrekare_cetveli["salon"].astype(int)

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
    total_siginak_ihtiyaci = int(metrekare_cetveli["SiginakIhtiyaci"].sum())

    # Drop unnecessary columns and format numeric columns
    metrekare_cetveli.drop(columns=['OtoparkKatsayisi', 'oda', 'salon', 'SiginakIhtiyaci'], inplace=True)
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
