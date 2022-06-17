using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailDatasetPackager
{
    public partial class DatasetPackagerDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        public DatasetPackagerDialog(
            ref DatasetProperties datasetProperties,
            ref NotificationsAndProgressTracker notificationsAndProgressTracker,
            string datasetFilename
            )
        {
            InitializeComponent();

            this.Text = Program.m_AssemblyTitle;
            m_DatasetPackager = new DatasetPackager(ref datasetProperties, ref notificationsAndProgressTracker, datasetFilename);
            m_NotificationsAndProgressTracker = notificationsAndProgressTracker;
            // Now let's run the worker thread. Make sure to update button states since they
            // will not be usable while the worker thread is running
            m_DoneButton.Enabled = false;
            Thread workerThread = new Thread(new ThreadStart(WorkerThread));
            workerThread.Start();
        }

        /// <summary>
        /// 
        /// </summary>
        private void WorkerThread()
        {
            m_DatasetPackager.PackageDataset(false);
            m_NotificationsAndProgressTracker.Done = true;
            m_DoneButton.Enabled = false;
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
            // First we print out all of the lingering notifications
            string notificationString = null;
            do
            {
                notificationString = m_NotificationsAndProgressTracker.GetNextNotification();
                if (null != notificationString)
                {
                    m_NotificationsListBox.Items.Add(notificationString);
                }
            }
            while (null != notificationString);
            // Now we check if we are done.
            if (true == m_NotificationsAndProgressTracker.Done)
            {
                m_RefreshTimer.Enabled = false;
                m_DoneButton.Enabled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_DoneButton_Click(
            object sender,
            EventArgs e
            )
        {
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        DatasetPackager m_DatasetPackager;
        NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
    }
}
