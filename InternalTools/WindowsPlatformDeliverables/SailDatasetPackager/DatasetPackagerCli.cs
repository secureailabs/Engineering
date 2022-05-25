using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace SailDatasetPackager
{
    public class DatasetPackagerCli
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="datasetProperties"></param>
        /// <param name="notificationsAndProgressTracker"></param>
        /// <param name="datasetFilename"></param>
        public DatasetPackagerCli(
            ref DatasetProperties datasetProperties,
            ref NotificationsAndProgressTracker notificationsAndProgressTracker,
            string datasetFilename
            )
        {
            m_DatasetPackager = new DatasetPackager(ref datasetProperties, ref notificationsAndProgressTracker, datasetFilename);
            m_NotificationsAndProgressTracker = notificationsAndProgressTracker;
        }

        /// <summary>
        /// 
        /// </summary>
        private void WorkerThread()
        {
            m_DatasetPackager.PackageDataset(true);
            m_NotificationsAndProgressTracker.Done = true;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sailPlatformAddress"></param>
        /// <param name="username"></param>
        /// <param name="password"></param>
        public void PackageDataset(
            string sailPlatformAddress,
            string username,
            string password
            )
        {
            bool isLoggedOn = ApiInterop.IsLoggedOn();
            if (false == isLoggedOn)
            {
                isLoggedOn = ApiInterop.Login(sailPlatformAddress, username, password);
            }

            if (false == ApiInterop.IsLoggedOn())
            {
                m_NotificationsAndProgressTracker.AddNotification("ERROR: Unable to connect to SAIL Platform Services. Operation terminated.");
            }
            else
            {
                // Start the worker thread
                Thread workerThread = new Thread(new ThreadStart(WorkerThread));
                workerThread.Start();
                // Now just spin there and print notification messages
                while (false == m_NotificationsAndProgressTracker.Done)
                {
                    string notificationMessage = null;
                    do
                    {
                        notificationMessage = m_NotificationsAndProgressTracker.GetNextNotification();
                        if (null != notificationMessage)
                        {
                            Console.WriteLine(notificationMessage);
                        }
                    }
                    while (null != notificationMessage);
                }
            }
        }

        private DatasetPackager m_DatasetPackager;
        NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
    }
}
