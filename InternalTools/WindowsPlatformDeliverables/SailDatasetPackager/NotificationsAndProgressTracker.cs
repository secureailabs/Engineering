using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace SailDatasetPackager
{
    public class NotificationsAndProgressTracker
    {
        /// <summary>
        /// 
        /// </summary>
        public NotificationsAndProgressTracker()
        {
            m_Mutex = new Mutex();
            m_Progress = 0;
            m_QueueOfNotifications = new Queue<string>();
            m_Done = false;
        }

        /// <summary>
        /// 
        /// </summary>
        public bool Done
        {
            get
            {
                return m_Done;
            }

            set
            {
                m_Done = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public uint Progress
        {
            get
            {
                return m_Progress;
            }

            set
            {
                m_Progress = value;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="notificationMessage"></param>
        public void AddNotification(
            string notificationMessage
            )
        {
            m_Mutex.WaitOne();
            m_QueueOfNotifications.Enqueue(notificationMessage);
            m_Mutex.ReleaseMutex();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public string GetNextNotification()
        {
            string nextNotification = null;

            m_Mutex.WaitOne();
            if (0 < m_QueueOfNotifications.Count)
            {
                nextNotification = m_QueueOfNotifications.Dequeue();
            }
            m_Mutex.ReleaseMutex();

            return nextNotification;
        }

        private Mutex m_Mutex;
        private bool m_Done;
        private uint m_Progress;
        private Queue<string> m_QueueOfNotifications;
    }
}
