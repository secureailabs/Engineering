using System.Security.Cryptography;
using Azure.Storage.Files.Shares;
using Hl7.Fhir.Model;
using Hl7.Fhir.Serialization;
using Hl7.Fhir.Specification.Source;
using Hl7.Fhir.Validation;
using ICSharpCode.SharpZipLib.Core;
using ICSharpCode.SharpZipLib.Zip;
using Newtonsoft.Json;
namespace DatasetTool;

class DatasetVersion
{
    private ModelDatasetVersionMetadata m_metadata = new ModelDatasetVersionMetadata();
    private List<string> m_data_files = new List<string>();
    public Guid m_dataset_version_id { get; set; } = default!;
    string m_dataset_format = "";

    /// <summary>
    /// Constructor for the dataset version object
    /// </summary>
    /// <param name="name"> Unique name for the dataset version in the dataset </param>
    /// <param name="description"> Description or summary for the dataset </param>
    /// <param name="tags"> Tags attached to the dataset version for discoverability </param>
    /// <param name="dataset_id"> Dataset Id for which this version is created </param>
    public DatasetVersion(string name, string description, string tags, Guid dataset_id, string format)
    {
        m_metadata.dataset_id = dataset_id;
        m_metadata.description = description;
        m_metadata.name = name;
        m_metadata.tags = tags;
        m_dataset_format = format;
    }

    /// <summary>
    /// Add all files form a directory to the dataset version
    /// </summary>
    /// <param name="dataset_directory"> The directory containing data for this dataset version </param>
    /// <exception cref="Exception"></exception>
    private void AddDatasetDirectory(string dataset_directory)
    {
        if (!Directory.Exists(dataset_directory))
        {
            throw new Exception("The directory does not exist");
        }

        m_data_files.AddRange(Directory.GetFiles(dataset_directory));
    }

    /// <summary>
    /// Add a file to the dataset version
    /// </summary>
    /// <param name="dataset_file"> The file containing data for this dataset version </param>
    /// <exception cref="Exception"></exception>
    private void AddDatasetFile(string dataset_file)
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
    public void ValidateAndUploadToAzure(string connection_string, string encryption_key, ModelDatasetHeader dataset_header)
    {
        // Validate the dataset
        Validate();

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
        dataset_header.aes_tag = tag;
        dataset_header.aes_nonce = System.Convert.ToBase64String(nonce);
        File.WriteAllText(dataset_header_file, JsonConvert.SerializeObject(dataset_header));

        // Create a data_model zip file
        // TODO: add correct data models when they are available
        string data_model_zip_file = "data_model.zip";
        CreateZipFromFiles(data_model_zip_file, new string[] { "dataset_header.json" });

        // Create a zip file with the dataset header, data model and data content
        string[] big_zip_files = { dataset_header_file, data_model_zip_file, data_content_zip_file };
        string dataset_file = "dataset_" + m_dataset_version_id.ToString() + ".zip";
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
        File.Delete(dataset_file);
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

    /// <summary>
    /// Add the source for the dataset
    /// </summary>
    /// <param name="dataset_source"> dataset source file or directory </param>
    /// <exception cref="Exception"></exception>
    public void AddDatasetSource(string dataset_source)
    {
        if (Directory.Exists(dataset_source))
        {
            AddDatasetDirectory(dataset_source);
        }
        else if (File.Exists(dataset_source))
        {
            AddDatasetFile(dataset_source);
        }
        else
        {
            throw new Exception("The dataset source file or directory does not exist");
        }
    }

    /// <summary>
    /// Validate the dataset for the correct format
    /// </summary>
    private void Validate()
    {
        if (m_dataset_format == "FHIR")
        {
            // Validate the FHIR dataset
            ValidateFHIR();
        }
        else
        {
            // TODO: Add a CSV validation
        }
    }

    /// <summary>
    /// Validate all FHIR dataset files
    /// </summary>
    private void ValidateFHIR()
    {
        // Create a resource resolver that searches for the core resources in 'specification.zip', which comes with the .NET FHIR Specification NuGet package
        // We create a source that takes its contents from a ZIP file (in this case the default 'specification.zip'). We decorate that source by encapsulating
        // it in a CachedResolver, which speeds up access by caching conformance resources once we got them from the large files in the ZIP.
        IResourceResolver core_source = new CachedResolver(ZipSource.CreateValidationSource());

        // Set up additional resolvers
        var resolver_us_core = new CachedResolver(new FhirPackageSource(
            "https://packages.simplifier.net",
            new[] { "hl7.fhir.us.core@5.0.1" }
        ));

        var resolver_nlm = new CachedResolver(new FhirPackageSource(
            "https://packages.simplifier.net",
            new[] { "us.nlm.vsac@0.9.0" }
        ));

        // This hidden folder will be created by pulling the FHIR profiles from the portal
        string profile_path = "./.FHIR_profiles_json";
        DirectorySourceSettings directory_source_settings = new DirectorySourceSettings();
        directory_source_settings.IncludeSubDirectories = true;
        var directory_source = new CachedResolver(new DirectorySource(profile_path, directory_source_settings));

        var resource_resolvers = new MultiResolver(directory_source, core_source, resolver_nlm, resolver_us_core);

        // setting up the validator
        ValidationSettings settings = new() { ResourceResolver = resource_resolvers };
        Validator validator = new(settings);

        // Get number of files in the dataset
        int num_files = m_data_files.Count;
        int i = 1;
        // Read the contents of the files and validate them
        foreach (string file in m_data_files)
        {
            var default_color = Console.ForegroundColor;
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write(i++ + "/" + num_files);
            Console.ForegroundColor = default_color;
            Console.Write(" Validating file: " + file);
            string file_contents = File.ReadAllText(file);
            FhirJsonParser parser = new FhirJsonParser();
            Bundle resource = parser.Parse<Bundle>(file_contents);

            // validate each resource in the bundle
            bool isValid = true;
            foreach (var entry in resource.Entry)
            {
                var outcome = validator.Validate(entry.Resource);
                if (!outcome.Success)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    if (isValid)
                    {
                        // Put a cross mark ❌
                        Console.WriteLine(" " + ((char)0x274C).ToString());
                    }
                    isValid = isValid & false;
                    Console.WriteLine("Validation failed for resource: " + entry.Resource.TypeName + " with id: " + entry.Resource.Id);
                    Console.WriteLine(entry + "\n" + outcome.ToString());
                    Console.WriteLine("TODO: Enable the validation. Continuing with the upload as a temporary resort.");
                    Console.ForegroundColor = default_color;
                    // throw new Exception("The FHIR bundle is not valid");
                }
            }
            if (isValid)
            {
                // Put a check mark ✅
                Console.WriteLine(" " + ((char)0x2705).ToString());
            }
        }
    }
}
