using System.CommandLine;

namespace DatasetTool;

class Program
{
    static int Main(string[] args)
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
            var datasets = user_session.GetDatasets();
            bool dataset_found = false;
            foreach (var dataset in datasets)
            {
                // if (dataset.name == dataset_configuration.configuration.name)
                {
                    dataset_found = true;
                    System.Console.WriteLine("Dataset found");
                }
            }

            // If the dataset is not found, create it
            if (!dataset_found)
            {
                System.Console.WriteLine("Dataset not found, creating it");
                // user_session.CreateDatasetAndAddToFederation(dataset_configuration.configuration.name, dataset_configuration.configuration.description, dataset_configuration.configuration.data_federation, dataset_configuration.configuration.data_format);
            }

            // Create and Register the dataset version metadata
            // var dataset_version = new DatasetVersion(dataset_configuration, federations, datasets);
            // user_session.RegisterDatasetVersion(dataset, dataset_version);

            // Get the azure connection string
            // var azure_connection_string = user_session.GetConnectionStringForDatasetVersion();

            // Upload the dataset
            // dataset_version.UploadToAzure(azure_connection_string);

            // Report to the user the status of the upload
        },
        ip_address_option, email_option, password_option, file_option);

        return root_command.InvokeAsync(args).Result;
    }
}
