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
        public Guid id { get; set; } = default!;
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

    private class ConnectionStringResponse
    {
        public string Guid { get; set; } = default!;
        public string connection_string { get; set; } = default!;
    }

    private LoginResponse m_LoginResponse = default!;
    private RestClient m_client = default!;

    /// <summary>
    /// Constructor for the UserSession class
    /// </summary>
    /// <param name="ip_address"> IP Address for the SAIL Platform Services </param>
    /// <param name="email"> Email of the data submitter </param>
    /// <param name="password"> Password of the data submitter </param>
    /// <exception cref="Exception"></exception>
    public UserSession(string ip_address, string email, string password)
    {
        // Create the client
        var client_options = new RestClientOptions("https://" + ip_address)
        {
            ThrowOnAnyError = true,
            MaxTimeout = 5000,
            // TODO: IMP!! Important!! Remove this line after real certificates are used.
            RemoteCertificateValidationCallback = (sender, certificate, chain, sslPolicyErrors) => true
        };
        System.Console.WriteLine("#####################################################################################################");
        System.Console.WriteLine("SSL Certificate validataion is disabled for this session. This is not recommended for production use.");
        System.Console.WriteLine("#####################################################################################################");
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

    /// <summary>
    /// Get the list of data federation with the provided name
    /// </summary>
    /// <param name="data_federation_name"></param>
    /// <returns> Guid of the data federation with the input name</returns>
    /// <exception cref="Exception"></exception>
    public Guid GetFederationId(string data_federation_name)
    {
        // Create the request
        var request = new RestRequest("/data-federations", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the federations
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Data federation list fetch failed.\n" + response.Content);
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

        return Guid.Empty;
    }

    /// <summary>
    /// Get the Guid of dataset with the given name
    /// </summary>
    /// <param name="dataset_name"> Name of the dataset for which id is requested </param>
    /// <returns> Guid of the dataset </returns>
    /// <exception cref="Exception">  </exception>
    public Guid GetDatasetId(string dataset_name)
    {
        // Create the request
        var request = new RestRequest("/datasets", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the datasets
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Datasets list fetch failed. \n" + response.Content);
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

        return Guid.Empty;
    }

    /// <summary>
    /// Creat a new dataset with the given name and description and add it te the given data federation
    /// </summary>
    /// <param name="dataset"> Dataset object </param>
    /// <param name="data_federation_name"> Name of the data federation to add the dataset </param>
    /// <returns> Guid of the newly created dataset </returns>
    /// <exception cref="Exception"></exception>
    public Guid CreateDatasetAndAddToFederation(Dataset dataset, string data_federation_name)
    {
        Guid data_federation_id = GetFederationId(data_federation_name);

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
            throw new Exception("Datasets register failed. \n." + response.Content);
        }

        // Get the dataset id
        var register_dataset_response = Newtonsoft.Json.JsonConvert.DeserializeObject<BasicInformation>(response.Content)!;
        Guid dataset_id = register_dataset_response.id;

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

    /// <summary>
    /// Register the dataset version metadata with the platform and get the version id
    /// </summary>
    /// <param name="dataset_id"> Dataset ID for the version </param>
    /// <param name="dataset_version_metadata"></param>
    /// <returns> Guid of the dataset version </returns>
    /// <exception cref="Exception"></exception>
    public Guid RegisterDatasetVersion(Guid dataset_id, string dataset_version_metadata)
    {
        // Get the dataset information and wait for it to be active before registering the version
        // We will try 10 times with 5 seconds delay between each try
        int count = 10;
        while (count > 0)
        {
            var dataset_request = new RestRequest("/datasets/" + dataset_id, Method.Get);
            dataset_request.AddHeader("accept", "application/json");
            dataset_request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

            // Get the dataset
            var dataset_response = m_client.Execute(dataset_request);
            if (dataset_response.StatusCode != System.Net.HttpStatusCode.OK || dataset_response.Content == null)
            {
                throw new Exception("Dataset fetch failed. \n" + dataset_response.Content);
            }

            // Get the dataset information
            var dataset = Newtonsoft.Json.JsonConvert.DeserializeObject<Dataset>(dataset_response.Content)!;
            if (dataset.state == "ACTIVE")
            {
                break;
            }

            count--;
            System.Threading.Thread.Sleep(5000);
        }
        if (count == 0)
        {
            throw new Exception("Dataset is not ready after 10 tries. Contact Secure AI Labs support.");
        }

        // Register the dataset version
        var request = new RestRequest("/dataset-versions", Method.Post);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);
        request.AddJsonBody(dataset_version_metadata);

        // Post the dataset and register
        var response = m_client.Execute(request);
        if (response.Content == null)
        {
            throw new Exception("Dataset version register failed. \n Response Code: " + response.StatusCode);
        }
        else if (response.StatusCode == System.Net.HttpStatusCode.OK)
        {
            System.Console.WriteLine("Dataset version already exists. Will only be allowed to upload the file if not already uploaded");
        }
        else if (response.StatusCode != System.Net.HttpStatusCode.Created)
        {
            throw new Exception("Dataset version register failed. \n" + response.Content);
        }

        // Get the dataset version id
        var register_dataset_version_response = Newtonsoft.Json.JsonConvert.DeserializeObject<BasicInformation>(response.Content)!;

        return register_dataset_version_response.id;
    }

    /// <summary>
    /// Get a SAS connection string for the dataset version
    /// </summary>
    /// <param name="dataset_version_id"> Dataset version for which SAS token is to be generated"/> </param>
    /// <returns></returns>
    /// <exception cref="Exception"></exception>
    public string GetConnectionStringForDatasetVersion(Guid dataset_version_id)
    {
        // Proceed only if the dataset version is in the ACTIVE state
        // We will try 10 times with 5 seconds delay between each try
        int count = 10;
        while (count > 0)
        {
            var dataset_version_request = new RestRequest("/dataset-versions/" + dataset_version_id, Method.Get);
            dataset_version_request.AddHeader("accept", "application/json");
            dataset_version_request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

            // Get the dataset version
            var dataset_version_response = m_client.Execute(dataset_version_request);
            if (dataset_version_response.StatusCode != System.Net.HttpStatusCode.OK || dataset_version_response.Content == null)
            {
                throw new Exception("Dataset version fetch failed. \n" + dataset_version_response.Content);
            }

            // Get the dataset version information
            var dataset_version = Newtonsoft.Json.JsonConvert.DeserializeObject<DatasetVersionMetadata>(dataset_version_response.Content)!;
            if (dataset_version.state == "NOT_UPLOADED")
            {
                break;
            }

            count--;
            System.Threading.Thread.Sleep(5000);
        }
        if (count == 0)
        {
            throw new Exception("Timeout. Dataset version is not ready after 10 tries. Contact Secure AI Labs Supoort");
        }

        // Get the dataset version connection string
        var request = new RestRequest("/dataset-versions/" + dataset_version_id.ToString() + "/connection-string", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the dataset version
        var response = m_client.Execute(request);
        if (response.StatusCode == System.Net.HttpStatusCode.BadRequest)
        {
            throw new Exception("Dataset version not found or already uploaded using the SAS token. \n" + response.Content);
        }
        else if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Dataset version fetch failed.\n" + response.Content);
        }

        // Get the dataset version
        var connection_string_response = Newtonsoft.Json.JsonConvert.DeserializeObject<ConnectionStringResponse>(response.Content)!;

        return connection_string_response.connection_string;
    }

    /// <summary>
    /// Mark the dataset version as uploaded on the SAIL platform services
    /// </summary>
    /// <param name="dataset_version_id"> the dataset version id to be marked as ready </param>
    /// <exception cref="Exception"></exception>
    public void MarkDatasetVersionAsActive(Guid dataset_version_id)
    {
        // Put the dataset version
        var request = new RestRequest("/dataset-versions/" + dataset_version_id.ToString(), Method.Put);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        request.AddJsonBody("{\"state\": \"ACTIVE\"}");

        // Execute the request
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.NoContent)
        {
            throw new Exception("Dataset version state update failed.\n" + response.Content);
        }
    }
}
