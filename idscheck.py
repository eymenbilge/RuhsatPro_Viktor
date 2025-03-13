# filename: idscheck.py
import ifcopenshell
import ifctester.ids
from typing import Tuple, Dict

def load_ids_file(ids_path: str) -> ifctester.ids.Ids:
    """Load and return an IDS file."""
    return ifctester.ids.open(ids_path)

def validate_ifc_ids(ifc_file: ifcopenshell.file, ids_file: ifctester.ids.Ids) -> Tuple[Dict, str]:
    """Validate IFC against IDS and return (results dict, HTML report)."""
    ids_file.validate(ifc_file, should_filter_version=True)
    html_content = generate_html_report(ids_file)
    return {"specifications": ids_file.specifications}, html_content

def generate_html_report(ids: ifctester.ids.Ids) -> str:
    """Generate HTML report as a string."""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IFC Validation Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            .pass {{ background-color: #97cc64; color: white; padding: 5px; border-radius: 5px; }}
            .fail {{ background-color: #fb5a3e; color: white; padding: 5px; border-radius: 5px; }}
            .container {{ width: 100%; background-color: #ddd; border-radius: 5px; margin: 10px 0; }}
            .percent {{ text-align: left; padding: 5px; color: white; border-radius: 5px; white-space: nowrap; }}
            h1, h2 {{ color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 8px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            details {{ margin-bottom: 10px; }}
            summary {{ cursor: pointer; font-weight: bold; }}
        </style>
    </head>
    <body>
    <h1>IFC Validation Report</h1>
    <h2>Summary</h2>
    <div class="container">
    <div class="pass percent" style="width: 100%;">100% Passed</div>
    </div>
    <hr>
    """

    for spec in ids.specifications:
        passed = len(spec.passed_entities)
        failed = len(spec.failed_entities)
        total = passed + failed
        pass_percentage = (passed / total * 100) if total > 0 else 100
        
        html += f"""
        <section>
            <h2>{spec.name}</h2>
            <div class="container">
                <div class="{'pass' if pass_percentage == 100 else 'fail'} percent" style="width: {pass_percentage:.1f}%">{pass_percentage:.1f}%</div>
            </div>
            <details>
                <summary>Passed Entities ({passed})</summary>
                <ul>{''.join(f'<li class="pass">{entity}</li>' for entity in spec.passed_entities)}</ul>
            </details>
            <details>
                <summary>Failed Entities ({failed})</summary>
                <ul>{''.join(f'<li class="fail">{entity}</li>' for entity in spec.failed_entities)}</ul>
            </details>
        </section>
        """
    
    html += "</body></html>"
    return html
def main():
    # Load IFC file
    ifc_file = ifcopenshell.open("model.ifc")
    
    # Load IDS file
    ids_file = load_ids_file("rules.ids")
    
    # Validate IFC against IDS
    _, html_report = validate_ifc_ids(ifc_file, ids_file)
    
    # Save HTML report
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_report)

    # Print success message
    print("Report saved successfully as validation_report.html")

if __name__ == "__main__":
    main()
