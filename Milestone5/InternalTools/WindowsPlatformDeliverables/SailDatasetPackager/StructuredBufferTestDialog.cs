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
    public partial class StructuredBufferTestDialog : Form
    {
        public StructuredBufferTestDialog()
        {
            InitializeComponent();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ConvertButton_Click(
            object sender,
            EventArgs e
            )
        {
            m_ResultingStructureBufferTextBox.Text = ApiInterop.TestConvertJsonStringToStructuredBuffer(m_SourceJsonStringTextBox.Text);
            m_ReconvertedStructureBufferTextBox.Text = ApiInterop.TestConvertStructuredBufferToStandardJson();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ConvertTypedButton_Click(
            object sender,
            EventArgs e
            )
        {
            m_ResultingStructureBufferTextBox.Text = ApiInterop.TestConvertJsonStringToStructuredBuffer(m_SourceJsonStringTextBox.Text);
            m_ReconvertedStructureBufferTextBox.Text = ApiInterop.TestConvertStructuredBufferToStronglyTypedJson();
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
            this.Close();
        }
    }
}
