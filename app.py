import viktor as vkt
from viktor import File
from pathlib import Path
from viktor.parametrization import FileField, Text
from ifcopenshell import open as ifc_open
from func import calculate_dataframes
from viktor import WebResult
from idscheck import load_ids_file, validate_ifc_ids


class AppCache:
    """Central cache manager for IFC data."""
    
    def __init__(self):
        self.ifc_model = None
        self.site_data = None
        self.calculation_results = None
        self.ids_validation = None
        
    def clear(self):
        """Clear all cached data."""
        self.ifc_model = None
        self.site_data = None
        self.calculation_results = None
        self.ids_validation = None


def _use_correct_file(params) -> File:
    """Returns either an uploaded file or a default one."""
    if params.page_1.ifc_upload:
        return params.page_1.ifc_upload.file
    return File.from_path(Path(__file__).parent / "model.ifc")


def _get_cache(params):
    """Get or create the cache object."""
    if not hasattr(params, "_app_cache"):
        params._app_cache = AppCache()
    return params._app_cache


def _load_ifc_file(params):
    """Load IFC file with caching."""
    cache = _get_cache(params)
    
    # Return cached model if available
    if cache.ifc_model is not None:
        return cache.ifc_model
    
    try:
        ifc_upload = _use_correct_file(params)
        ifc_path = ifc_upload.source
        model = ifc_open(ifc_path)
        cache.ifc_model = model
        return model
    except Exception as e:
        print(f"Error loading IFC file: {e}")
        return None


def _extract_site_data(model):
    """Extract site data from IFC model."""
    if model is None:
        return {
            "arsa_alani": 0.0,
            "taks": 0.0,
            "kaks": 0.0,
            "emsal_hakki": 0.0,
            "emsal_30_minha_hakki": 0.0
        }
    
    ifc_site = model.by_type("IfcSite")[0]
    pset_arsa_bilgileri = {"ArsaAlani": None, "TAKS": None, "KAKS": None}
    
    for rel in ifc_site.IsDefinedBy:
        if rel.is_a("IfcRelDefinesByProperties"):
            property_set = rel.RelatingPropertyDefinition
            for prop in property_set.HasProperties:
                if prop.Name in pset_arsa_bilgileri:
                    value = prop.NominalValue.wrappedValue
                    pset_arsa_bilgileri[prop.Name] = float(value.split()[0]) if "m²" in value else float(value)
    
    arsa_alani = float(pset_arsa_bilgileri["ArsaAlani"] or 0.0)
    taks = float(pset_arsa_bilgileri["TAKS"] or 0.0)
    kaks = float(pset_arsa_bilgileri["KAKS"] or 0.0)
    emsal_hakki = arsa_alani * kaks
    emsal_30_minha_hakki = emsal_hakki * 0.3
    
    return {
        "arsa_alani": arsa_alani,
        "taks": taks,
        "kaks": kaks,
        "emsal_hakki": emsal_hakki,
        "emsal_30_minha_hakki": emsal_30_minha_hakki
    }


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

    page_2 = vkt.Page('IDS Validation', views=['ids_validation_view'])
    page_3 = vkt.Page('Emsal Özeti', views=['emsal_view'])
    page_4 = vkt.Page('Metrekare Cetveli', views=['metrekare_view'])


class Controller(vkt.ViktorController):
    label = "My Entity Type"
    parametrization = Parametrization(width=30)

    def get_data(self, params, key: str):
        """Get data with comprehensive caching strategy."""
        cache = _get_cache(params)
        
        # Get site data (with caching)
        if key in ["arsa_alani", "taks", "kaks", "emsal_hakki", "emsal_30_minha_hakki"]:
            if cache.site_data is None:
                model = _load_ifc_file(params)
                cache.site_data = _extract_site_data(model)
            return cache.site_data[key]
        
        # Get calculation results (with caching)
        if key in ["metrekare_cetveli", "emsal_ozet_tablo_all", "total_siginak_ihtiyaci", "total_otopark_ihtiyaci"]:
            if cache.calculation_results is None:
                model = _load_ifc_file(params)
                # This is an expensive operation, do it only once
                cache.calculation_results = calculate_dataframes(model, Path(__file__).parent / "room_data.csv")
            return cache.calculation_results[key]
        
        return None

    @vkt.WebView("IDS Validation Report", duration_guess=5)
    def ids_validation_view(self, params, **kwargs):
        """IDS validation view with caching."""
        cache = _get_cache(params)
        
        # Return cached validation if available
        if cache.ids_validation is not None:
            return WebResult(html=cache.ids_validation)
        
        # Get files and validate
        try:
            model = _load_ifc_file(params)
            ids_file = File.from_path(Path(__file__).parent / "rules.ids")
            ids = load_ids_file(ids_file.source)
            _, html_report = validate_ifc_ids(model, ids)
            
            # Cache the result
            cache.ids_validation = html_report
            return WebResult(html=html_report)
        except Exception as e:
            return WebResult(html=f"<h2>Validation Error</h2><p>{str(e)}</p>")

    @vkt.TableView("Metrekare Cetveli", duration_guess=1)
    def metrekare_view(self, params, **kwargs):
        """Metrekare cetveli view."""
        metrekare_cetveli = self.get_data(params, "metrekare_cetveli")
        return vkt.TableResult(metrekare_cetveli)

    @vkt.TableView("Emsal Özet Tablosu", duration_guess=1)
    def emsal_view(self, params, **kwargs):
        """Emsal özet view."""
        emsal_ozet_tablo_all = self.get_data(params, "emsal_ozet_tablo_all")
        return vkt.TableResult(emsal_ozet_tablo_all)

    @vkt.IFCAndDataView("IFC and data view", duration_guess=10)
    def get_ifc_view(self, params, **kwargs):
        """IFC view with all required data."""
        # Using the original file to show IFC model
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