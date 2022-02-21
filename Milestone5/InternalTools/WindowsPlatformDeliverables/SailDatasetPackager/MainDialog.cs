using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailDatasetPackager
{
    public partial class MainDialog : Form
    {
        public MainDialog(
            ref DatasetProperties datasetProperties,
            ref NotificationsAndProgressTracker notificationsAndProgressTracker
            )
        {
            InitializeComponent();

            m_DatasetProperties = datasetProperties;
            m_NotificationAndProgressTracker = notificationsAndProgressTracker;
            m_SailWebApiPortalLoginDialog = new SailWebApiPortalLoginDialog();
            m_TableIndexAssociation = new Dictionary<ulong, uint>();
            m_DatasetIdentifierTextBox.Text = m_DatasetProperties.Identifier;
            m_DatasetTitleTextBox.Text = m_DatasetProperties.Title;
            m_DatasetDescriptionTextBox.Text = m_DatasetProperties.Description;
            m_DatasetTagsTextBox.Text = m_DatasetProperties.Tags;
            m_DeleteTableToolStripMenuItem.Enabled = false;
            uint[] listOfTablePackageIndexes = m_DatasetProperties.GetListOfTablePackageIndexes();
            foreach (uint tablePackageIndex in listOfTablePackageIndexes)
            {
                string tablePackageIdentifier = m_DatasetProperties.GetTablePackageIdentifierByIndex(tablePackageIndex);
                string tablePackageTitle = m_DatasetProperties.GetTablePackageTitleByIndex(tablePackageIndex);
                string listBoxDisplayString = tablePackageTitle + ",{" + tablePackageIdentifier + "}";
                ulong listBoxDisplayStringHash = ApiInterop.Get64BitHashOfString(listBoxDisplayString, false);
                m_TableIndexAssociation.Add(listBoxDisplayStringHash, tablePackageIndex);
                m_TablesListBox.Items.Add(listBoxDisplayString);
            }

            if (false == ApiInterop.IsLoggedOn())
            {
                SailWebApiPortalLoginDialog sailWebApiPortalLoginDialog = new SailWebApiPortalLoginDialog();
                sailWebApiPortalLoginDialog.ShowDialog();
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public void Clear()
        {
            m_TableIndexAssociation = new Dictionary<ulong, uint>();
            m_DatasetProperties.Clear();
            m_TableIndexAssociation = new Dictionary<ulong, uint>();
            m_DatasetIdentifierTextBox.Text = m_DatasetProperties.Identifier;
            m_DatasetTitleTextBox.Text = m_DatasetProperties.Title;
            m_DatasetDescriptionTextBox.Text = m_DatasetProperties.Description;
            m_DatasetTagsTextBox.Text = m_DatasetProperties.Tags;
            m_DeleteTableToolStripMenuItem.Enabled = false;
            m_TablesListBox.Items.Clear();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_RefreshDatasetFamiliesLinkLabel_LinkClicked(
            object sender,
            LinkLabelLinkClickedEventArgs e
            )
        {
            if (false == ApiInterop.IsLoggedOn())
            {
                SailWebApiPortalLoginDialog sailWebApiPortalLoginDialog = new SailWebApiPortalLoginDialog();
                sailWebApiPortalLoginDialog.ShowDialog();
            }

            if (true == ApiInterop.IsLoggedOn())
            {
                ApiInterop.UpdateDatasetFamilyInformation();
                string commaDelimitedListOfDatasetFamilyIdentifiers = ApiInterop.GetListOfDatasetFamilyIdentifiers();
                string[] datasetFamilyIdentifiers = commaDelimitedListOfDatasetFamilyIdentifiers.Split(new string[] { "," }, StringSplitOptions.None);
                m_DatasetFamilyComboBox.Items.Clear();
                foreach (string datasetFamilyIdentifier in datasetFamilyIdentifiers)
                {
                    string datasetFamilyTitle = ApiInterop.GetDatasetFamilyTitle(datasetFamilyIdentifier);
                    m_DatasetFamilyComboBox.Items.Add(datasetFamilyTitle + "," + datasetFamilyIdentifier);
                }
                m_DatasetFamilyComboBox.SelectedIndex = 0;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_AddExistingItemToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            m_OpenFileDialog.Filter = "Packaged Table|*.sailtable";
            if (DialogResult.OK == m_OpenFileDialog.ShowDialog())
            {
                uint tablePackageIndex = m_DatasetProperties.AddTablePackageToDataset(m_OpenFileDialog.FileName);
                string tablePackageIdentifier = m_DatasetProperties.GetTablePackageIdentifierByIndex(tablePackageIndex);
                string tablePackageTitle = m_DatasetProperties.GetTablePackageTitleByIndex(tablePackageIndex);
                string listBoxDisplayString = tablePackageTitle + ",{" + tablePackageIdentifier + "}";
                ulong listBoxDisplayStringHash = ApiInterop.Get64BitHashOfString(listBoxDisplayString, false);
                m_TableIndexAssociation.Add(listBoxDisplayStringHash, tablePackageIndex);
                m_TablesListBox.Items.Add(listBoxDisplayString);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_DeleteTableToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            if (-1 != m_TablesListBox.SelectedIndex)
            {
                ulong listBoxDisplayStringHash = ApiInterop.Get64BitHashOfString(m_TablesListBox.Items[m_TablesListBox.SelectedIndex].ToString(), false);
                uint tablePackageIndex = m_TableIndexAssociation[listBoxDisplayStringHash];
                m_DatasetProperties.RemoveTablePackageFromDataset(tablePackageIndex);
                m_TablesListBox.Items.RemoveAt(m_TablesListBox.SelectedIndex);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_TablesListBox_SelectedIndexChanged(
            object sender,
            EventArgs e
            )
        {
            if (-1 != m_TablesListBox.SelectedIndex)
            {
                m_DeleteTableToolStripMenuItem.Enabled = true;
            }
            else
            {
                m_DeleteTableToolStripMenuItem.Enabled = false;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_NewToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            if (DialogResult.Yes == MessageBox.Show("Lose your current work and start a new dataset?", "SAIL Data Publishing Tool", MessageBoxButtons.YesNo, MessageBoxIcon.Exclamation))
            {
                this.Clear();
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_OpenToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            m_OpenFileDialog.Filter = "Dataset Template|*.saildataset";
            if (DialogResult.OK == m_OpenFileDialog.ShowDialog())
            {
                m_DatasetProperties = new DatasetProperties(m_OpenFileDialog.FileName);
                m_TableIndexAssociation = new Dictionary<ulong, uint>();
                m_DatasetIdentifierTextBox.Text = m_DatasetProperties.Identifier;
                m_DatasetTitleTextBox.Text = m_DatasetProperties.Title;
                m_DatasetDescriptionTextBox.Text = m_DatasetProperties.Description;
                m_DatasetTagsTextBox.Text = m_DatasetProperties.Tags;
                m_DatasetFamilyComboBox.Items.Clear();
                m_DatasetFamilyComboBox.Items.Add("None");
                m_DatasetFamilyComboBox.SelectedIndex = m_DatasetFamilyComboBox.Items.Add(m_DatasetProperties.DatasetFamilyDescription);
                m_DeleteTableToolStripMenuItem.Enabled = false;
                uint[] listOfTablePackageIndexes = m_DatasetProperties.GetListOfTablePackageIndexes();
                foreach (uint tablePackageIndex in listOfTablePackageIndexes)
                {
                    string tablePackageIdentifier = m_DatasetProperties.GetTablePackageIdentifierByIndex(tablePackageIndex);
                    string tablePackageTitle = m_DatasetProperties.GetTablePackageTitleByIndex(tablePackageIndex);
                    string listBoxDisplayString = tablePackageTitle + ",{" + tablePackageIdentifier + "}";
                    ulong listBoxDisplayStringHash = ApiInterop.Get64BitHashOfString(listBoxDisplayString, false);
                    m_TableIndexAssociation.Add(listBoxDisplayStringHash, tablePackageIndex);
                    m_TablesListBox.Items.Add(listBoxDisplayString);
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_SaveToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            m_SaveFileDialog.Filter = "Dataset Template|*.saildataset";
            if (DialogResult.OK == m_SaveFileDialog.ShowDialog())
            {
                m_DatasetProperties.Title = m_DatasetTitleTextBox.Text;
                m_DatasetProperties.Description = m_DatasetDescriptionTextBox.Text;
                m_DatasetProperties.Tags = m_DatasetTagsTextBox.Text;
                if (("" != m_DatasetFamilyComboBox.Text) && ("None" != m_DatasetFamilyComboBox.Text))
                {
                    string[] comboBoxParsedValues = m_DatasetFamilyComboBox.Text.Split(',');
                    string datasetFamilyIdentifier = comboBoxParsedValues[1].Replace('{', ' ');
                    datasetFamilyIdentifier = datasetFamilyIdentifier.Replace('}', ' ');
                    datasetFamilyIdentifier = datasetFamilyIdentifier.Trim();
                    datasetFamilyIdentifier = datasetFamilyIdentifier.ToLower();
                    m_DatasetProperties.DatasetFamily = datasetFamilyIdentifier;
                    m_DatasetProperties.DatasetFamilyDescription = m_DatasetFamilyComboBox.Text;
                }
                m_DatasetProperties.SaveTemplateToDisk(m_SaveFileDialog.FileName);
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_CloseToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            if (DialogResult.Yes == MessageBox.Show("Lose your current work and close this dataset?", "SAIL Data Publishing Tool", MessageBoxButtons.YesNo, MessageBoxIcon.Exclamation))
            {
                this.Clear();
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ExitToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            this.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_PublishNowToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            if (false == ApiInterop.IsLoggedOn())
            {
                SailWebApiPortalLoginDialog sailWebApiPortalLoginDialog = new SailWebApiPortalLoginDialog();
                sailWebApiPortalLoginDialog.ShowDialog();
            }

            if (true == ApiInterop.IsLoggedOn())
            {
                m_SaveFileDialog.Filter = "Dataset File|*.csvp";
                if (DialogResult.OK == m_SaveFileDialog.ShowDialog())
                {
                    m_DatasetProperties.Title = m_DatasetTitleTextBox.Text;
                    m_DatasetProperties.Description = m_DatasetDescriptionTextBox.Text;
                    m_DatasetProperties.Tags = m_DatasetTagsTextBox.Text;
                    if (("" != m_DatasetFamilyComboBox.Text) && ("None" != m_DatasetFamilyComboBox.Text))
                    {
                        string[] comboBoxParsedValues = m_DatasetFamilyComboBox.Text.Split(',');
                        string datasetFamilyIdentifier = comboBoxParsedValues[1].Replace('{', ' ');
                        datasetFamilyIdentifier = datasetFamilyIdentifier.Replace('}', ' ');
                        datasetFamilyIdentifier = datasetFamilyIdentifier.Trim();
                        datasetFamilyIdentifier = datasetFamilyIdentifier.ToLower();
                        m_DatasetProperties.DatasetFamily = datasetFamilyIdentifier;
                        
                    }
                    DatasetPackagerDialog datasetPackagerDialog = new DatasetPackagerDialog(ref m_DatasetProperties, ref m_NotificationAndProgressTracker, m_SaveFileDialog.FileName);
                    datasetPackagerDialog.ShowDialog();
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_AboutToolStripMenuItem_Click(
            object sender,
            EventArgs e
            )
        {
            AboutDialog aboutDialog = new AboutDialog();
            aboutDialog.ShowDialog();
        }

        /// <summary>
        /// This method is used to check if each field contains data and update the status of various Menu items from enabled to disabled
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_UpdateMenuItemStates_Tick(
            object sender,
            EventArgs e
            )
        {
            if ((0 < m_DatasetIdentifierTextBox.Text.Length)&&(0 < m_DatasetTitleTextBox.Text.Length)&&(0 < m_DatasetDescriptionTextBox.Text.Length))
            {
                // We have an identifier, a title and a description. This is enough to allow us to save a template
                m_SaveToolStripMenuItem.Enabled = true;
                if (0 < m_DatasetProperties.GetListOfTablePackageIndexes().Count())
                {
                    m_PublishNowToolStripMenuItem.Enabled = true;
                }
                else
                {
                    m_PublishNowToolStripMenuItem.Enabled = false;
                }
            }
            else
            {
                m_SaveToolStripMenuItem.Enabled = false;
                m_PublishNowToolStripMenuItem.Enabled = false;
            }
        }

        /// <summary>
        /// Private data members
        /// </summary>
        private DatasetProperties m_DatasetProperties;
        private NotificationsAndProgressTracker m_NotificationAndProgressTracker;
        private SailWebApiPortalLoginDialog m_SailWebApiPortalLoginDialog;
        private Dictionary<ulong, uint> m_TableIndexAssociation;
    }
}
