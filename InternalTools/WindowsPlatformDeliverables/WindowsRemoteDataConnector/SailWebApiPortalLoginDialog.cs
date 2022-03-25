﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Win32;
using System.Windows.Forms;

namespace WindowsRemoteDataConnector
{
    public partial class SailWebApiPortalLoginDialog : Form
    {
        /// <summary>
        /// 
        /// </summary>
        public SailWebApiPortalLoginDialog()
        {
            InitializeComponent();

            // Load default settings from the registry of they exist
            RegistryKey registryKey = Registry.CurrentUser.CreateSubKey(@"SOFTWARE\SAIL");
            string[] registryKeyValues = registryKey.GetValueNames();
            if (true == registryKeyValues.Contains("DefaultSailWebApiPortalIpAddress"))
            {
                m_IpAddressTextBox.Text = registryKey.GetValue("DefaultSailWebApiPortalIpAddress").ToString();
            }
            if (true == registryKeyValues.Contains("DefaultSailWebApiPortalUsername"))
            {
                m_UsernameEditBox.Text = registryKey.GetValue("DefaultSailWebApiPortalUsername").ToString();
            }
            registryKey.Close();

            if ("" != m_IpAddressTextBox.Text)
            {
                if ("" != m_UsernameEditBox.Text)
                {
                    m_PasswordEditBox.Select();
                }
                else
                {
                    m_UsernameEditBox.Select();
                }
            }

            m_ValidUsername = "";
            m_ValidPassword = "";
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_LoginButton_Click(
            object sender,
            EventArgs e
            )
        {
            if (("" == m_IpAddressTextBox.Text) || ("" == m_UsernameEditBox.Text) || ("" == m_PasswordEditBox.Text))
            {
                MessageBox.Show(this, "Missing input!!!\r\nAll three input fields must be specified.", "Error!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                bool successfulLogin = SailWebApiPortalInterop.Login(m_IpAddressTextBox.Text, m_UsernameEditBox.Text, m_PasswordEditBox.Text);
                if (false == successfulLogin)
                {
                    MessageBox.Show(this, "Invalid credentials provided. Try again!!", "Authentication Failure", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    // Persist some of the settings to the registry to make it easier to restart the
                    // application later.
                    RegistryKey registryKey = Registry.CurrentUser.CreateSubKey(@"SOFTWARE\SAIL");
                    registryKey.SetValue("DefaultSailWebApiPortalIpAddress", m_IpAddressTextBox.Text);
                    registryKey.SetValue("DefaultSailWebApiPortalUsername", m_UsernameEditBox.Text);
                    registryKey.Close();
                    this.DialogResult = DialogResult.OK;
                    this.m_RefreshTimer.Stop();
                    this.Close();
                    // Make sure that the successful login updates the valid username and password
                    m_ValidIpAddress = m_IpAddressTextBox.Text;
                    m_ValidUsername = m_UsernameEditBox.Text;
                    m_ValidPassword = m_PasswordEditBox.Text;
                }
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string IpAddress
        {
            get
            {
                return m_ValidIpAddress;
            }
        }
        /// <summary>
        /// 
        /// </summary>
        public string Username
        {
            get
            {
                return m_ValidUsername;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        public string Password
        {
            get
            {
                return m_ValidPassword;
            }
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
            this.m_RefreshTimer.Stop();
            this.Close();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_ExceptionsStripStatusLabel_Click(
            object sender,
            EventArgs e
            )
        {
            
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void m_RefreshTimer_Tick(
            object sender,
            EventArgs e
            )
        {
            
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void SailWebApiPortalLoginDialog_Load(
            object sender,
            EventArgs e
            )
        {

        }

        private string m_ValidIpAddress;
        private string m_ValidUsername;
        private string m_ValidPassword;
    }
}