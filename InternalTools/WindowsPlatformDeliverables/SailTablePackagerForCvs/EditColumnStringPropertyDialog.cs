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
    public partial class EditColumnStringPropertyDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="propertyName"></param>
        /// <param name="propertyValue"></param>
        public EditColumnStringPropertyDialog(
            string propertyName,
            string propertyValue
            )
        {
            InitializeComponent();

            this.Text = "Edit Column Property (" + propertyName + ")";
            m_PropertyTextBox.Text = propertyValue;
            m_DescriptionLabel.Text = "Property Value for (" + propertyName + ")";
        }

        /// <summary>
        /// 
        /// </summary>
        public string PropertyValue
        {
            get
            {
                return m_PropertyTextBox.Text;
            }
        }
    }
}
