# -----------------------------------------------------------
#
# Azure Template Managment Helpers
#
# -----------------------------------------------------------


def get_az_template_payload():
    """
    Helper to return template of azure template payload

    :return: az_template_payload
    :rtype: dict
    """
    az_template_payload = {
        "TemplateData": {
            "Name": "Test_template",
            "Description": "Test_template_spices",
            "SubscriptionID": "3d2b9951-a0c8-4dc3-8114-2776b047b15c",
            "Secret": "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2",
            "TenantID": "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8",
            "ApplicationID": "4f909fab-ad4c-4685-b7a9-7ddaae4efb22",
            "ResourceGroup": "ScratchpadRg",
            "VirtualNetwork": "Vnet",
            "HostRegion": "eastus",
            "NetworkSecurityGroup": "NsgTemp",
            "VirtualMachineImage": "testing_vm",
        },
    }
    return az_template_payload
