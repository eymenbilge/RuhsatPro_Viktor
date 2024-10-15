import viktor as vkt
from viktor.views import IFCView, IFCResult, IFCAndDataView, IFCAndDataResult
from viktor import File
from pathlib import Path
import time
from tempfile import NamedTemporaryFile
from viktor import File, ViktorController
from viktor.parametrization import (
    BooleanField,
    DownloadButton,
    FileField,
    MultiSelectField,
    Text,
    IsFalse,
    Lookup,
    ViktorParametrization,
)
from viktor.result import DownloadResult
from viktor.core import progress_message
from datetime import date
import ifcopenshell
import pandas as pd

def _use_correct_file(params) -> File:
    if params.page_1.get_sample_ifc_toggle is True:
        params.use_file = File.from_path(
            Path(__file__).parent / "sample.ifc"
        )
    else:
        params.use_file = params.page_1.ifc_upload.file
    return params.use_file

def _load_ifc_file(params):
    """Load ifc file into ifc model object."""
    ifc_upload = _use_correct_file(params)
    path = ifc_upload.copy().source
    model = ifcopenshell.open(path)
    return model

class Parametrization(vkt.Parametrization):
    page_1 = vkt.Page('IFC', views=["get_ifc_view"])
    page_1.text1 = Text(
        """
# IFC veri şeması ile yapı ruhsat süreçleri ve emsal hesaplarının kontrolü
Uygulama varsayılan bir IFC dosyası kullanır. 
Alternatif olarak siz kendi dosyanızı kullanabilirsiniz.
        """
    )
    page_1.get_sample_ifc_toggle = BooleanField("Varsayılan IFC dosyası", default=True, flex=100)
    page_1.text2 = Text(
        """
## Dosya yükleme
Gerekli parametrelerin doldurulmuş olduğu modeli buradan yükleyebilirsiniz. 
        """
    )
    page_1.ifc_upload = FileField(
        "Upload model", file_types=[".ifc"], visible=IsFalse(Lookup("page_1.get_sample_ifc_toggle")), max_size=50_000_000,
    )

    page_2 = vkt.Page('Metrekare Cetveli', views=['metrekare_view'])
    page_3 = vkt.Page('Emsal Özeti', views=['emsal_view'])

