using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace SailTablePackagerForCsv
{
    public class TablePackagerCli
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="tableProperties"></param>
        /// <param name="destinationFilename"></param>
        public TablePackagerCli(
            ref TableProperties tableProperties,
            string destinationFilename
            )
        {
            m_TableProperties = tableProperties;
            m_NotificationsAndProgressTracker = new NotificationsAndProgressTracker();
            m_TableProperties.SetTableProperty("DestinationIntermediateFile", destinationFilename);
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
        /// <returns></returns>
        public int PackageTable()
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
            Console.WriteLine("Done!!!");

            return 15;
        }

        private NotificationsAndProgressTracker m_NotificationsAndProgressTracker;
        private TableProperties m_TableProperties;
    }
}
