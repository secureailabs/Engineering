using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using CsvHelper;
using CsvHelper.Configuration;

namespace SailTablePackagerForCsv
{
    public class TablePackager
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tableProperties"></param>
        public TablePackager(
            ref TableProperties tableProperties,
            ref NotificationsAndProgressTracker notificationsAndProgressTracker
            )
        {
            m_TableProperties = tableProperties;
            m_CsvReader = null;
            m_NotificationsAndProgressTracker = notificationsAndProgressTracker;
        }

        /// <summary>
        /// 
        /// </summary>
        private void SetupCsvSourceFile()
        {
            // Prepare to initialize the CSV configation settings to match the selected input settings
            // within the m_TableProperties object
            CsvConfiguration csvInputConfigurationSettings = new CsvConfiguration(System.Globalization.CultureInfo.CurrentCulture);
            // Configure the settings for the input file
            csvInputConfigurationSettings.BadDataFound = null;
            csvInputConfigurationSettings.Delimiter = m_TableProperties.GetTableProperty("ValueSeparatorCharacter");
            csvInputConfigurationSettings.HasHeaderRecord = m_TableProperties.GetTableProperty("HeadersOnFirstLine");
            csvInputConfigurationSettings.AllowComments = m_TableProperties.GetTableProperty("AllowComments");
            csvInputConfigurationSettings.Comment = m_TableProperties.GetTableProperty("CommentCharacter");
            csvInputConfigurationSettings.Quote = m_TableProperties.GetTableProperty("QuoteCharacter");
            csvInputConfigurationSettings.Escape = m_TableProperties.GetTableProperty("EscapeCharacter");
            csvInputConfigurationSettings.IgnoreBlankLines = true;
            csvInputConfigurationSettings.TrimOptions = (TrimOptions.Trim | TrimOptions.InsideQuotes);
            // Prepare the CSV file reader which is responsible for reading the source CSV file
            var streamReader = new System.IO.StreamReader(m_TableProperties.SourceFilename);
            m_CsvReader = new CsvReader(streamReader, csvInputConfigurationSettings);
        }

        /// <summary>
        /// 
        /// </summary>
        private void SetupColumns()
        {
            // How columns are processed depends on whether or not the source file has a set of column headers on the
            // first line or not. Without headers, column processing is strictly positional, which means that the
            // source file must have records which perfectly match the m_TableProperties column count. When using
            // headers, a source file is allowed to have more columns than the number of columns specified within
            // the m_TableProperties
            if (true == m_TableProperties.GetTableProperty("HeadersOnFirstLine"))
            {
                // We are using column headers within the source file
                for (int columnIndex = 0; columnIndex < m_TableProperties.ColumnCount; columnIndex++)
                {
                    string columnIndexAsString = columnIndex.ToString();
                    string columnIdentifier = m_TableProperties.GetColumnProperty(columnIndex, "Identifier");
                    string columnName = m_TableProperties.GetColumnProperty(columnIndex, "Name");
                    string columnDescription = m_TableProperties.GetColumnProperty(columnIndex, "Description");
                    string columnTags = m_TableProperties.GetColumnProperty(columnIndex, "Tags");
                    string columnUnits = m_TableProperties.GetColumnProperty(columnIndex, "Units");
                    string columnType = m_TableProperties.GetColumnProperty(columnIndex, "Type");                    
                    string columnUnitCategories = ("Categorical" == columnUnits) ? m_TableProperties.GetColumnProperty(columnIndex, "UnitCategories") : "";

                    ApiInterop.AddColumnToTablePackageFile(columnIdentifier, columnName, columnDescription, columnTags, columnUnits, columnType, columnUnitCategories);
                }
            }
            else
            {
                // Column processing is strictly positional
            }
        }

        /// <summary>
        /// 
        /// </summary>
        private void SetupDestinationFile()
        {
            // We need the size of the source filename in order to pre-estimate what to allocate in
            // memory within the tablepackage file
            System.IO.FileInfo sourceFileInformation = new System.IO.FileInfo(m_TableProperties.SourceFilename);
            // Start the table package to be built
            ApiInterop.OpenTablePackageFileForWriting(m_TableProperties.GetTableProperty("DestinationIntermediateFile"), sourceFileInformation.Length);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public void PackageTable(
            bool runSilent
            )
        {
            try
            {
                this.SetupCsvSourceFile();
                this.SetupColumns();
                this.SetupDestinationFile();

                // Now go through all of the records one by one and add them to the table package
                while (m_CsvReader.Read())
                {
                    // If the source record has LESS data elements than required, the record is automatically rejected
                    if (m_TableProperties.ColumnCount == m_CsvReader.Parser.Record.Length)
                    {
                        // Get one record. This will yield an array of strings which have been extracted
                        // using the value delimiter of record. But this might not be the SAIL standard
                        // value delimiter, so the next step that is required.
                        string[] currentRecord = m_CsvReader.Parser.Record;
                        // The next step is to validate the base type of each records
                        // Since we have all of the separate elements of a single record, let's join
                        // the elements back together, but this time we use the standard SAIL value
                        // delimiter (1x1f)
                        string properlyDelimitedRecord = string.Join("\x1f", currentRecord);
                        // Now that we have a properly value delimited record, let's give that to our
                        // C++ engine which will take care of sanitizing the rest of the data
                        ApiInterop.AddRecordToTablePackageFile(properlyDelimitedRecord);
                        m_NotificationsAndProgressTracker.Progress++;
                    }
                    else
                    {
                        m_NotificationsAndProgressTracker.AddNotification("Bad record rejected at line # " + m_NotificationsAndProgressTracker.Progress);
                    }
                }
                // Now we commit the CsvFile to disk. We need to do a fixup on the title first
                ApiInterop.CompleteTablePackageFile(m_TableProperties.Identifier, m_TableProperties.GetTableProperty("Title"), m_TableProperties.GetTableProperty("Description"), m_TableProperties.GetTableProperty("Tags"), m_TableProperties.ColumnCount, (int) m_NotificationsAndProgressTracker.Progress);
                if (false == runSilent)
                {
                    m_NotificationsAndProgressTracker.AddNotification("Done!!!");
                }
                m_NotificationsAndProgressTracker.Done = true;
            }

            catch
            {

            }
        }

        /// <summary>
        /// Private data members
        /// </summary>
        private TableProperties m_TableProperties;
        private NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
        private CsvReader m_CsvReader;
    }
}
