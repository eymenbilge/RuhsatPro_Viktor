import viktor as vkt
from viktor import File
from pathlib import Path
import time
from viktor.parametrization import (
    FileField,
    Text,

)
import ifcopenshell
import pandas as pd
import time
from viktor.core import progress_message
from func import calculate_dataframes
#from viktor import WebResult
#from idscheck import load_ids_file, validate_ifc_ids


PROGRESS_MESSAGE_DELAY = 10  # Adjust this based on your desired delay


def _use_correct_file(params) -> File:
    """
    Returns either an uploaded file or a default one
    """
    if params.page_1.ifc_upload:
        return params.page_1.ifc_upload.file
    return File.from_path(Path(__file__).parent / "model.ifc")

def _load_ifc_file(params):
    """Load ifc file into ifc model object."""
    ifc_upload = _use_correct_file(params)
    ifc_path = ifc_upload.copy().source
    model = ifcopenshell.open(ifc_path)
    return model

def get_filtered_ifc_file(params, **kwargs) -> File:
    """
    Filters an IFC file based on multiple IfcSpace ObjectType values.
    """
    selected_types = params.page_1.option  # This is now a list of selected options

    progress_message("Load IFC file...")
    model = _load_ifc_file(params)

    delta_time = PROGRESS_MESSAGE_DELAY + 1
    start = time.time()

    # Filter IfcSpace objects based on selected ObjectType values
    for space in model.by_type("IfcSpace"):
        if space.ObjectType not in selected_types:  # Check against a list
            if delta_time > PROGRESS_MESSAGE_DELAY:
                start = time.time()
                progress_message(f"Removing space: {space.ObjectType}")
            model.remove(space)
        delta_time = time.time() - start

    # Optionally filter IfcElement and IfcSite, if needed
    for t in ("IfcElement", "IfcSite"):
        for element in model.by_type(t):
            if delta_time > PROGRESS_MESSAGE_DELAY:
                start = time.time()
                progress_message(f"Removing element: {element.get_info()['type']}")
            model.remove(element)
            delta_time = time.time() - start

    progress_message("Exporting file...")
    file = File()
    model.write(file.source)
    
    return file

    
    return file

class Parametrization(vkt.Parametrization):
    page_1 = vkt.Page('IFC', views=["get_ifc_view"])


    page_1.text1 = Text(
        """
# IFC veri şeması ile yapı ruhsat süreçleri ve emsal hesaplarının kontrolü

        """
    )
    page_1.text2 = Text(
        """
## Dosya yükleme
Gerekli parametrelerin doldurulmuş olduğu modeli buradan yükleyebilirsiniz.
Bir dosya yüklemesi yapılmaz ise uygulama varsayılan IFC dosyası'nı kullanır.
        """
    )

    page_1.ifc_upload = FileField(
        "Upload model",
        file_types=[".ifc"],
        flex=100,
        max_size=45_000_000,
        description="If you leave this empty, the app will use a default file.",
    )

    page_1.option = vkt.MultiSelectField('Gösterimi yapılacak şemalar', options=['Net Alan', 'Emsal Alan', 'Brüt Alan'], default=['Net Alan'])

    #page_2 = vkt.Page('IDS Validation', views=['ids_validation_view'])
    page_3 = vkt.Page('Emsal Özeti', views=['emsal_view'])
    page_4 = vkt.Page('Metrekare Cetveli', views=['metrekare_view'])

