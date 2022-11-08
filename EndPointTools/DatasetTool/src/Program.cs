using System.CommandLine;

namespace DatasetTool;

class Program
{
    static int Main(string[] args)
    {
        try
        {
            // Get all the command line arguments
            var ip_address_option = new Option<string>(
                name: "--ip",
                description: "The IP address of the server")
            { IsRequired = true };

            var email_option = new Option<string>(
                name: "--email",
                description: "The email address to use for authentication")
            { IsRequired = true };

            var password_option = new Option<string>(
                name: "--password",
                description: "The password to use for authentication")
            { IsRequired = true };

            var file_option = new Option<FileInfo>(
                name: "--config",
                description: "The file with the dataset configuration")
            { IsRequired = true };

            var root_command = new RootCommand("App to register and upload the datasets to Secure AI Labs pltform");
            root_command.AddOption(email_option);
            root_command.AddOption(password_option);
            root_command.AddOption(file_option);
            root_command.AddOption(ip_address_option);

            root_command.SetHandler((string ip_address, string email, string password, FileInfo file) =>
            {
                // Read the configuration and make sure it is valid
                var dataset_configuration = new DatasetConfiguration(file);

                // Create a user session object
                var user_session = new UserSession(ip_address, email, password);

                // Get the list of the datasets
                Guid dataset_id = user_session.GetDatasetId(dataset_configuration.m_configuration.dataset.name);

                // If the dataset is not found, create it
                if (dataset_id.CompareTo(Guid.Empty) == 0)
                {
                    System.Console.WriteLine("Dataset not found, creating it");
                    dataset_id = user_session.CreateDatasetAndAddToFederation(dataset_configuration.m_configuration.dataset, dataset_configuration.m_configuration.data_federation);
                }

                // Create and Register the dataset version metadata
                var dataset_version = new DatasetVersion(dataset_configuration.m_configuration.dataset_version.name,
                    dataset_configuration.m_configuration.dataset_version.description,
                    dataset_configuration.m_configuration.dataset_version.tags,
                    dataset_id);

                // Add all the dataset files
                foreach (var data_source in dataset_configuration.m_configuration.data_source)
                {
                    dataset_version.AddDatasetFile(data_source);
                }

                // Register the dataset version with the portal
                Guid dataset_version_id = user_session.RegisterDatasetVersion(dataset_id, dataset_version.GetMetadataJson());

                // Update the dataset version with the dataset files
                dataset_version.dataset_version_id = dataset_version_id;

                // Get the azure connection string
                var azure_connection_string = "";
                // var azure_connection_string = user_session.GetConnectionStringForDatasetVersion(dataset_version_id);
                if (azure_connection_string == null)
                {
                    throw new Exception("Could not get the connection string for the dataset version");
                }

                // Upload the dataset
                dataset_version.UploadToAzure(azure_connection_string, "DhA5lu3lYGnvOIztQn/IGLX6ar1T25AuVaMMuwLuJGs=");

                // Mark the dataset version as ready
                user_session.MarkDatasetVersionAsActive(dataset_version_id);

                // Report to the user the status of the upload
                System.Console.WriteLine("Dataset Version uploaded successfully!!");
            },
            ip_address_option, email_option, password_option, file_option);

            return root_command.InvokeAsync(args).Result;
        }
        catch (System.Exception exception)
        {
            System.Console.WriteLine(exception.Message);
            return 1;
        }
    }
}
