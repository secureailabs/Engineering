using System.CommandLine;
using RestSharp;
namespace DatasetTool;

class UserSession
{
    private class LoginResponse
    {
        public string access_token { get; set; } = default!;
        public string refresh_token { get; set; } = default!;
        public string token_type { get; set; } = default!;
    }

    private class BasicInformation
    {
        public string name { get; set; } = default!;
        public string id { get; set; } = default!;
        public string state { get; set; } = default!;
    }

    private class DatasetList
    {
        public BasicInformation[] datasets { get; set; } = default!;
    }

    private class DataFederationList
    {
        public BasicInformation[] data_federations { get; set; } = default!;
    }

    private LoginResponse m_LoginResponse = default!;
    private RestClient m_client = default!;

    public UserSession(string ip_address, string email, string password)
    {
        // Create the client
        var client_options = new RestClientOptions("http://" + ip_address)
        {
            ThrowOnAnyError = true,
            MaxTimeout = 5000,
            RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true
        };
        m_client = new RestClient(client_options);

        // Create the request
        var request = new RestRequest("/login", Method.Post);
        request.AddHeader("Content-Type", "application/x-www-form-urlencoded");
        request.AddHeader("accept", "application/json");
        request.AddParameter("grant_type", "");
        request.AddParameter("username", email, true);
        request.AddParameter("password", password, true);
        request.AddParameter("scope", "");
        request.AddParameter("client_id", "");
        request.AddParameter("client_secret", "");

        // Login
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Login failed");
        }

        // Get the access token from the json response
        m_LoginResponse = Newtonsoft.Json.JsonConvert.DeserializeObject<LoginResponse>(response.Content)!;
        if (m_LoginResponse == null)
        {
            throw new Exception("Invalid response");
        }
    }

    public string GetFederationId(string data_federation_name)
    {
        // Create the request
        var request = new RestRequest("/data-federations", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the federations
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Data federation list fetch failed");
        }

        // Get the list of datasets
        var federation_list = Newtonsoft.Json.JsonConvert.DeserializeObject<DataFederationList>(response.Content)!;
        for (int i = 0; i < federation_list.data_federations.Count(); i++)
        {
            if (federation_list.data_federations[i].name == data_federation_name)
            {
                return federation_list.data_federations[i].id;
            }
        }

        return null!;
    }

    public string GetDatasetId(string dataset_name)
    {
        // Create the request
        var request = new RestRequest("/datasets", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the datasets
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Datasets list fetch failed");
        }

        // Get the list of datasets
        var datasets_list = Newtonsoft.Json.JsonConvert.DeserializeObject<DatasetList>(response.Content)!;
        for (int i = 0; i < datasets_list.datasets.Count(); i++)
        {
            if (datasets_list.datasets[i].name == dataset_name)
            {
                return datasets_list.datasets[i].id;
            }
        }

        return null!;
    }

    public string CreateDatasetAndAddToFederation(Dataset dataset, string data_federation_name)
    {
        string data_federation_id = GetFederationId(data_federation_name);
        if (data_federation_id == null)
        {
            throw new Exception("Data federation not found");
        }

        // Create json from the input
        string dataset_json = Newtonsoft.Json.JsonConvert.SerializeObject(dataset);

        // Register the dataset
        var request = new RestRequest("/datasets", Method.Post);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);
        request.AddJsonBody(dataset_json);

        // Post the dataset
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.Created || response.Content == null)
        {
            throw new Exception("Datasets register failed");
        }

        // Get the dataset id
        var register_dataset_response = Newtonsoft.Json.JsonConvert.DeserializeObject<BasicInformation>(response.Content)!;
        string dataset_id = register_dataset_response.id;

        // Add the dataset to the federation
        request = new RestRequest("/data-federations/" + data_federation_id + "/datasets/" + dataset_id, Method.Put);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Post the dataset
        response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.NoContent)
        {
            throw new Exception("Dataset Addition to Federation register failed");
        }

        return dataset_id;
    }

    public void RegisterDatasetVersion(string dataset_id, DatasetVersion dataset_version)
    {
        // Create json from the input
        string dataset_json = Newtonsoft.Json.JsonConvert.SerializeObject(dataset_version);

        // Register the dataset
        var request = new RestRequest("/datasets", Method.Post);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);
        request.AddJsonBody(dataset_json);

        // Post the dataset
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.Created || response.Content == null)
        {
            throw new Exception("Datasets register failed");
        }
    }
}
