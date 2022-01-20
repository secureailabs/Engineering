using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CsvHelper;
using CsvHelper.Configuration;

namespace SailDatasetPackager
{
    public class DatasetProperties
    {
        /// <summary>
        /// 
        /// </summary>
        public DatasetProperties()
        {
            this.Clear();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="templateFilaname"></param>
        public DatasetProperties(
            string templateFilename
            )
        {
            this.Clear();
            this.LoadTemplateFromDisk(templateFilename);
            m_Identifier = ApiInterop.GenerateIdentifier(1);
        }

        /// <summary>
        /// 
        /// </summary>
        public void Clear()
        {
            m_ListOfLoadedTablePackageIndexes = new List<uint>();
            m_Identifier = ApiInterop.GenerateIdentifier(1);
            m_Title = null;
            m_Description = null;
            m_Tags = null;
            m_DatasetFamily = null;
            m_DatasetFamilyDescription = null;
        }

        /// <summary>
        /// 
        /// </summary>
        public string Identifier
        {
            get
            {
                return m_Identifier;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string Title
        {
            get
            {
                return m_Title;
            }
            set
            {
                m_Title = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string Description
        {
            get
            {
                return m_Description;
            }
            set
            {
                m_Description = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string Tags
        {
            get
            {
                return m_Tags;
            }
            set
            {
                m_Tags = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string DatasetFamilyDescription
        {
            get
            {
                return m_DatasetFamilyDescription;
            }
            set
            {
                m_DatasetFamilyDescription = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string DatasetFamily
        {
            get
            {
                return m_DatasetFamily;
            }
            set
            {
                m_DatasetFamily = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageFilename"></param>
        /// <returns></returns>
        public uint AddTablePackageToDataset(
            string tablePackageFilename
            )
        {
            uint tablePackageIndex = ApiInterop.AddTablePackageFromFile(tablePackageFilename);
            if (0xFFFFFFFF != tablePackageIndex)
            {
                m_ListOfLoadedTablePackageIndexes.Add(tablePackageIndex);
            }
            return tablePackageIndex;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageIndex"></param>
        public void RemoveTablePackageFromDataset(
            uint tablePackageIndex
            )
        {
            ApiInterop.RemoveTablePackageByIndex(tablePackageIndex);
            m_ListOfLoadedTablePackageIndexes.Remove(tablePackageIndex);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public uint[] GetListOfTablePackageIndexes()
        {
            return m_ListOfLoadedTablePackageIndexes.ToArray();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageIndex"></param>
        public string GetTablePackageIdentifierByIndex(
            uint tablePackageIndex
            )
        {
            string tablePackageIdentifier = "";

            if (true == m_ListOfLoadedTablePackageIndexes.Contains(tablePackageIndex))
            {
                tablePackageIdentifier = ApiInterop.GetTablePackageIdentifierByIndex(tablePackageIndex);
            }

            return tablePackageIdentifier;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageIndex"></param>
        /// <returns></returns>
        public string GetTablePackageTitleByIndex(
            uint tablePackageIndex
            )
        {
            string tablePackageTitle = "";

            if (true == m_ListOfLoadedTablePackageIndexes.Contains(tablePackageIndex))
            {
                tablePackageTitle = ApiInterop.GetTablePackageTitleByIndex(tablePackageIndex);
            }

            return tablePackageTitle;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageIndex"></param>
        /// <returns></returns>
        public string GetTablePackageDescriptionByIndex(
            uint tablePackageIndex
            )
        {
            string tablePackageDescription = "";

            if (true == m_ListOfLoadedTablePackageIndexes.Contains(tablePackageIndex))
            {
                tablePackageDescription = ApiInterop.GetTablePackageDescriptionByIndex(tablePackageIndex);
            }

            return tablePackageDescription;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="tablePackageIndex"></param>
        /// <returns></returns>
        public string GetTablePackageFilenameByIndex(
            uint tablePackageIndex
            )
        {
            string tablePackageFilename= "";

            if (true == m_ListOfLoadedTablePackageIndexes.Contains(tablePackageIndex))
            {
                tablePackageFilename = ApiInterop.GetTablePackageFilenameByIndex(tablePackageIndex);
            }

            return tablePackageFilename;
        }
        
        /// <summary>
        /// 
        /// </summary>
        /// <param name="datasetFilaname"></param>
        /// <returns></returns>
        public bool PackageDatasetToDisk(
            string datasetFilaname
            )
        {
            bool success = false;

            return success;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="templateFilename"></param>
        public void SaveTemplateToDisk(
           string templateFilename
           )
        {
            // First make sure to delete any existing gile
            System.IO.File.Delete(templateFilename);
            // Now create a new destination file
            StreamWriter file = new StreamWriter(templateFilename, append: true);
            // Write out the dataset properties.
            file.WriteLine("DatasetProperty,Title,\"" + m_Title + "\"");
            file.WriteLine("DatasetProperty,Description,\"" + m_Description + "\"");
            file.WriteLine("DatasetProperty,Tags,\"" + m_Tags + "\"");
            file.WriteLine("DatasetProperty,DatasetFamily,\"" + m_DatasetFamily + "\"");
            file.WriteLine("DatasetProperty,DatasetFamilyDescription,\"" + DatasetFamilyDescription + "\"");
            // Write out the table package properties
            foreach (uint tablePackageIndex in m_ListOfLoadedTablePackageIndexes)
            {
                file.WriteLine("TablePackage,\"" + Path.GetFileName(ApiInterop.GetTablePackageFilenameByIndex(tablePackageIndex)) + "\"");
            }
            file.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="templateFilename"></param>
        private void LoadTemplateFromDisk(
            string templateFilename
            )
        {
            // Prepare to initialize the CSV configation settings to match the selected input settings
            // within the m_TableProperties object
            CsvConfiguration csvInputConfigurationSettings = new CsvConfiguration(System.Globalization.CultureInfo.CurrentCulture);
            // Configure the settings for the input file
            csvInputConfigurationSettings.BadDataFound = null;
            csvInputConfigurationSettings.Delimiter = ",";
            csvInputConfigurationSettings.HasHeaderRecord = false;
            csvInputConfigurationSettings.AllowComments = false;
            csvInputConfigurationSettings.Quote = '"';
            csvInputConfigurationSettings.Escape = '\\';
            csvInputConfigurationSettings.IgnoreBlankLines = true;
            csvInputConfigurationSettings.TrimOptions = (TrimOptions.Trim | TrimOptions.InsideQuotes);
            // Prepare the CSV file reader which is responsible for reading the source CSV file
            var streamReader = new System.IO.StreamReader(templateFilename);
            var csvReader = new CsvReader(streamReader, csvInputConfigurationSettings);
            while (csvReader.Read())
            {
                string[] record = csvReader.Parser.Record;
                if ("DatasetProperty" == record[0])
                {
                    switch (record[1])
                    {
                        case "Title"
                        :   m_Title = record[2];
                            break;
                        case "Description"
                        :   m_Description = record[2];
                            break;
                        case "Tags"
                        :   m_Tags = record[2];
                            break;
                        case "DatasetFamily"
                        :   m_DatasetFamily = record[2];
                            break;
                        case "DatasetFamilyDescription"
                        :   DatasetFamilyDescription = record[2];
                            break;
                        default
                        :
                            break;
                    }
                }
                else if ("TablePackage" == record[0])
                {
                    this.AddTablePackageToDataset(record[1]);
                }
            }
            streamReader.Close();
        }

        private string m_Identifier;
        private string m_Title;
        private string m_Description;
        private string m_Tags;
        private string m_DatasetFamily;
        private string m_DatasetFamilyDescription;
        private List<uint> m_ListOfLoadedTablePackageIndexes;
    }
}
