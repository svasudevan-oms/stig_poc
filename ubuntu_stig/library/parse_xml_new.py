from ansible.module_utils.basic import AnsibleModule
import xml.etree.ElementTree as ET

def parse_xml(file_path, device_ip):
    """
    Parses the given XML file and extracts rule ids, their results, and adds a device IP.
    :param file_path: Path to the XML file.
    :param device_ip: The device IP to add to each dictionary.
    :return: List of dictionaries with rule id, result, and device IP.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define the namespace
        namespace = {'cdf': 'http://checklists.nist.gov/xccdf/1.2'}

        # Extract rule results
        rule_results = []
        for rule in root.findall("cdf:rule-result", namespace):
            rule_id = rule.get("idref")
            result = rule.find("cdf:result", namespace).text
            rule_results.append({"rule_id": rule_id, "result": result, "device_ip": device_ip})

        return {"changed": False, "rule_results": rule_results}

    except ET.ParseError as e:
        return {"changed": False, "failed": True, "msg": f"XML parsing error: {str(e)}"}
    except Exception as e:
        return {"changed": False, "failed": True, "msg": f"Unexpected error: {str(e)}"}

def main():
    module_args = dict(
        xml_file=dict(type='str', required=True),
        device_ip=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    xml_file = module.params['xml_file']
    device_ip = module.params['device_ip']

    if not xml_file or not device_ip:
        module.fail_json(msg="The 'xml_file' and 'device_ip' parameters are required.")

    result = parse_xml(xml_file, device_ip)

    if "failed" in result and result["failed"]:
        module.fail_json(msg=result.get("msg", "An unknown error occurred"))
    else:
        module.exit_json(**result)

if __name__ == '__main__':
    main()
