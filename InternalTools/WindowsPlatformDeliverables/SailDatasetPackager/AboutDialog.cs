using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Reflection;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SailDatasetPackager
{
    public partial class AboutDialog : Form
    {
        public AboutDialog()
        {
            InitializeComponent();

            System.Reflection.Assembly assembly = System.Reflection.Assembly.GetExecutingAssembly();
            AssemblyFileVersionAttribute fileVersionAttribute = (AssemblyFileVersionAttribute)assembly.GetCustomAttribute(typeof(AssemblyFileVersionAttribute));

            this.label1.Text = "SAIL Dataset Packager Tool\r\nVersion " + fileVersionAttribute.Version + "\r\n" + DateTime.Today.ToString("D") + "\r\nCopyright(C) 2021 Secure AI Labs, Inc.All Rights Reserved";
        }
    }
}
