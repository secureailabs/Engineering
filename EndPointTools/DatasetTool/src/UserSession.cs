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

    private LoginResponse m_LoginResponse = default!;
    private RestClient m_client = default!;

    public UserSession(string ip_address, string email, string password)
    {
        // Create the client
        var client_options = new RestClientOptions("https://" + ip_address)
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

    public List<string> GetFederations(string data_federation_name)
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

        return new List<string>();
    }

    public List<string> GetDatasets()
    {
        // Create the request
        var request = new RestRequest("/datasets", Method.Get);
        request.AddHeader("accept", "application/json");
        request.AddHeader("Authorization", "Bearer " + m_LoginResponse.access_token);

        // Get the federations
        var response = m_client.Execute(request);
        if (response.StatusCode != System.Net.HttpStatusCode.OK || response.Content == null)
        {
            throw new Exception("Datasets list fetch failed");
        }

        return new List<string>();
    }
}
