using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailTablePackagerForCsv
{
    public partial class SelectUnitsDialog : Form
    {
        public SelectUnitsDialog(
            int columnIndex,
            string propertyName,
            ref TableProperties tableProperties
            )
        {
            InitializeComponent();

            // Make sure to record incoming parameters
            m_ColumnIndex = columnIndex;
            m_TableProperties = tableProperties;
            // Initialize the various controls
            m_ColumnOriginalNameTextBox.Text = m_TableProperties.GetColumnProperty(m_ColumnIndex, "SourceFileHeaderName");
            m_ColumnDisplayNameTextBox.Text = m_TableProperties.GetColumnProperty(m_ColumnIndex, "Name");
            m_PropertyNameTextBox.Text = propertyName;
            // Now select the proper combo box item
            string currentUnits = m_TableProperties.GetColumnProperty(m_ColumnIndex, "Units");
            // Figure out how to make the proper selection in the combo box
            int index = 0;
            foreach (string unit in m_UnitsComboBox.Items)
            {
                if (currentUnits == unit)
                {
                    m_UnitsComboBox.SelectedIndex = index;
                }
                index++;
            }
            // If this is a categorical value, display the categories
            if ("Categorical" == currentUnits)
            {
                string categories = m_TableProperties.GetColumnProperty(m_ColumnIndex, "UnitCategories");
                m_CategoriesTextBox.Enabled = true;
                m_CategoriesTextBox.BackColor = SystemColors.Info;
                m_CategoriesTextBox.Text = categories;
            }
            else
            {
                m_CategoriesTextBox.Enabled = false;
                m_CategoriesTextBox.BackColor = SystemColors.Control;
                m_CategoriesTextBox.Text = "";
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_OkButton_Click(
            object sender,
            EventArgs e
            )
        {
            m_TableProperties.SetColumnProperty(m_ColumnIndex, "Units", m_UnitsComboBox.SelectedItem.ToString());
            m_TableProperties.SetColumnProperty(m_ColumnIndex, "Type", m_TypeTextBox.Text);
            if ("Categorical" == m_UnitsComboBox.SelectedItem.ToString())
            {
                m_TableProperties.SetColumnProperty(m_ColumnIndex, "UnitCategories", m_CategoriesTextBox.Text);
            }
            else
            {
                m_TableProperties.DeleteColumnProperty(m_ColumnIndex, "UnitCategories");
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_UnitsComboBox_SelectedIndexChanged(
            object sender,
            EventArgs e
            )
        {
            switch (m_UnitsComboBox.SelectedItem.ToString())
            {
                case "Boolean"
                :   m_TypeTextBox.Text = "string";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Celcius"
                :   m_TypeTextBox.Text = "float";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Centimeters"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "DecimalNumber"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Farenheit"
                :   m_TypeTextBox.Text = "float";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Feet"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Categorical"
                :   m_TypeTextBox.Text = "string";
                    m_CategoriesTextBox.Enabled = true;
                    m_CategoriesTextBox.BackColor = SystemColors.Info;
                    break;
                case "GenericString"
                :   m_TypeTextBox.Text = "string";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Inches"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Integer"
                :   m_TypeTextBox.Text = "int";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Meters"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
                case "Millimeters"
                :   m_TypeTextBox.Text = "double";
                    m_CategoriesTextBox.Enabled = false;
                    m_CategoriesTextBox.BackColor = SystemColors.Control;
                    break;
            }
        }

        private int m_ColumnIndex;
        private TableProperties m_TableProperties;
    }
}
