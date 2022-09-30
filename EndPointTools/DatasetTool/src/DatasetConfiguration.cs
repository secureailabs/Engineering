using System.CommandLine;
using Newtonsoft.Json;

namespace DatasetTool;

class DatasetConfiguration
{
    public class DatasetConfigurationJson
    {
        public Dataset dataset { get; set; } = default!;
        public string description { get; set; } = default!;
        public string data_federation { get; set; } = default!;
        public string data_format { get; set; } = default!;
        public string[] data_source { get; set; } = default!;
    }

    public DatasetConfigurationJson configuration = default!;

    public DatasetConfiguration(FileInfo file)
    {
        // Read the contents of the file as a string
        string json_content = File.ReadAllText(file.FullName);
        if (json_content.Length == 0)
        {
            throw new Exception("The file is empty");
        }
        System.Console.WriteLine(json_content);

        configuration = JsonConvert.DeserializeObject<DatasetConfigurationJson>(json_content)!;
        if (configuration == null)
        {
            throw new Exception("The file is not a valid JSON");
        }
        System.Console.WriteLine(configuration.dataset.name);
    }
}
