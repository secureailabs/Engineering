using System.CommandLine;
using Newtonsoft.Json;

namespace DatasetTool;

class DatasetConfiguration
{
    public class DatasetConfigurationJson
    {
        public Dataset dataset { get; set; } = default!;
        public Dataset dataset_version { get; set; } = default!;
        public string data_federation { get; set; } = default!;
        public string data_format { get; set; } = default!;
        public string[] data_source { get; set; } = default!;
    }

    public DatasetConfigurationJson m_configuration = default!;

    public DatasetConfiguration(FileInfo file)
    {
        // Read the contents of the file as a string
        string json_content = File.ReadAllText(file.FullName);
        if (json_content.Length == 0)
        {
            throw new Exception("The file is empty");
        }

        // Deserialize the JSON string into the configuration object
        m_configuration = JsonConvert.DeserializeObject<DatasetConfigurationJson>(json_content)!;
        if (m_configuration == null)
        {
            throw new Exception("The file is not a valid JSON");
        }
    }
}
