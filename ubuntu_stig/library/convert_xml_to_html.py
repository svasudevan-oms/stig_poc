#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
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

    return {"changed": True, "msg": f"HTML file generated as {html_file_path}"}


def run_module():
    # Define the argument spec
    module_args = dict(
        xml_file_path=dict(type='str', required=True),
        html_file_path=dict(type='str', required=True)
    )

    # Instantiate the Ansible module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # Run the XML to HTML conversion
    result = convert_xml_to_html(module.params['xml_file_path'], module.params['html_file_path'])

    # Return the result
    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
