using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using CsvHelper;
using CsvHelper.Configuration;

namespace SailTablePackagerForCsv
{
    public partial class TablePackagerDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tableProperties"></param>
        public TablePackagerDialog(
            ref TableProperties tableProperties
            )
        {
            InitializeComponent();

            m_TableProperties = tableProperties;
            m_NotificationsAndProgressTracker = new NotificationsAndProgressTracker();
        }

        /// <summary>
        /// 
        /// </summary>
        private void WorkerThread()
        {
            TablePackager tablePackager = new TablePackager(ref m_TableProperties, ref m_NotificationsAndProgressTracker);
            tablePackager.PackageTable();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_GoButton_Click(
            object sender,
            EventArgs e
            )
        {
            // We need to figure out whether or not the table property "DestinationIntermediateFile" already exists. If
            // it does, we do not present the save file dialog
            string[] tableProperties = m_TableProperties.GetTableProperties();
            this.m_SaveFileDialog.Filter = "Packaged Table|*.sailtable";
            this.m_SaveFileDialog.Title = "Select the name of the SAIL Table Package file to save to...";
            if ((false == tableProperties.Contains("DestinationIntermediateFile")) && (DialogResult.OK == m_SaveFileDialog.ShowDialog()))
            {
                // Update the m_TableProperties structure with the destination file
                m_TableProperties.SetTableProperty("DestinationIntermediateFile", m_SaveFileDialog.FileName);
                tableProperties = m_TableProperties.GetTableProperties();
            }
            // By now, regardless of whether or not the save file dialog was displayed, we should
            // have a value "DestinationIntermediateFile" table property. If not, exit.
            if (true == tableProperties.Contains("DestinationIntermediateFile"))
            {
                // Now let's run the worker thread. Make sure to update button states since they
                // will not be usable while the worker thread is running
                m_ExitButton.Enabled = false;
                m_GoButton.Enabled = false;
                m_RefreshTimer.Enabled = true;
                Thread workerThread = new Thread(new ThreadStart(WorkerThread));
                workerThread.Start();
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ExitButton_Click(
            object sender,
            EventArgs e
            )
        {
            if (true == m_NotificationsAndProgressTracker.Done)
            {
                this.DialogResult = DialogResult.OK;
            }
            else
            {
                this.DialogResult = DialogResult.Cancel;
            }
            this.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_RefreshTimer_Tick(
            object sender,
            EventArgs e
            )
        {
            // Display any new notifications, one by one
            string newNotification = null;
            do
            {
                newNotification = m_NotificationsAndProgressTracker.GetNextNotification();
                if (null != newNotification)
                {
                    m_NotificationsListBox.Items.Add(newNotification);
                    m_NotificationsListBox.SelectedIndex = m_NotificationsListBox.Items.Count - 1;
                }
            }
            while (null != newNotification);
            // Update the progress bar
            m_ProgressTextBox.Text = m_NotificationsAndProgressTracker.Progress.ToString() + " have been processed.";
            // Check to see if we are done
            if (true == m_NotificationsAndProgressTracker.Done)
            {
                m_RefreshTimer.Enabled = false;
                m_ExitButton.Enabled = true;
                // Ask for the name of the file to save the template to
                this.m_SaveFileDialog.Filter = "Packaged Table Template|*.stpt";
                this.m_SaveFileDialog.Title = "Select the name of the template file to save to...";
                if (DialogResult.OK == m_SaveFileDialog.ShowDialog())
                {
                    m_TableProperties.SaveTemplateToDisk(m_SaveFileDialog.FileName);
                    m_NotificationsListBox.Items.Add("Saved template file to " + m_SaveFileDialog.FileName);
                    m_NotificationsListBox.SelectedIndex = m_NotificationsListBox.Items.Count - 1;
                }
            }
        }

        private NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
        private TableProperties m_TableProperties;
    }
}
