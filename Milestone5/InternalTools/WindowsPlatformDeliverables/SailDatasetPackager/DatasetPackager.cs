using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SailDatasetPackager
{
    public class DatasetPackager
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="datasetProperties"></param>
        /// <param name="notificationsAndProgressTracker"></param>
        public DatasetPackager(
            ref DatasetProperties datasetProperties,
            ref NotificationsAndProgressTracker notificationsAndProgressTracker,
            string datasetFilename
            )
        {
            m_DatasetProperties = datasetProperties;
            m_NotificationsAndProgressTracker = notificationsAndProgressTracker;
            m_DatasetFilename = datasetFilename;
        }

        /// <summary>
        /// 
        /// </summary>
        public void PackageDataset()
        {
            try
            {
                m_NotificationsAndProgressTracker.AddNotification("Process to package the dataset to disk started...");
                bool success = ApiInterop.GenerateDataset(m_DatasetFilename, m_DatasetProperties.Identifier, m_DatasetProperties.Title, m_DatasetProperties.Description, m_DatasetProperties.Tags, m_DatasetProperties.DatasetFamily);
                if (false == success) throw new Exception();
                m_NotificationsAndProgressTracker.AddNotification("Process to publish the dataset to the SAIL Platform started...");
                success = ApiInterop.PublishDataset(m_DatasetFilename);
                if (false == success) throw new Exception();
                m_NotificationsAndProgressTracker.AddNotification("Done.");
            }

            catch
            {
                m_NotificationsAndProgressTracker.AddNotification("ERROR: Something went wrong while trying to package and publish the new dataset.");
                while (0 < ApiInterop.GetExceptionCount())
                {
                    m_NotificationsAndProgressTracker.AddNotification(ApiInterop.GetNextException());
                }
            }
        }

        private DatasetProperties m_DatasetProperties;
        private string m_DatasetFilename;
        private NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
    }
}
