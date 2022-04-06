using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using CsvHelper;
using CsvHelper.Configuration;

namespace SailTablePackagerForCsv
{
    /// <summary>
    /// The goal of the GlobalImportPropertiesDialog is to allow the user to specify initial importation settings
    /// for the CSF file and to view how this impacts the importation of the file in real-time. Users can
    /// change settings and see the impact in real-time
    /// </summary>
    public partial class GlobalImportPropertiesDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tableProperties"></param>
        public GlobalImportPropertiesDialog(
            ref TableProperties tableProperties
            )
        {
            InitializeComponent();
            // Make sure to register the filename
            m_TableProperties = tableProperties;
            // Make sure to validate character input
            m_ValueSeparatorCharacterTextBox.KeyPress += m_ValueSeparatorCharacterTextBox_KeyPress;
            m_LineCommentCharacterTextBox.KeyPress += m_LineCommentCharacterTextBox_KeyPress;
            m_QuoteCharacterTextBox.KeyPress += m_QuoteCharacterTextBox_KeyPress;
            m_EscapeCharacterTextBox.KeyPress += m_EscapeCharacterTextBox_KeyPress;
            // Now we need to initialize the text field with the tableProperties passed in
            if (null != m_TableProperties.GetTableProperty("ValueSeparatorCharacter"))
            {
                m_ValueSeparatorCharacterTextBox.Text = m_TableProperties.GetTableProperty("ValueSeparatorCharacter").ToString();
            }
            if (null != m_TableProperties.GetTableProperty("AllowComments"))
            {
                m_ParseCommentLinesCheckBox.Checked = m_TableProperties.GetTableProperty("AllowComments");
            }
            if (null != m_TableProperties.GetTableProperty("CommentCharacter"))
            {
                m_LineCommentCharacterTextBox.Text = m_TableProperties.GetTableProperty("CommentCharacter").ToString();
            }
            if (null != m_TableProperties.GetTableProperty("HeadersOnFirstLine"))
            {
                m_FirstLineHeadersCheckBox.Checked = m_TableProperties.GetTableProperty("HeadersOnFirstLine");
            }
            if (null != m_TableProperties.GetTableProperty("QuoteCharacter"))
            {
                m_QuoteCharacterTextBox.Text = m_TableProperties.GetTableProperty("QuoteCharacter").ToString();
            }
            if (null != m_TableProperties.GetTableProperty("EscapeCharacter"))
            {
                m_EscapeCharacterTextBox.Text = m_TableProperties.GetTableProperty("EscapeCharacter").ToString();
            }
            if (null != m_TableProperties.GetTableProperty("ColumnCount"))
            {
                m_ColumnCount = m_TableProperties.GetTableProperty("ColumnCount");
            }
            // Starting default
            m_FirstLineHeaderHasChanged = true;
            // Do the initial load and view
            this.UpdateColumnNames();
            this.RefreshDataGridView();
        }

