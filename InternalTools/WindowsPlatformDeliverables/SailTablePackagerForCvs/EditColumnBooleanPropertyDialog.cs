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
    public partial class EditColumnBooleanPropertyDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="propertyName"></param>
        /// <param name="propertyValue"></param>
        public EditColumnBooleanPropertyDialog(
            string propertyName,
            bool propertyValue
            )
        {
            InitializeComponent();

            this.Text = "Edit Column Property (" + propertyName + ")";
            if (true == propertyValue)
            {
                m_TrueRadioButton.Checked = true;
                m_FalseRadioButton.Checked = false;
            }
            else
            {
                m_TrueRadioButton.Checked = false;
                m_FalseRadioButton.Checked = true;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public bool PropertyValue
        {
            get
            {
                return m_TrueRadioButton.Checked;
            }
        }
    }
}
