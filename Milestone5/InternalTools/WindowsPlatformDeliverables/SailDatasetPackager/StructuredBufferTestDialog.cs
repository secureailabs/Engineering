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
        /// <summary>
        /// 
        /// </summary>
        public StructuredBufferTestDialog()
        {
            InitializeComponent();

            System.IO.StreamReader reader;
            char ch;
            uint[] characterCounts = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

            reader = new System.IO.StreamReader(@"passwords2.txt");
            do
            {
                ch = (char)reader.Read();
                if (128 > ch)
                {
                    characterCounts[ch]++;
                }
            }
            while (!reader.EndOfStream);
            reader.Close();
            reader.Dispose();
            foreach (uint characterCount in characterCounts)
            {
                m_ResultingStructureBufferTextBox.Text += characterCount.ToString() + ",";
            }
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