        /// <summary>
        /// This method is used to check and make sure that the user input provided
        /// in one of the input fields is unique to that input field. This is to
        /// prevent the same input value specifier from being used in more than
        /// one specification
        /// </summary>
        /// <param name="inputCharacter"></param>
        /// <param name="stringFieldName"></param>
        /// <returns></returns>
        private bool CheckInputValueUniqueness(
            char inputCharacter,
            string stringFieldName
            )
        {
            bool isUnique = true;

            if ("EscapeCharacter" != stringFieldName)
            { 
                if (inputCharacter == m_EscapeCharacterTextBox.Text[0])
                {
                    isUnique = false;
                }
            }
            if ("LineCommentCharacter" != stringFieldName)
            {
                if (inputCharacter == m_LineCommentCharacterTextBox.Text[0])
                {
                    isUnique = false;
                }
            }
            if ("QuoteCharacter" != stringFieldName)
            {
                if (inputCharacter == m_QuoteCharacterTextBox.Text[0])
                {
                    isUnique = false;
                }
            }
            if ("ValueSeparator" != stringFieldName)
            {
                if (inputCharacter == m_ValueSeparatorCharacterTextBox.Text[0])
                {
                    isUnique = false;
                }
            }

            return isUnique;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ValueSeparatorCharacterTextBox_KeyPress(
            object sender,
            KeyPressEventArgs e
            )
        {
            if ((false == char.IsPunctuation(e.KeyChar))&&('|' != e.KeyChar))
            {
                // Prevent any characters that are not punctuation characters from being entered in the
                // m_ValueSeparatorCharacterTextBox field
                e.Handled = true;
            }
            else
            {
                // We need to make sure that the new value being proposed isn't
                // a value used in another field
                if (true == this.CheckInputValueUniqueness(e.KeyChar, "ValueSeparator"))
                {
                    m_ValueSeparatorCharacterTextBox.Text = e.KeyChar.ToString();
                }
                else
                {
                    MessageBox.Show(this, "Cannot specify a value which exists in another field", "Invalid Value Specified", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                e.Handled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_QuoteCharacterTextBox_KeyPress(
            object sender,
            KeyPressEventArgs e
            )
        {
            if ((false == char.IsPunctuation(e.KeyChar)) && ('|' != e.KeyChar))
            {
                // Prevent any characters that are not punctuation characters from being entered in the
                // m_ValueSeparatorCharacterTextBox field
                e.Handled = true;
            }
            else
            {
                // We need to make sure that the new value being proposed isn't
                // a value used in another field
                if (true == this.CheckInputValueUniqueness(e.KeyChar, "QuoteCharacter"))
                {
                    m_QuoteCharacterTextBox.Text = e.KeyChar.ToString();
                }
                else
                {
                    MessageBox.Show(this, "Cannot specify a value which exists in another field", "Invalid Value Specified", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                e.Handled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_LineCommentCharacterTextBox_KeyPress(
            object sender,
            KeyPressEventArgs e
            )
        {
            if ((false == char.IsPunctuation(e.KeyChar)) && ('|' != e.KeyChar))
            {
                // Prevent any characters that are not punctuation characters from being entered in the
                // m_ValueSeparatorCharacterTextBox field
                e.Handled = true;
            }
            else
            {
                // We need to make sure that the new value being proposed isn't
                // a value used in another field
                if (true == this.CheckInputValueUniqueness(e.KeyChar, ""))
                {
                    m_LineCommentCharacterTextBox.Text = e.KeyChar.ToString();
                }
                else
                {
                    MessageBox.Show(this, "Cannot specify a value which exists in another field", "Invalid Value Specified", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                e.Handled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_EscapeCharacterTextBox_KeyPress(
            object sender,
            KeyPressEventArgs e
            )
        {
            if ((false == char.IsPunctuation(e.KeyChar)) && ('|' != e.KeyChar))
            {
                // Prevent any characters that are not punctuation characters from being entered in the
                // m_ValueSeparatorCharacterTextBox field
                e.Handled = true;
            }
            else
            {
                // We need to make sure that the new value being proposed isn't
                // a value used in another field
                if (true == this.CheckInputValueUniqueness(e.KeyChar, "EscapeCharacter"))
                {
                    m_EscapeCharacterTextBox.Text = e.KeyChar.ToString();
                }
                else
                {
                    MessageBox.Show(this, "Cannot specify a value which exists in another field", "Invalid Value Specified", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                e.Handled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ValueSeparatorCharacterTextBox_TextChanged(
            object sender,
            EventArgs e
            )
        {
            if (2 == m_ValueSeparatorCharacterTextBox.Text.Length)
            {
                m_ValueSeparatorCharacterTextBox.Text = m_ValueSeparatorCharacterTextBox.Text.Substring(1);
            }
            else if (0 == m_ValueSeparatorCharacterTextBox.Text.Length)
            {
                m_ValueSeparatorCharacterTextBox.Text = ",";
            }

            this.UpdateColumnNames();
            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_LineCommentCharacterTextBox_TextChanged(
            object sender,
            EventArgs e
            )
        {
            if (2 == m_LineCommentCharacterTextBox.Text.Length)
            {
                m_LineCommentCharacterTextBox.Text = m_LineCommentCharacterTextBox.Text.Substring(1);
            }

            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_QuoteCharacterTextBox_TextChanged(
            object sender,
            EventArgs e
            )
        {
            if (2 == m_QuoteCharacterTextBox.Text.Length)
            {
                m_QuoteCharacterTextBox.Text = m_QuoteCharacterTextBox.Text.Substring(1);
            }

            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_EscapeCharacterTextBox_TextChanged(
            object sender,
            EventArgs e
            )
        {
            if (2 == m_EscapeCharacterTextBox.Text.Length)
            {
                m_EscapeCharacterTextBox.Text = m_EscapeCharacterTextBox.Text.Substring(1);
            }

            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_FirstLineHeadersCheckBox_CheckedChanged(
            object sender,
            EventArgs e
            )
        {
            m_FirstLineHeaderHasChanged = true;
            this.UpdateColumnNames();
            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ParseCommentLinesCheckBox_CheckedChanged(
            object sender,
            EventArgs e
            )
        {
            if (true == m_ParseCommentLinesCheckBox.Checked)
            {
                m_LineCommentCharacterTextBox.Enabled = true;
            }
            else
            {
                m_LineCommentCharacterTextBox.Enabled = false;
            }

            this.RefreshDataGridView();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_NextButton_Click(
            object sender,
            EventArgs e
            )
        {
            // Record all of the settings selected and then move on
            m_TableProperties.SetTableProperty("ValueSeparatorCharacter", m_ValueSeparatorCharacterTextBox.Text);
            m_TableProperties.SetTableProperty("AllowComments", m_ParseCommentLinesCheckBox.Checked);
            m_TableProperties.SetTableProperty("CommentCharacter", m_LineCommentCharacterTextBox.Text[0]);
            m_TableProperties.SetTableProperty("HeadersOnFirstLine", m_FirstLineHeadersCheckBox.Checked);
            m_TableProperties.SetTableProperty("QuoteCharacter", m_QuoteCharacterTextBox.Text[0]);
            m_TableProperties.SetTableProperty("EscapeCharacter", m_EscapeCharacterTextBox.Text[0]);
            m_TableProperties.SetTableProperty("ColumnCount", m_ColumnCount);
            if (null == m_TableProperties.GetTableProperty("Title")) m_TableProperties.SetTableProperty("Title", "EDIT ME <This is a new table>");
            if (null == m_TableProperties.GetTableProperty("Description")) m_TableProperties.SetTableProperty("Description", "EDIT ME <This is the description of a new table>");
            if (null == m_TableProperties.GetTableProperty("Tags")) m_TableProperties.SetTableProperty("Tags", "EDIT ME <Tags for table>");
            // Now make sure to initialize all of the mandatory columns with default values
            for (int index = 0; index < m_ColumnCount; index++)
            {
                if (null == m_TableProperties.GetColumnProperty(index, "Identifier")) m_TableProperties.SetColumnProperty(index, "Identifier", ApiInterop.GenerateIdentifier(3));
                if (null == m_TableProperties.GetColumnProperty(index, "Units")) m_TableProperties.SetColumnProperty(index, "Units", "GenericString");
                if (null == m_TableProperties.GetColumnProperty(index, "Type")) m_TableProperties.SetColumnProperty(index, "Type", "string");
                if (null == m_TableProperties.GetColumnProperty(index, "Description")) m_TableProperties.SetColumnProperty(index, "Description", "EDIT ME <This is the description of a column containing generic text>");
                if (null == m_TableProperties.GetColumnProperty(index, "Tags")) m_TableProperties.SetColumnProperty(index, "Tags", "EDIT ME <#Column>");
                if (null == m_TableProperties.GetColumnProperty(index, "RejectRowDataIfInvalidData")) m_TableProperties.SetColumnProperty(index, "RejectRowDataIfInvalidData", false);
                if (null == m_TableProperties.GetColumnProperty(index, "RejectRowDataIfMissingData")) m_TableProperties.SetColumnProperty(index, "RejectRowDataIfMissingData", false);
                if (null == m_TableProperties.GetColumnProperty(index, "ReplaceCellDataWithEmptyIfInvalidData")) m_TableProperties.SetColumnProperty(index, "ReplaceCellDataWithEmptyIfInvalidData", true);
            }
        }

        /// <summary>
        /// Method used to update the column name based on whether or not we are using column headers or not
        /// </summary>
        private void UpdateColumnNames()
        {
            CsvConfiguration csvConfigurationSettings = new CsvConfiguration(System.Globalization.CultureInfo.CurrentCulture);

            csvConfigurationSettings.BadDataFound = null;
            // Configure the delimiter for the input file
            csvConfigurationSettings.Delimiter = m_ValueSeparatorCharacterTextBox.Text;
            // Configure whether or not the input file contains column headers or not
            if (true == m_FirstLineHeadersCheckBox.Checked)
            {
                csvConfigurationSettings.HasHeaderRecord = true;
            }
            else
            {
                csvConfigurationSettings.HasHeaderRecord = false;
            }
            // Configure whether or not the input file uses comments
            if (true == m_ParseCommentLinesCheckBox.Checked)
            {
                if (1 == m_LineCommentCharacterTextBox.Text.Length)
                {
                    csvConfigurationSettings.AllowComments = true;
                    csvConfigurationSettings.Comment = m_LineCommentCharacterTextBox.Text[0];
                }
                else
                {
                    csvConfigurationSettings.AllowComments = false;
                }
            }
            else
            {
                csvConfigurationSettings.AllowComments = false;
            }
            // Configure the quote character
            if (1 == m_QuoteCharacterTextBox.Text.Length)
            {
                csvConfigurationSettings.Quote = m_QuoteCharacterTextBox.Text[0];
            }
            if (1 == m_EscapeCharacterTextBox.Text.Length)
            {
                csvConfigurationSettings.Escape = m_EscapeCharacterTextBox.Text[0];
            }
            csvConfigurationSettings.IgnoreBlankLines = true;
            csvConfigurationSettings.TrimOptions = (TrimOptions.Trim | TrimOptions.InsideQuotes);
            // Read in the CSV file and display the first 100 lines. There is two ways to do this,
            // with a header, or without a header. It's important NOT to try and access the
            // header if csvConfigurationSettings.HasHeaderRecord = false
            var streamReader = new System.IO.StreamReader(m_TableProperties.SourceFilename);
            var csvReader = new CsvReader(streamReader, csvConfigurationSettings);
            var dataReader = new CsvDataReader(csvReader);
            // Update the column count
            if (true == m_FirstLineHeaderHasChanged)
            {
                m_TableProperties.DeleteColumnProperties();
                m_FirstLineHeaderHasChanged = false;
            }
            if (true == m_FirstLineHeadersCheckBox.Checked)
            {
                int columnIndex = 0;

                // Figure out the column count
                m_ColumnCount = csvReader.HeaderRecord.Length;

                if (m_ColumnCount != m_TableProperties.ColumnCount)
                {
                    m_TableProperties.ColumnCount = m_ColumnCount;
                }

                foreach (string oColumnName in csvReader.HeaderRecord)
                {
                    m_TableProperties.DeleteColumnProperty(columnIndex, "SourceFileColumnPosition");
                    m_TableProperties.SetColumnProperty(columnIndex, "SourceFileHeaderName", oColumnName);
                    m_TableProperties.SetColumnProperty(columnIndex, "Name", oColumnName);
                    m_TableProperties.DeleteColumnProperty(columnIndex, "DestinationFileColumnName");
                    ++columnIndex;
                }
            }
            else
            {
                // Figure out the column count
                m_ColumnCount = csvReader.Parser.Record.Length;

                if (m_ColumnCount != m_TableProperties.ColumnCount)
                {
                    m_TableProperties.ColumnCount = m_ColumnCount;
                }

                for (int columnIndex = 0; columnIndex < m_ColumnCount; columnIndex++)
                {
                    m_TableProperties.SetColumnProperty(columnIndex, "SourceFileColumnPosition", columnIndex);
                    m_TableProperties.SetColumnProperty(columnIndex, "SourceFileColumnName", columnIndex.ToString());
                    m_TableProperties.SetColumnProperty(columnIndex, "Name", columnIndex.ToString());
                    m_TableProperties.SetColumnProperty(columnIndex, "DestinationFileColumnName", columnIndex.ToString());
                    //++columnIndex;
                }
            }
        }

        /// <summary>
        /// This function effectively reloads everything and displays it all over again using the
        /// new settings
        /// </summary>
        private void RefreshDataGridView()
        {
            CsvConfiguration csvConfigurationSettings = new CsvConfiguration(System.Globalization.CultureInfo.CurrentCulture);

            csvConfigurationSettings.BadDataFound = null;
            // Configure the delimiter for the input file
            csvConfigurationSettings.Delimiter = m_ValueSeparatorCharacterTextBox.Text;
            // Configure whether or not the input file contains column headers or not
            if (true == m_FirstLineHeadersCheckBox.Checked)
            {
                csvConfigurationSettings.HasHeaderRecord = true;
            }
            else
            {
                csvConfigurationSettings.HasHeaderRecord = false;
            }
            // Configure whether or not the input file uses comments
            if (true == m_ParseCommentLinesCheckBox.Checked)
            {
                if (1 == m_LineCommentCharacterTextBox.Text.Length)
                {
                    csvConfigurationSettings.AllowComments = true;
                    csvConfigurationSettings.Comment = m_LineCommentCharacterTextBox.Text[0];
                }
                else
                {
                    csvConfigurationSettings.AllowComments = false;
                }
            }
            else
            {
                csvConfigurationSettings.AllowComments = false;
            }
            // Configure the quote character
            if (1 == m_QuoteCharacterTextBox.Text.Length)
            {
                csvConfigurationSettings.Quote = m_QuoteCharacterTextBox.Text[0];
            }
            if (1 == m_EscapeCharacterTextBox.Text.Length)
            {
                csvConfigurationSettings.Escape = m_EscapeCharacterTextBox.Text[0];
            }
            csvConfigurationSettings.IgnoreBlankLines = true;
            csvConfigurationSettings.TrimOptions = (TrimOptions.Trim | TrimOptions.InsideQuotes);
            // Read in the CSV file and display the first 100 lines. There is two ways to do this,
            // with a header, or without a header. It's important NOT to try and access the
            // header if csvConfigurationSettings.HasHeaderRecord = false
            var streamReader = new System.IO.StreamReader(m_TableProperties.SourceFilename);
            var csvReader = new CsvReader(streamReader, csvConfigurationSettings);
            var dataReader = new CsvDataReader(csvReader);
            var dataTableToDisplay = new DataTable();
            if (true == csvConfigurationSettings.HasHeaderRecord)
            {
                int columnIndex = 0;
                int rowIndex = 0;

                m_ColumnCount = csvReader.HeaderRecord.Length;
                foreach (string oColumnName in csvReader.HeaderRecord)
                {
                    DataColumn dataColumn = new DataColumn(m_TableProperties.GetColumnProperty(columnIndex, "Name"), m_TableProperties.GetColumnProperty(columnIndex, "Name").GetType());
                    dataTableToDisplay.Columns.Add(dataColumn);
                    ++columnIndex;
                }

                while (csvReader.Read() && (rowIndex < 100))
                {
                    if (m_ColumnCount == csvReader.Parser.Record.Length)
                    {
                        dataTableToDisplay.Rows.Add(csvReader.Parser.Record);
                        rowIndex++;
                    }
                }
            }
            else
            {
                int columnIndex = 0;
                int rowIndex = 0;

                m_ColumnCount = csvReader.Parser.Record.Length;
                foreach (object oColumnName in csvReader.Parser.Record)
                {
                    DataColumn dataColumn = new DataColumn(columnIndex.ToString(), oColumnName.GetType());
                    dataTableToDisplay.Columns.Add(dataColumn);
                    ++columnIndex;
                }

                do
                {
                    if (m_ColumnCount == csvReader.Parser.Record.Length)
                    {
                        dataTableToDisplay.Rows.Add(csvReader.Parser.Record);
                        rowIndex++;
                    }
                }
                while (csvReader.Read() && (rowIndex < 100));
            }
            // Associate the dataTableToDisplay with the DataGrid to display
            m_PreviewDataGrid.DataSource = dataTableToDisplay;
        }

        /// <summary>
        /// We need to add this event in order to change the column weight to something
        /// other than 1, otherwise we will not be able to import tables which have
        /// more than 300 colums
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_PreviewDataGrid_ColumnAdded(
            object sender,
            DataGridViewColumnEventArgs e
            )
        {
            e.Column.FillWeight = 1;
        }

        private TableProperties m_TableProperties;
        private int m_ColumnCount;
        private bool m_FirstLineHeaderHasChanged;
    }
}
