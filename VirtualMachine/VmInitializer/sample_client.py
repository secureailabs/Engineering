import requests

intialization_vector_file = "InitializationVector.json"
bin_package_file = "package.tar.gz"

headers = {"accept": "application/json"}
files = {
    "initialization_vector": open(intialization_vector_file, "rb"),
    "bin_package": open(bin_package_file, "rb"),
}

# response = requests.get("https://52.152.149.193:9090/docs", headers=headers, files=files, verify=False)
response = requests.put("http://127.0.0.1:9090/initialization-data", headers=headers, files=files, verify=False)
