import xml.etree.ElementTree as ET

def convert_xml_to_html(xml_file_path, html_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract namespace and register it
    namespace = {"cdf": "http://checklists.nist.gov/xccdf/1.2"}
    ET.register_namespace("cdf", namespace["cdf"])

    # Start HTML structure
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Test Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Test Results</h1>
        <p><strong>Test ID:</strong> {root.get('id')}</p>
        <p><strong>End Time:</strong> {root.get('end-time')}</p>
        <p><strong>Target:</strong> {root.find('cdf:target', namespace).text}</p>

        <table>
            <tr>
                <th>Rule ID</th>
                <th>Result</th>
            </tr>
    """

    # Iterate over rule-result elements to build rows
    for rule_result in root.findall('cdf:rule-result', namespace):
        rule_id = rule_result.get('idref')
        result = rule_result.find('cdf:result', namespace).text
        html += f"""
            <tr>
                <td>{rule_id}</td>
                <td>{result}</td>
            </tr>
        """

    # Close HTML structure
    html += """
        </table>
    </body>
    </html>
    """

    # Save HTML to a file
    with open(html_file_path, "w") as file:
        file.write(html)

    print(f"HTML file generated as {html_file_path}")

# Example usage
xml_file_path = 'stig_result/results.xml'  # Change this to your XML file path
html_file_path = 'stig_result/output.html'  # Change this if you want a different output file name
convert_xml_to_html(xml_file_path, html_file_path)
