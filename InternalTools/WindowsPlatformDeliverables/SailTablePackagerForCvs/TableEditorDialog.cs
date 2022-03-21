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
    public partial class TableEditDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tableProperties"></param>
        public TableEditDialog(
            ref TableProperties tableProperties
            )
        {
            InitializeComponent();

            // Initialize table properties
            m_TableProperties = tableProperties;
            m_TableIdentifierTextBox.Text = tableProperties.Identifier;
            m_TableCsvSourceFileTextBox.Text = tableProperties.SourceFilename;
            m_TableTitleTextBox.Text = tableProperties.GetTableProperty("Title");
            m_TableDescriptionTextBox.Text = tableProperties.GetTableProperty("Description");
            m_TableTagsTextBox.Text = tableProperties.GetTableProperty("Tags");
            // Render the table and columns
            this.RenderTable();
            // Now render the selected column information
            m_SelectedPropertyName = "";
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_TableDataGrid_SelectionChanged(
            object sender,
            EventArgs e
            )
        {
            this.RenderSelectedColumnInformation();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_SelectedColumnDynamicPropertiesListBox_SelectedIndexChanged(
            object sender,
            EventArgs e
            )
        {
            if (1 == m_SelectedColumnDynamicPropertiesListBox.SelectedItems.Count)
            {
                string[] words = m_SelectedColumnDynamicPropertiesListBox.SelectedItems[0].ToString().Split(' ');
                if (0 < words.Length)
                {
                    // Make sure that the global m_SelectedPropertyName is set
                    m_SelectedPropertyName = words[0];
                    // There are a series of column properties which we cannot DELETE. Manipulate the
                    // context menu to reflect that
                    if (true == m_ListOfPropertiesWeCannotDelete.Contains(m_SelectedPropertyName))
                    {
                        m_SelectedColumnPropertiesListBoxContextMenuStrip.Items[1].Enabled = false;
                    }
                    else
                    {
                        m_SelectedColumnPropertiesListBoxContextMenuStrip.Items[1].Enabled = true;
                    }
                    // There are a series of column properties which we cannot EDIT. Manipulate the
                    // context menu to reflect that
                    if (true == m_ListOfPropertiesWeCannotEdit.Contains(m_SelectedPropertyName))
                    {
                        m_SelectedColumnPropertiesListBoxContextMenuStrip.Items[2].Enabled = false;
                    }
                    else
                    {
                        m_SelectedColumnPropertiesListBoxContextMenuStrip.Items[2].Enabled = true;
                    }
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_SelectedColumnDynamicPropertiesListBox_DoubleClick(
            object sender,
            EventArgs e
            )
        {
            // Double clicking means we are trying to edit a value. We can only edit some value
            if (true == m_ListOfPropertiesWeCannotEdit.Contains(m_SelectedPropertyName))
            {
                MessageBox.Show(this, "Selected property is read only and cannot be modified.", "Access Denied", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                // We can only proceed if we know that there is an item selected within m_SelectedColumnDynamicPropertiesListBox
                if ("" != m_SelectedPropertyName)
                {
                    // Now we need to figure out what the index of the column is based on the name of the
                    // currently selected column
                    if (0 < m_TableDataGrid.SelectedColumns.Count)
                    {
                        string currentlySelectedColumnHeaderName = m_TableDataGrid.SelectedColumns[0].HeaderText;
                        for (int index = 0; index < m_TableProperties.ColumnCount; index++)
                        {
                            string columnName = m_TableProperties.GetColumnProperty(index, "Name");
                            if (columnName == currentlySelectedColumnHeaderName)
                            {
                                // Once we have both the NAME of the property AND the index of the column, we can
                                // proceed to edit the property
                                this.EditSelectedColumnProperty(index, m_SelectedPropertyName);
                            }
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_AddPropertyToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {

        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_DeletePropertyToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            // We can only proceed if we know that there is an item selected within m_SelectedColumnDynamicPropertiesListBox
            if ("" != m_SelectedPropertyName)
            {
                // Now we need to figure out what the index of the column is based on the name of the
                // currently selected column
                if (0 < m_TableDataGrid.SelectedColumns.Count)
                {
                    // Now we need to figure out what the index of the column is based on the name of the
                    // currently selected column
                    string currentlySelectedColumnHeaderName = m_TableDataGrid.SelectedColumns[0].HeaderText;
                    for (int index = 0; index < m_TableProperties.ColumnCount; index++)
                    {
                        string columnName = m_TableProperties.GetColumnProperty(index, "Name");
                        if (columnName == currentlySelectedColumnHeaderName)
                        {
                            m_TableProperties.DeleteColumnProperty(index, m_SelectedPropertyName);
                            this.RenderSelectedColumnInformation();
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_EditPropertyToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            // We can only proceed if we know that there is an item selected within m_SelectedColumnDynamicPropertiesListBox
            if ("" != m_SelectedPropertyName)
            {
                // Now we need to figure out what the index of the column is based on the name of the
                // currently selected column
                if (0 < m_TableDataGrid.SelectedColumns.Count)
                {
                    string currentlySelectedColumnHeaderName = m_TableDataGrid.SelectedColumns[0].HeaderText;
                    for (int index = 0; index < m_TableProperties.ColumnCount; index++)
                    {
                        string columnName = m_TableProperties.GetColumnProperty(index, "Name");
                        if (columnName == currentlySelectedColumnHeaderName)
                        {
                            // Once we have both the NAME of the property AND the index of the column, we can
                            // proceed to edit the property
                            this.EditSelectedColumnProperty(index, m_SelectedPropertyName);
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="columnIndex"></param>
        /// <param name="propertyName"></param>
        private void EditSelectedColumnProperty(
            int columnIndex,
            string propertyName
            )
        {
            switch (propertyName)
            {
                case "Name":
                case "Description":
                case "Tags"
                :  {
                        EditColumnStringPropertyDialog editColumnStringPropertyDialog = new EditColumnStringPropertyDialog(propertyName, m_TableProperties.GetColumnProperty(columnIndex, propertyName));
                        if (DialogResult.OK == editColumnStringPropertyDialog.ShowDialog())
                        {
                            m_TableProperties.SetColumnProperty(columnIndex, propertyName, editColumnStringPropertyDialog.PropertyValue);
                        }

                        if ("Name" == propertyName)
                        {
                            // We need to change the column header properly
                            m_TableDataGrid.Columns[columnIndex].HeaderText = editColumnStringPropertyDialog.PropertyValue;
                        }

                        this.RenderSelectedColumnInformation();
                    }
                    break;
                case "PrivacyLevel"
                :
                    break;
                case "RejectRowDataIfInvalidData":
                case "RejectRowDataIfMissingData":
                case "ReplaceCellDataWithEmptyIfInvalidData"
                :  {
                        EditColumnBooleanPropertyDialog editColumnBooleanPropertyDialog = new EditColumnBooleanPropertyDialog(propertyName, m_TableProperties.GetColumnProperty(columnIndex, propertyName));
                        if (DialogResult.OK == editColumnBooleanPropertyDialog.ShowDialog())
                        {
                            m_TableProperties.SetColumnProperty(columnIndex, propertyName, editColumnBooleanPropertyDialog.PropertyValue);
                        }

                        this.RenderSelectedColumnInformation();
                    }
                    break;
                case "Units"
                :   SelectUnitsDialog selectUnitsDialog = new SelectUnitsDialog(columnIndex, propertyName, ref m_TableProperties);
                    if (DialogResult.OK == selectUnitsDialog.ShowDialog())
                    {
                        this.RenderSelectedColumnInformation();
                    }
                    break;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        private void RenderTable()
        {
            CsvConfiguration csvConfigurationSettings = new CsvConfiguration(System.Globalization.CultureInfo.CurrentCulture);

            csvConfigurationSettings.BadDataFound = null;
            // Configure the delimiter for the input file
            csvConfigurationSettings.Delimiter = m_TableProperties.GetTableProperty("ValueSeparatorCharacter");
            csvConfigurationSettings.HasHeaderRecord = m_TableProperties.GetTableProperty("HeadersOnFirstLine");
            csvConfigurationSettings.AllowComments = m_TableProperties.GetTableProperty("AllowComments");
            csvConfigurationSettings.Comment = m_TableProperties.GetTableProperty("CommentCharacter");
            csvConfigurationSettings.Quote = m_TableProperties.GetTableProperty("QuoteCharacter");
            csvConfigurationSettings.Escape = m_TableProperties.GetTableProperty("EscapeCharacter");
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
                int rowIndex = 0;

                foreach (object oColumnName in csvReader.HeaderRecord)
                {
                    DataColumn dataColumn = new DataColumn(oColumnName.ToString(), oColumnName.GetType());
                    dataTableToDisplay.Columns.Add(dataColumn);
                }

                while (csvReader.Read() && (rowIndex < 100))
                {
                    if (m_TableProperties.ColumnCount == csvReader.Parser.Record.Length)
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

                foreach (object oColumnName in csvReader.Parser.Record)
                {
                    DataColumn dataColumn = new DataColumn(columnIndex.ToString(), oColumnName.GetType());
                    dataTableToDisplay.Columns.Add(dataColumn);
                    ++columnIndex;
                }

                do
                {
                    if (m_TableProperties.ColumnCount == csvReader.Parser.Record.Length)
                    {
                        dataTableToDisplay.Rows.Add(csvReader.Parser.Record);
                        rowIndex++;
                    }
                }
                while (csvReader.Read() && (rowIndex < 100));
            }
            // Associate the dataTableToDisplay with the DataGrid to display
            m_TableDataGrid.DataSource = dataTableToDisplay;
            foreach (DataGridViewColumn col in m_TableDataGrid.Columns)
            {
                col.SortMode = DataGridViewColumnSortMode.NotSortable;
            }
            m_TableDataGrid.SelectionMode = DataGridViewSelectionMode.FullColumnSelect;
        }

        /// <summary>
        /// 
        /// </summary>
        private void RenderSelectedColumnInformation()
        {
            if (0 < m_TableDataGrid.SelectedColumns.Count)
            {
                string currentlySelectedColumnHeaderName = m_TableDataGrid.SelectedColumns[0].HeaderText;
                for (int index = 0; index < m_TableProperties.ColumnCount; index++)
                {
                    string columnName = m_TableProperties.GetColumnProperty(index, "Name");
                    if (columnName == currentlySelectedColumnHeaderName)
                    {
                        m_SelectedColumnDynamicPropertiesListBox.Items.Clear();
                        foreach (string columnPropertyName in m_TableProperties.GetColumnProperties(index))
                        {
                            string informationToDisplay = columnPropertyName + " = " + m_TableProperties.GetColumnProperty(index, columnPropertyName);
                            m_SelectedColumnDynamicPropertiesListBox.Items.Add(informationToDisplay);
                        }
                    }
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_BackButton_Click(
            object sender,
            EventArgs e
            )
        {
            m_TableProperties.SetTableProperty("Title", m_TableTitleTextBox.Text);
            m_TableProperties.SetTableProperty("Description", m_TableDescriptionTextBox.Text);
            m_TableProperties.SetTableProperty("Tags", m_TableTagsTextBox.Text);
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
            m_TableProperties.SetTableProperty("Title", m_TableTitleTextBox.Text);
            m_TableProperties.SetTableProperty("Description", m_TableDescriptionTextBox.Text);
            m_TableProperties.SetTableProperty("Tags", m_TableTagsTextBox.Text);
        }

        private TableProperties m_TableProperties;
        private string m_SelectedPropertyName;
        private string[] m_ListOfPropertiesWeCannotDelete = { "Description", "Identifier", "SourceFileHeaderName", "Name", "Units", "Type", "PrivacyLevel", "UnitCategories" };
        private string[] m_ListOfPropertiesWeCannotEdit = { "Identifier", "SourceFileHeaderName", "Type", "UnitCategories" };
    }
}


