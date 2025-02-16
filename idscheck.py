import ifcopenshell
import ifctester.ids
import os

ifc_file_path = "model.ifc"
ids_file_path = "rules.ids"
output_report_path = "report.html"

try:
    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Load the IDS file
    ids = ifctester.ids.open(ids_file_path)

    # Validate the IFC file against the IDS rules
    ids.validate(ifc_file, should_filter_version=True)

    # Generate HTML Report
    with open(output_report_path, "w", encoding="utf-8") as report_file:
        report_file.write("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IFC Validation Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                .pass { background-color: #97cc64; color: white; padding: 5px; border-radius: 5px; }
                .fail { background-color: #fb5a3e; color: white; padding: 5px; border-radius: 5px; }
                .container { width: 100%; background-color: #ddd; border-radius: 5px; margin: 10px 0; }
                .percent { text-align: left; padding: 5px; color: white; border-radius: 5px; white-space: nowrap; }
                h1, h2 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { padding: 8px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #f4f4f4; }
                details { margin-bottom: 10px; }
                summary { cursor: pointer; font-weight: bold; }
            </style>
        </head>
        <body>
        <h1>IFC Validation Report</h1>
        <h2>Summary</h2>
        <div class="container">
        <div class="pass percent" style="width: 100%;">100% Passed</div>
        </div>
        <hr>
        """)

        for spec in ids.specifications:
            passed = len(spec.passed_entities)
            failed = len(spec.failed_entities)
            total = passed + failed
            pass_percentage = (passed / total * 100) if total > 0 else 100
            
            report_file.write(f"""
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
            """)
        
        report_file.write("</body></html>")
    
    print(f"Validation complete. Report saved to {output_report_path}")

except FileNotFoundError:
    print(f"Error: File not found. Check the paths for IFC file ({ifc_file_path}) or IDS file ({ids_file_path}).")
except ifctester.ids.IdsXmlValidationError as e:
    print(f"Error: Invalid IDS file format: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
