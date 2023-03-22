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
                try
                {
                    // Read the configuration and make sure it is valid
                    var dataset_configuration = new DatasetConfiguration(file);

                    // Create a user session object
                    var user_session = new UserSession(ip_address, email, password);

                    // Get the data federation id
                    ModelDataFederation data_federation = user_session.GetFederation(dataset_configuration.m_configuration.data_federation);
                    if (data_federation == null)
                    {
                        throw new Exception("Data federation not found");
                    }

                    // Data federation model should not be empty
                    if (data_federation.data_model == null || data_federation.data_model.Length == 0)
                    {
                        throw new Exception("Data federation model is not set. Kindly ask the data federation owner to set the model.");
                    }

                    // Check if the dataset configuration format matches the data federation format
                    if (dataset_configuration.m_configuration.dataset.format != data_federation.data_format)
                    {
                        throw new Exception("Dataset format does not match the data federation designated format");
                    }

                    // Get the list of the datasets
                    Guid dataset_id = user_session.GetDatasetId(dataset_configuration.m_configuration.dataset.name);
                    // If the dataset is not found, create it
                    if (dataset_id.CompareTo(Guid.Empty) == 0)
                    {
                        System.Console.WriteLine("Dataset not found, creating it");
                        dataset_id = user_session.CreateDatasetAndAddToFederation(dataset_configuration.m_configuration.dataset, data_federation.id);
                    }

                    // Create and Register the dataset version metadata
                    var dataset_version = new DatasetVersion(dataset_configuration.m_configuration.dataset_version.name,
                        dataset_configuration.m_configuration.dataset_version.description,
                        dataset_configuration.m_configuration.dataset_version.tags,
                        dataset_id,
                        dataset_configuration.m_configuration.dataset.format);

                    // Add all the dataset files
                    foreach (var data_source in dataset_configuration.m_configuration.data_source)
                    {
                        dataset_version.AddDatasetSource(data_source);
                    }

                    // Register the dataset version with the portal
                    Guid dataset_version_id = user_session.RegisterDatasetVersion(dataset_id, dataset_version.GetMetadataJson());

                    // Update the dataset version with the dataset files
                    dataset_version.m_dataset_version_id = dataset_version_id;

                    // Get the azure connection string
                    var azure_connection_string = user_session.GetConnectionStringForDatasetVersion(dataset_version_id);
                    if (azure_connection_string == null)
                    {
                        throw new Exception("Could not get the connection string for the dataset version");
                    }

                    // Get the encryption key from the backend
                    string encryption_key = user_session.GetEncryptionKeyForDataset(dataset_id, data_federation.id);

                    // Create a dataset header
                    ModelDatasetHeader dataset_header = new ModelDatasetHeader();
                    dataset_header.dataset_id = dataset_id;
                    dataset_header.dataset_name = dataset_configuration.m_configuration.dataset.name;
                    dataset_header.data_federation_id = data_federation.id;
                    dataset_header.data_federation_name = data_federation.name;
                    if (dataset_configuration.m_configuration.dataset.format == "FHIR")
                    {
                        dataset_header.dataset_packaging_format = "fhirv1";
                    }
                    else if (dataset_configuration.m_configuration.dataset.format == "CSV")
                    {
                        dataset_header.dataset_packaging_format = "csvv1";
                    }
                    else
                    {
                        throw new Exception("Unknown dataset format");
                    }

                    // Upload the dataset
                    dataset_version.ValidateAndUploadToAzure(azure_connection_string, encryption_key, dataset_header, data_federation.data_model);

                    // Mark the dataset version as ready
                    user_session.MarkDatasetVersionAsActive(dataset_version_id);

                    // Report to the user the status of the upload
                    System.Console.WriteLine("Dataset Version uploaded successfully!!");

                }
                catch (Exception exception)
                {
                    var default_color = Console.ForegroundColor;
                    Console.ForegroundColor = ConsoleColor.Red;
                    System.Console.WriteLine("FAILED:" + exception.Message);
                    Console.ForegroundColor = default_color;
                }
            },
            ip_address_option, email_option, password_option, file_option);

            return root_command.InvokeAsync(args).Result;
        }
        catch (Exception exception)
        {
            var default_color = Console.ForegroundColor;
            Console.ForegroundColor = ConsoleColor.Red;
            System.Console.WriteLine("FAILED:" + exception.Message);
            Console.ForegroundColor = default_color;
            return 1;
        }
    }
}