class Controller(vkt.ViktorController):
    label = "My Entity Type"
    parametrization = Parametrization(width=30)
    

    @staticmethod
    def get_data(params, key: str):
        ifc_file = _load_ifc_file(params)

        ifc_site = ifc_file.by_type("IfcSite")[0]

        # Dictionary to store the required values
        pset_values = {"ArsaAlani": None, "TAKS": None, "KAKS": None}

        # Loop through property sets of the IfcSite element
        for rel in ifc_site.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                property_set = rel.RelatingPropertyDefinition
                # Loop through properties in the property set
                for prop in property_set.HasProperties:
                    if prop.Name in pset_values:
                        # Extract the numeric value and handle potential units like 'm²'
                        value = prop.NominalValue.wrappedValue
                        pset_values[prop.Name] = float(value.split()[0]) if "m²" in value else float(value)

        # Assign extracted values to variables
        arsa_alani, taks, kaks = pset_values["ArsaAlani"], pset_values["TAKS"], pset_values["KAKS"]
        emsal_hakki=arsa_alani*kaks
        emsal_30_minha_hakki =emsal_hakki*.3
        # Helper function to get a property's value from a property set
        def get_pset_property(pset, property_name):
            for prop in pset.HasProperties:
                if prop.Name == property_name:
                    return prop.NominalValue.wrappedValue if not prop.NominalValue.is_a('IfcBoolean') else prop.NominalValue.wrappedValue
            return ''

        # Helper function to get the IfcBuildingStorey for a given IfcSpace
        def get_building_storey(space):
            for rel in space.Decomposes:
                if rel.is_a('IfcRelAggregates') and rel.RelatingObject.is_a('IfcBuildingStorey'):
                    return rel.RelatingObject.Name
            return ''

        # Get all spaces from the IFC file
        spaces = ifc_file.by_type("IfcSpace")

        # Extract the desired properties for each space
        data = []
        for space in spaces:
            object_type = space.ObjectType or ''
            name = space.Name or ''
            long_name = space.LongName or ''
            area = bagimsiz_bolum_no = blok_no = emsal_alan_tipi = eklenti_degil = ''
            
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
                        elif pset.Name == 'Pset_MahalNetAlanTipi':
                            eklenti_degil = get_pset_property(pset, 'Eklenti/Degil')
            
            building_storey = get_building_storey(space)
            
            data.append([object_type, name, long_name, area, bagimsiz_bolum_no, blok_no, emsal_alan_tipi, eklenti_degil, building_storey])

        # Create a DataFrame from the extracted data
        df = pd.DataFrame(data, columns=['ObjectType', 'Number', 'Name', 'Area', 'BagimsizBolumNo', 'BlokNo', 'EmsalAlanTipi', 'Eklenti/Degil', 'Level'])

        # Get unique ObjectType values and create separate DataFrames for each
        dfs = {obj_type: df[df['ObjectType'] == obj_type] for obj_type in df['ObjectType'].unique()}

        # Specific dataframes for different types
        df_emsal = dfs.get('Emsal Alan', pd.DataFrame())
        df_bagimsiz_bolum = dfs.get('Brüt Alan', pd.DataFrame())
        df_rooms = dfs.get('Net Alan', pd.DataFrame()).copy()
        df_rooms['BlokBagimsizBolumNo'] = df_rooms['BlokNo'] + df_rooms['BagimsizBolumNo'].astype(str)
        df_rooms_ozet = df_rooms.pivot_table(
            index=['BlokNo', 'BagimsizBolumNo','Eklenti/Degil','BlokBagimsizBolumNo'],  # Set your indexes
            values='Area',                              # Set the value column
            aggfunc='sum'                               # Aggregation function (sum, mean, etc.)
        )
        df_rooms_ozet= df_rooms_ozet.reset_index()
        df_bagimsiz_bolum = df_bagimsiz_bolum.copy()
        df_bagimsiz_bolum.loc[:, 'BlokBagimsizBolumNo'] = df_bagimsiz_bolum['BlokNo'] + df_bagimsiz_bolum['BagimsizBolumNo'].astype(str)
        insaat_alani_toplam = round(df_bagimsiz_bolum['Area'].sum(),2)
        # Convert the 'Area' column to numeric (coercing errors) using .loc
        df_emsal.loc[:, 'Area'] = pd.to_numeric(df_emsal['Area'], errors='coerce')
        # Calculate the total area (excluding rows with errors)
        emsal_harici_toplam = df_emsal['Area'].dropna().sum()
        # Calculate the used area
        emsal_kullanilan_toplam = round((insaat_alani_toplam - emsal_harici_toplam),2)
        # Filter out rows where 'EmsalAlanTipi' is null or empty
        df_emsal_filtered = df_emsal[df_emsal['EmsalAlanTipi'].notna() & (df_emsal['EmsalAlanTipi'] != '')]
        # Create the pivot table
        emsal_ozet_tablo = df_emsal_filtered.pivot_table(
            index='Level',
            columns='EmsalAlanTipi', 
            values='Area', 
            aggfunc='sum'
        ).reset_index()
        # Calculate the new column
        emsal_ozet_tablo['TOPLAM EMSAL DIŞI'] = emsal_ozet_tablo.get('30/70 KAPSAMINDA EMSAL DIŞI ALAN', 0) + emsal_ozet_tablo.get('DOĞRUDAN EMSAL DIŞI ALAN', 0)
        # Rename axis
        emsal_ozet_tablo = emsal_ozet_tablo.rename_axis(None, axis=0)
        insaat_alan_bylevel = df_bagimsiz_bolum.pivot_table(
                    
                        index='Level',
                        values='Area', 
                        aggfunc='sum'
                    ).reset_index()
        insaat_alan_bylevel = insaat_alan_bylevel.rename_axis(None, axis=0) 
        emsal_ozet_tablo_all = pd.merge(emsal_ozet_tablo, insaat_alan_bylevel, on='Level', how='left')

        emsal_ozet_tablo_all = emsal_ozet_tablo_all.rename(columns={'Area': 'İNŞAAT ALANI'})
        emsal_ozet_tablo_all['EMSAL ALANI'] = emsal_ozet_tablo_all['İNŞAAT ALANI'] - emsal_ozet_tablo_all['TOPLAM EMSAL DIŞI']
        desired_order = ['Level', 'İNŞAAT ALANI', 'TOPLAM EMSAL DIŞI', '30/70 KAPSAMINDA EMSAL DIŞI ALAN', 'DOĞRUDAN EMSAL DIŞI ALAN', 'EMSAL ALANI']
        emsal_ozet_tablo_all =emsal_ozet_tablo_all[desired_order]
        emsal_disi_30_toplam = round(emsal_ozet_tablo_all['30/70 KAPSAMINDA EMSAL DIŞI ALAN'].sum(),2)

        df_area_sum = df_emsal.groupby(["Level", 'Name', 'EmsalAlanTipi'])['Area'].sum().reset_index()
        net_alan = df_rooms_ozet[~df_rooms_ozet['Eklenti/Degil']].groupby('BlokBagimsizBolumNo')['Area'].sum().reset_index().rename(columns={'Area': 'NetAlan'})
        eklenti_net_alan = df_rooms_ozet[df_rooms_ozet['Eklenti/Degil']].groupby('BlokBagimsizBolumNo')['Area'].sum().reset_index().rename(columns={'Area': 'EklentiNetAlan'})
        brut_alan = df_bagimsiz_bolum[df_bagimsiz_bolum['Name'] == 'BAĞIMSIZ BÖLÜM'].groupby('BlokBagimsizBolumNo')['Area'].sum().reset_index().rename(columns={'Area': 'BrutAlan'})
        eklenti_brut_alan = df_bagimsiz_bolum[df_bagimsiz_bolum['Name'] == 'EKLENTİ ALAN'].groupby('BlokBagimsizBolumNo')['Area'].sum().reset_index().rename(columns={'Area': 'EklentiBrutAlan'})

        unique_blok_bagimsiz_bolum_no = pd.DataFrame(df_bagimsiz_bolum['BlokBagimsizBolumNo'].unique(), columns=['BlokBagimsizBolumNo'])

        final_df = unique_blok_bagimsiz_bolum_no \
            .merge(net_alan, on='BlokBagimsizBolumNo', how='left') \
            .merge(eklenti_net_alan, on='BlokBagimsizBolumNo', how='left') \
            .merge(brut_alan, on='BlokBagimsizBolumNo', how='left') \
            .merge(eklenti_brut_alan, on='BlokBagimsizBolumNo', how='left') \
            .fillna(0)

        metrekare_cetveli = final_df[final_df['BlokBagimsizBolumNo'] != '']
        sum_of_ortak_alan_area = df_bagimsiz_bolum[df_bagimsiz_bolum['Name'] == 'ORTAK ALAN']['Area'].sum()
        total_brut_alan = metrekare_cetveli['BrutAlan'].sum()

        distribution_factor = sum_of_ortak_alan_area / total_brut_alan

        metrekare_cetveli = metrekare_cetveli.copy()
        metrekare_cetveli.loc[:, 'OrtakAlan'] = metrekare_cetveli['BrutAlan'] * distribution_factor
        metrekare_cetveli.loc[:, 'ToplamBrutAlan'] = metrekare_cetveli[['BrutAlan', 'EklentiBrutAlan']].sum(axis=1)
        metrekare_cetveli.loc[:, 'GenelBrutAlan'] = metrekare_cetveli['ToplamBrutAlan'] + metrekare_cetveli['OrtakAlan']

        # Step 4: Calculating total_otopark_katsayisi
        def calculate_otopark_katsayisi(brut_alan):
            if brut_alan < 80:
                return 0.33
            elif brut_alan < 120:
                return 0.5
            elif brut_alan < 180:
                return 1
            else:
                return 2

        metrekare_cetveli.loc[:, 'OtoparkKatsayisi'] = metrekare_cetveli['BrutAlan'].apply(calculate_otopark_katsayisi)
        total_otopark_adedi = str(round(metrekare_cetveli['OtoparkKatsayisi'].sum())) +" adet"

        odasi_counts = df_rooms[df_rooms['Name'].str.contains('ODASI', na=False)].groupby('BlokBagimsizBolumNo').size().reset_index(name='OdaSayisi')
        metrekare_cetveli = metrekare_cetveli.merge(odasi_counts, on='BlokBagimsizBolumNo', how='left').fillna(0)
        metrekare_cetveli['OdaSayisi'] = metrekare_cetveli['OdaSayisi'].astype(int)

        metrekare_cetveli['SiginakIhtiyaci'] = metrekare_cetveli['OdaSayisi'].apply(lambda x: 2 if x == 1 else (3 if x == 2 else (4 if x >= 3 else 0)))
        total_siginak_ihtiyaci = str(metrekare_cetveli['SiginakIhtiyaci'].sum()) + " m²"

        metrekare_cetveli = metrekare_cetveli.drop(columns=['OtoparkKatsayisi', 'OdaSayisi', 'SiginakIhtiyaci'])
        metrekare_cetveli = metrekare_cetveli.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
        emsal_ozet_tablo_all = emsal_ozet_tablo_all.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
  
        if key == "metrekare_cetveli":
            return metrekare_cetveli
        elif key == "emsal_ozet_tablo_all":
             return emsal_ozet_tablo_all
        elif key == "total_siginak_ihtiyaci":
             return total_siginak_ihtiyaci    
        elif key == "total_otopark_adedi":
             return total_otopark_adedi    
        elif key == "arsa_alani":
             return arsa_alani  
        elif key == "taks":
             return taks  
        elif key == "kaks":
             return kaks  
        elif key == "emsal_kullanilan_toplam":
             return emsal_kullanilan_toplam          
        elif key == "insaat_alani_toplam":
             return insaat_alani_toplam  
        elif key == "emsal_hakki":
             return emsal_hakki  
        elif key == "emsal_30_minha_hakki":
             return emsal_30_minha_hakki  
        elif key == "emsal_disi_30_toplam":
             return emsal_disi_30_toplam                              

    @vkt.TableView("Metrekare Cetveli")
    def metrekare_view(self, params, **kwargs):
        metrekare_cetveli = self.get_data(params, "metrekare_cetveli")  # Fetch only metrekare_cetveli
        return vkt.TableResult(metrekare_cetveli)

    @vkt.TableView("Emsal Özet Tablosu")
    def emsal_view(self, params, **kwargs):
        emsal_ozet_tablo_all = self.get_data(params, "emsal_ozet_tablo_all")  # Fetch only emsal_ozet_tablo_all
        return vkt.TableResult(emsal_ozet_tablo_all)

    @vkt.IFCAndDataView("IFC and data view")
    def get_ifc_view(self, params, **kwargs):
        ifc_file = _use_correct_file(params)
        
        # Grouping the data as required
        data = vkt.DataGroup(
            # "Arsa Bilgileri" group
            arsa_bilgileri=vkt.DataItem(
                'Arsa Bilgileri', '', subgroup=vkt.DataGroup(
                    arsa_alani=vkt.DataItem('Arsa alanı', self.get_data(params, "arsa_alani")),
                    taks=vkt.DataItem('TAKS', self.get_data(params, "taks")),
                    kaks=vkt.DataItem('KAKS', self.get_data(params, "kaks")),
                    emsal_hakki=vkt.DataItem('Emsal hakkı', self.get_data(params, "emsal_hakki")),
                    emsal_30_minha=vkt.DataItem('%30 minha hakkı', self.get_data(params, "emsal_30_minha_hakki"))

                )
            ),
            
            # "Emsal Bilgileri" group
            emsal_bilgileri=vkt.DataItem(
                'Emsal Bilgileri', '', subgroup=vkt.DataGroup(
                    toplam_insaat_alani=vkt.DataItem('Toplam inşaat alanı', self.get_data(params, "insaat_alani_toplam")),
                    emsal_kullanilan=vkt.DataItem('Kullanılan emsal', self.get_data(params, "emsal_kullanilan_toplam")),
                    emsal_disi_30_kullanilan=vkt.DataItem('Kullanılan %30 minha', self.get_data(params, "emsal_disi_30_toplam"))
                )
            ),
            
            # "İhtiyaçlar" group
            ihtiyaclar=vkt.DataItem(
                'İhtiyaçlar', '', subgroup=vkt.DataGroup(
                    siginak_ihtiyaci=vkt.DataItem('Toplam sığınak ihtiyacı', self.get_data(params, "total_siginak_ihtiyaci")),
                    otopark_ihtiyaci=vkt.DataItem('Toplam otopark ihtiyacı', self.get_data(params, "total_otopark_adedi"))
                )
            )
        )
        
        
        return vkt.IFCAndDataResult(ifc_file, data)