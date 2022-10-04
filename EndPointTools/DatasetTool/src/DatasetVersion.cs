using Newtonsoft.Json;
using ICSharpCode.SharpZipLib.Tar;
using Azure.Storage.Files.Shares;

namespace DatasetTool;

class DatasetVersion
{
    private DatasetVersionMetadata m_metadata = new DatasetVersionMetadata();
    private List<string> m_data_files = new List<string>();

    public Guid dataset_version_id { get; set; } = default!;

    /// <summary>
    /// Constructor for the dataset version object
    /// </summary>
    /// <param name="name"> Unique name for the dataset version in the dataset </param>
    /// <param name="description"> Description or summary for the dataset </param>
    /// <param name="tags"> Tags attached to the dataset version for discoverability </param>
    /// <param name="dataset_id"> Dataset Id for which this version is created </param>
    public DatasetVersion(string name, string description, string tags, Guid dataset_id)
    {
        m_metadata.dataset_id = dataset_id;
        m_metadata.description = description;
        m_metadata.name = name;
        m_metadata.tags = tags;
    }

    /// <summary>
    /// Add a file to the dataset version
    /// </summary>
    /// <param name="dataset_file"> The file containing data for this dataset version </param>
    /// <exception cref="Exception"></exception>
    public void AddDatasetFile(string dataset_file)
    {
        if (!File.Exists(dataset_file))
        {
            throw new Exception("The file " + dataset_file + " does not exist. Please check the path");
        }

        // Append only if its a valid file
        m_data_files.Add(dataset_file);
    }

    /// <summary>
    /// Get the metadata for the dataset version to be used for registration
    /// </summary>
    /// <returns> A JSON string </returns>
    public string GetMetadataJson()
    {
        return JsonConvert.SerializeObject(m_metadata);
    }

    /// <summary>
    /// Package the dataset file into a tar file, encrypt it and upload it to the Azure File Share
    /// </summary>
    /// <param name="connection_string"> Connection string with write permission to the file share </param>
    public void UploadToAzure(string connection_string)
    {
        // Create a tar package with the data files
        string tar_file = dataset_version_id.ToString();
        using (FileStream fs = File.Create(tar_file))
        {
            using (TarArchive tarArchive = TarArchive.CreateOutputTarArchive(fs))
            {
                foreach (string file in m_data_files)
                {
                    TarEntry tarEntry = TarEntry.CreateEntryFromFile(file);
                    tarArchive.WriteEntry(tarEntry, true);
                }
            }
        }

        // TODO: Encrypt the tar file

        // Upload the tar file to the Azure File Share
        using (FileStream fs = File.Open(tar_file, FileMode.Open))
        {
            // Upload the files created tar file to Azure file share using the sas token
            ShareFileClient fileClient = new ShareFileClient(new Uri(connection_string));
            fileClient.Create(fs.Length);
            fileClient.Upload(fs);
        }

        // Delete the tar file
        File.Delete(tar_file);
    }
}
