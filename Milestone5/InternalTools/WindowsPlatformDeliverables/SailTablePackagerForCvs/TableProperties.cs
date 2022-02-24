using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CsvHelper;
using CsvHelper.Configuration;

namespace SailTablePackagerForCsv
{
    public class TableProperties
    { 
        /// <summary>
        /// 
        /// </summary>
        /// <param name="sourceFilame"></param>
        /// <param name="columnCount"></param>
        public TableProperties()
        {
            m_Identifier = ApiInterop.GenerateIdentifier(2);
            this.Clear();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="templateFilename"></param>
        public TableProperties(
            string templateFilename
            )
        {
            this.Clear();
            this.LoadTemplateFromDisk(templateFilename);
            m_Identifier = ApiInterop.GenerateIdentifier(2);
        }

        /// <summary>
        /// 
        /// </summary>
        public void Clear()
        {
            m_SourceFilename = "";
            m_TablePropertyName = new Dictionary<ulong, string>();
            m_TableProperties = new Dictionary<ulong, dynamic>();
            m_ColumnPropertyNames = new List<Dictionary<ulong, string>>();
            m_ColumnProperties = new List<Dictionary<ulong, dynamic>>();
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
        public string SourceFilename
        {
            get
            {
                return m_SourceFilename;
            }

            set
            {
                m_SourceFilename = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public int ColumnCount
        {
            get
            {
                return m_ColumnProperties.Count;
            }

            set
            {
                m_ColumnPropertyNames = new List<Dictionary<ulong, string>>();
                m_ColumnProperties = new List<Dictionary<ulong, dynamic>>();
                // Initialize the dictionary for each column
                for (int index = 0; index < value; index++)
                {
                    Dictionary<ulong, string> columnPropertyNames = new Dictionary<ulong, string>();
                    Dictionary<ulong, dynamic> columnProperties = new Dictionary<ulong, dynamic>();
                    m_ColumnPropertyNames.Add(columnPropertyNames);
                    m_ColumnProperties.Add(columnProperties);
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="propertyName"></param>
        /// <param name="propertyValue"></param>
        /// <returns></returns>
        public void SetTableProperty(
            string propertyName,
            object propertyValue
            )
        {
            ulong hashOfPropertyName = ApiInterop.Get64BitHashOfString(propertyName, false);
            m_TablePropertyName[hashOfPropertyName] = propertyName;
            m_TableProperties[hashOfPropertyName] = propertyValue;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="propertyName"></param>
        /// <returns></returns>
        public dynamic GetTableProperty(
            string propertyName
            )
        {
            ulong hashOfPropertyName = ApiInterop.Get64BitHashOfString(propertyName, false);
            dynamic returnValue = null;
            if (m_TableProperties.ContainsKey(hashOfPropertyName))
            {
                returnValue = m_TableProperties[hashOfPropertyName];
            }
            return returnValue;
        }

        /// <summary>
        /// 
        /// </summary>
        public string[] GetTableProperties()
        {
            string[] tableProperties = new string[m_TablePropertyName.Count];
            int index = 0;
            foreach (KeyValuePair<ulong,string> valuePair in m_TablePropertyName)
            {
                tableProperties[index] = valuePair.Value;
                index++;
            }
            return tableProperties;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="columnIndex"></param>
        /// <param name="propertyName"></param>
        /// <param name="propertyValue"></param>
        /// <returns></returns>
        public void SetColumnProperty(
            int columnIndex,
            string propertyName,
            object propertyValue)
        {
            ulong hashOfPropertyName = ApiInterop.Get64BitHashOfString(propertyName, false);
            m_ColumnPropertyNames[columnIndex][hashOfPropertyName] = propertyName;
            m_ColumnProperties[columnIndex][hashOfPropertyName] = propertyValue;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="columnIndex"></param>
        /// <param name="propertyName"></param>
        public void DeleteColumnProperty(
            int columnIndex,
            string propertyName
            )
        {
            ulong hashOfPropertyName = ApiInterop.Get64BitHashOfString(propertyName, false);
            if (columnIndex < m_ColumnPropertyNames.Count)
            {
                if (true == m_ColumnPropertyNames[columnIndex].ContainsKey(hashOfPropertyName))
                {
                    m_ColumnPropertyNames[columnIndex].Remove(hashOfPropertyName);
                }
                if (true == m_ColumnProperties[columnIndex].ContainsKey(hashOfPropertyName))
                {
                    m_ColumnProperties[columnIndex].Remove(hashOfPropertyName);
                }
            }
        }

        /// <summary>
        /// Get the names of all the properties associated with a specific column
        /// </summary>
        /// <param name="columnIndex"></param>
        /// <returns></returns>
        public string[] GetColumnProperties(
            int columnIndex
            )
        {
            string[] columnProperties = new string[m_ColumnPropertyNames[columnIndex].Count];
            int index = 0;
            foreach (string colunmPropertyName in m_ColumnPropertyNames[columnIndex].Values)
            {
                columnProperties[index] = colunmPropertyName;
                index++;
            }
            return columnProperties;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="columnIndex"></param>
        /// <param name="propertyName"></param>
        /// <returns></returns>
        public dynamic GetColumnProperty(
            int columnIndex,
            string propertyName
            )
        {
            ulong hashOfPropertyName = ApiInterop.Get64BitHashOfString(propertyName, false);
            dynamic propertyValue = null;
            if (columnIndex < m_ColumnProperties.Count)
            {
                if (true == m_ColumnProperties[columnIndex].ContainsKey(hashOfPropertyName))
                {
                    propertyValue = m_ColumnProperties[columnIndex][hashOfPropertyName];
                }
            }

            return propertyValue;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public void SaveTemplateToDisk(
            string templateFilename
            )
        {
            System.IO.File.Delete(templateFilename);
            // Open up the destination file
            StreamWriter file = new StreamWriter(templateFilename, append: true);
            // Write out the table properties.
            string[] tablePropertyNames = this.GetTableProperties();
            foreach (string propertyName in tablePropertyNames)
            {
                var propertyValue = this.GetTableProperty(propertyName);
                string outputString = null;
                if ("System.String" == propertyValue.GetType().ToString())
                {
                    outputString = "TableProperty," + propertyName + "," + propertyValue.GetType() + ",\"" + propertyValue.ToString() + "\"";
                }
                else if ("System.Char" == propertyValue.GetType().ToString())
                {
                    if ('"' == propertyValue)
                    {
                        outputString = "TableProperty," + propertyName + "," + propertyValue.GetType() + ",\"\\\"\"";
                    }
                    else if ('\\' == propertyValue)
                    {
                        outputString = "TableProperty," + propertyName + "," + propertyValue.GetType() + ",\"\\\\\"";
                    }
                    else
                    {
                        outputString = "TableProperty," + propertyName + "," + propertyValue.GetType() + ",\"" + propertyValue.ToString() + "\"";
                    }
                }
                else
                {
                    outputString = "TableProperty," + propertyName + "," + propertyValue.GetType() + "," + propertyValue.ToString();
                }
                file.WriteLine(outputString);
            }
            // Now go through each column and print out all of the column properties to file
            for (int index = 0; index < m_ColumnPropertyNames.Count; index++)
            {
                string[] columnPropertyNames = this.GetColumnProperties(index);
                foreach (string propertyName in columnPropertyNames)
                {
                    var propertyValue = this.GetColumnProperty(index, propertyName);
                    string outputString = null;
                    if ("System.String" == propertyValue.GetType().ToString())
                    {
                        outputString = "ColumnProperty," + index + "," + propertyName + "," + propertyValue.GetType() + ",\"" + propertyValue.ToString() + "\"";
                    }
                    else if ("System.Char" == propertyValue.GetType().ToString())
                    {
                        if ('"' == propertyValue)
                        {
                            outputString = "ColumnProperty," + index + "," + propertyName + "," + propertyValue.GetType() + ",\"\\\"\"";
                        }
                        else if ('\\' == propertyValue)
                        {
                            outputString = "ColumnProperty," + index + "," + propertyName + "," + propertyValue.GetType() + ",\"\\\\\"";
                        }
                        else
                        {
                            outputString = "ColumnProperty," + index + "," + propertyName + "," + propertyValue.GetType() + ",\"" + propertyValue.ToString() + "\"";
                        }
                    }
                    else
                    {
                        outputString = "ColumnProperty," + index + "," + propertyName + "," + propertyValue.GetType() + "," + propertyValue.ToString();
                    }
                    file.WriteLine(outputString);
                }
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
                if ("TableProperty" == record[0])
                {
                    switch (record[2])
                    {
                        case "System.String"
                        :   this.SetTableProperty(record[1], record[3]);
                            break;
                        case "System.Boolean"
                        :
                            this.SetTableProperty(record[1], bool.Parse(record[3]));
                            break;
                        case "System.Char"
                        :
                            this.SetTableProperty(record[1], char.Parse(record[3]));
                            break;
                        case "System.Int32"
                        :   if ("ColumnCount" == record[1])
                            {
                                this.ColumnCount = Int32.Parse(record[3]);
                            }
                            this.SetTableProperty(record[1], Int32.Parse(record[3]));
                            break;
                        default
                        :
                            break;
                    }
                }
                else if ("ColumnProperty" == record[0])
                {
                    int index = int.Parse(record[1]);
                    switch (record[3])
                    {
                        case "System.String"
                        :   if ("Identifier" == record[2])
                            {
                                this.SetColumnProperty(index, record[2], ApiInterop.GenerateIdentifier(3));
                            }
                            else
                            {
                                this.SetColumnProperty(index, record[2], record[4]);
                            }
                            break;
                        case "System.Boolean"
                        :
                            this.SetColumnProperty(index, record[2], bool.Parse(record[4]));
                            break;
                        case "System.Char"
                        :
                            this.SetColumnProperty(index, record[2], char.Parse(record[4]));
                            break;
                        case "System.Int32"
                        :
                            this.SetColumnProperty(index, record[2], Int32.Parse(record[4]));
                            break;
                        default
                        :
                            break;
                    }
                }
            }
        }

        /// <summary>
        /// Private data members
        /// </summary>
        private string m_Identifier;
        private string m_SourceFilename;
        private Dictionary<ulong, string> m_TablePropertyName;
        private Dictionary<ulong, dynamic> m_TableProperties;
        private List<Dictionary<ulong, string>> m_ColumnPropertyNames;
        private List<Dictionary<ulong, dynamic>> m_ColumnProperties;
    }
}
