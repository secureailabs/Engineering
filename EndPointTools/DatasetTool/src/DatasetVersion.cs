using System.Security.Cryptography;
using Azure.Storage.Files.Shares;
using ICSharpCode.SharpZipLib.Core;
using ICSharpCode.SharpZipLib.Zip;
using Newtonsoft.Json;
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
    public void UploadToAzure(string connection_string, string encryption_key)
    {
        // Create a zip package with the data files
        string data_content_zip_file = "data_content.zip";
        CreateZipFromFiles(data_content_zip_file, m_data_files.ToArray());

        // Encrypt the data content zip file
        byte[] nonce = new byte[12];
        RandomNumberGenerator.Fill(nonce);
        byte[] key = System.Convert.FromBase64String(encryption_key);
        var tag = EncryptFileInPlace(data_content_zip_file, key, nonce);

        // Create a file with name dataset_header.json
        string dataset_header_file = "dataset_header.json";
        DatasetHeader dataset_header = new DatasetHeader();
        dataset_header.aes_tag = tag;
        dataset_header.aes_nonce = System.Convert.ToBase64String(nonce);
        dataset_header.dataset_version = m_metadata;
        File.WriteAllText(dataset_header_file, JsonConvert.SerializeObject(dataset_header));

        // Create a data_model zip file
        // TODO: add correct data models when they are available
        string data_model_zip_file = "data_model.zip";
        CreateZipFromFiles(data_model_zip_file, new string[] { "dataset_header.json" });

        // Create a zip file with the dataset header, data model and data content
        string[] big_zip_files = { dataset_header_file, data_model_zip_file, data_content_zip_file };
        string dataset_file = "dataset_" + dataset_version_id.ToString() + ".zip";
        CreateZipFromFiles(dataset_file, big_zip_files);

        // Upload the zip file to the Azure File Share
        using (FileStream fs = File.Open(dataset_file, FileMode.Open))
        {
            // Upload the files created tar file to Azure file share using the sas token
            ShareFileClient fileClient = new ShareFileClient(new Uri(connection_string));
            fileClient.Create(fs.Length);
            fileClient.Upload(fs);
        }

        // Delete the tar file
        File.Delete(data_content_zip_file);
        File.Delete(data_model_zip_file);
        File.Delete(dataset_header_file);
    }

    /// <summary>
    /// Create a zip file from a list of files
    /// </summary>
    /// <param name="zip_file"> Name of the zip file to be created </param>
    /// <param name="files"> array of files to be zipped </param>
    private void CreateZipFromFiles(string zip_file, string[] files)
    {
        using (FileStream fsOut = File.Create(zip_file))
        using (var zipStream = new ZipOutputStream(fsOut))
        {
            //0-9, 9 being the highest level of compression
            zipStream.SetLevel(3);

            foreach (var filename in files)
            {
                var fi = new FileInfo(filename);

                // Clean the name and fix slash direction
                var entryName = Path.GetFileName(ZipEntry.CleanName(filename));
                var newEntry = new ZipEntry(entryName);
                newEntry.Size = fi.Length;
                zipStream.PutNextEntry(newEntry);

                // Zip the file in buffered chunks
                var buffer = new byte[4096];
                using (FileStream fsInput = File.OpenRead(filename))
                {
                    StreamUtils.Copy(fsInput, zipStream, buffer);
                }
                zipStream.CloseEntry();
            }
        }
    }

    /// <summary>
    /// Encrypt the file in place
    /// </summary>
    /// <param name="file"> The file to encrypt </param>
    /// <param name="key"> The 256 bytes key to encrypt </param>
    /// <param name="nonce"> The 12 byte nonce which is also a initialization vector </param>
    /// <returns> The authentication tag generated after encryption </returns>
    private string EncryptFileInPlace(string file, byte[] key, byte[] nonce)
    {
        // Check the size of the key
        if (key.Length != 32)
        {
            throw new Exception("The key must be 256 bits");
        }

        // Check the size of the nonce
        if (nonce.Length != 12)
        {
            throw new Exception("The nonce must be 96 bits");
        }

        // Read the file into a byte array
        byte[] file_bytes = File.ReadAllBytes(file);

        // Create a new byte array with the same size as the file
        byte[] encrypted_file_bytes = new byte[file_bytes.Length];

        // Allocate a buffer for the tag
        var tag = new byte[AesGcm.TagByteSizes.MaxSize];

        // Create a new instance of the Aes class
        using (AesGcm aes = new AesGcm(key))
        {
            // Encrypt the file
            aes.Encrypt(nonce, file_bytes, encrypted_file_bytes, tag);

            // Write the encrypted file to the same file
            File.WriteAllBytes(file, encrypted_file_bytes);
        }
        return System.Convert.ToBase64String(tag);
    }
}
