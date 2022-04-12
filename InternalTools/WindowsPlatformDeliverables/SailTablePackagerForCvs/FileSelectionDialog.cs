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
    public partial class FileSelectionDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        public FileSelectionDialog()
        {
            InitializeComponent();

            // By default, the next button is disabled, until a valid filename has been
            // selected
            m_NextButton.Enabled = false;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_CancelButton_Click(
            object sender,
            EventArgs e
            )
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_BrowseForFileLinkLabel_LinkClicked(
            object sender,
            LinkLabelLinkClickedEventArgs e
            )
        {
            if (DialogResult.OK == m_OpenCvsFileDialog.ShowDialog())
            {
                m_CvsFilenameTextBox.Text = m_OpenCvsFileDialog.FileName;
                m_NextButton.Enabled = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_BrowseForTemplateFileLinkLabel_LinkClicked(
            object sender,
            LinkLabelLinkClickedEventArgs e
            )
        {
            if (DialogResult.OK == m_OpenTemplateFileDialog.ShowDialog())
            {
                m_TemplateFilenameTextBox.Text = m_OpenTemplateFileDialog.FileName;
            }
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
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        public string CsvFilename
        {
            get
            {
                return m_CvsFilenameTextBox.Text;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string TemplateFilename
        {
            get
            {
                return m_TemplateFilenameTextBox.Text;
            }
        }
    }
}