class Controller(vkt.ViktorController):
    label = "My Entity Type"
    parametrization = Parametrization(width=30)
    

    @staticmethod
    def get_data(params, key: str):
        model = _load_ifc_file(params)
        ifc_site = model.by_type("IfcSite")[0]
        # Dictionary to store the required values
        pset_arsa_bilgileri = {"ArsaAlani": None, "TAKS": None, "KAKS": None}
        # Loop through property sets of the IfcSite element
        for rel in ifc_site.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByProperties"):
                property_set = rel.RelatingPropertyDefinition
                # Loop through properties in the property set
                for prop in property_set.HasProperties:
                    if prop.Name in pset_arsa_bilgileri:
                        # Extract the numeric value and handle potential units like 'm²'
                        value = prop.NominalValue.wrappedValue
                        pset_arsa_bilgileri[prop.Name] = float(value.split()[0]) if "m²" in value else float(value)

        # Assign extracted values to variables
        arsa_alani, taks, kaks = pset_arsa_bilgileri["ArsaAlani"], pset_arsa_bilgileri["TAKS"], pset_arsa_bilgileri["KAKS"]
        emsal_hakki=arsa_alani*kaks
        emsal_30_minha_hakki =emsal_hakki*.3
        arsa_alani = float(arsa_alani) if arsa_alani is not None else 0.0
        taks = float(taks) if taks is not None else 0.0
        kaks = float(kaks) if kaks is not None else 0.0
        emsal_hakki = float(emsal_hakki)
        emsal_30_minha_hakki = float(emsal_30_minha_hakki)

        results_func = calculate_dataframes(model, "room_data.csv")
   
        if key == "metrekare_cetveli":
            return results_func["metrekare_cetveli"]
        elif key == "emsal_ozet_tablo_all":
             return results_func["emsal_ozet_tablo_all"]
        elif key == "total_siginak_ihtiyaci":
             return results_func["total_siginak_ihtiyaci"]   
        elif key == "total_otopark_ihtiyaci":
             return results_func["total_otopark_ihtiyaci"]   
        elif key == "arsa_alani":
             return arsa_alani  
        elif key == "taks":
             return taks  
        elif key == "kaks":
             return kaks  
        elif key == "emsal_hakki":
             return emsal_hakki  
        elif key == "emsal_30_minha_hakki":
             return emsal_30_minha_hakki  
    """
    @vkt.WebView("IDS Validation Report", duration_guess=5)
    def ids_validation_view(self, params, **kwargs):
        # Get files
        ifc_file = _load_ifc_file(params)
        ids_file = File.from_path(Path(__file__).parent / "rules.ids")
        
        # Validate
        try:
            ids = load_ids_file(ids_file.source)
            _, html_report = validate_ifc_ids(ifc_file, ids)
            return WebResult(html=html_report)
        except Exception as e:
            return WebResult(html=f"<h2>Validation Error</h2><p>{str(e)}</p>")
    """    
    @vkt.TableView("Metrekare Cetveli",duration_guess=1)
    def metrekare_view(self, params, **kwargs):
        metrekare_cetveli = self.get_data(params, "metrekare_cetveli")  # Fetch only metrekare_cetveli
        return vkt.TableResult(metrekare_cetveli)

    @vkt.TableView("Emsal Özet Tablosu", duration_guess=1)
    def emsal_view(self, params, **kwargs):
        emsal_ozet_tablo_all = self.get_data(params, "emsal_ozet_tablo_all")  # Fetch only emsal_ozet_tablo_all
        return vkt.TableResult(emsal_ozet_tablo_all)

    @vkt.IFCAndDataView("IFC and data view", duration_guess=10)
    def get_ifc_view(self, params, **kwargs):
        if params.page_1.option:
            model = get_filtered_ifc_file(params)
        else:
            model = _use_correct_file(params)
        
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
            

            
            # "İhtiyaçlar" group
            ihtiyaclar=vkt.DataItem(
                'İhtiyaçlar', '', subgroup=vkt.DataGroup(
                    siginak_ihtiyaci=vkt.DataItem('Toplam sığınak ihtiyacı', self.get_data(params, "total_siginak_ihtiyaci")),
                    otopark_ihtiyaci=vkt.DataItem('Toplam otopark ihtiyacı', self.get_data(params, "total_otopark_ihtiyaci"))
                )
            )
        )
        
        
        return vkt.IFCAndDataResult(model, data)
    