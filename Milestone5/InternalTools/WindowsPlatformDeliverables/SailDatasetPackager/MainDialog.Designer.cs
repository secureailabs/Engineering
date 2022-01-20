namespace SailDatasetPackager
{
    partial class MainDialog
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.m_TablesListBox = new System.Windows.Forms.ListBox();
            this.m_TablesListBoxContextMenuStrip = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.m_AddExistingItemToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_DeleteTableToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.m_DatasetIdentifierTextBox = new System.Windows.Forms.TextBox();
            this.m_DatasetTitleTextBox = new System.Windows.Forms.TextBox();
            this.m_DatasetDescriptionTextBox = new System.Windows.Forms.TextBox();
            this.m_DatasetTagsTextBox = new System.Windows.Forms.TextBox();
            this.m_DatasetFamilyComboBox = new System.Windows.Forms.ComboBox();
            this.m_TablesGroupBox = new System.Windows.Forms.GroupBox();
            this.label6 = new System.Windows.Forms.Label();
            this.m_MainMenuStrip = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_NewToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_OpenToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_SaveToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_CloseToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.m_ExitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.publishToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_PublishNowToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_AboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_SaveFileDialog = new System.Windows.Forms.SaveFileDialog();
            this.m_OpenFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.m_RefreshDatasetFamiliesLinkLabel = new System.Windows.Forms.LinkLabel();
            this.m_UpdateMenuItemStates = new System.Windows.Forms.Timer(this.components);
            this.m_TablesListBoxContextMenuStrip.SuspendLayout();
            this.m_TablesGroupBox.SuspendLayout();
            this.m_MainMenuStrip.SuspendLayout();
            this.SuspendLayout();
            // 
            // m_TablesListBox
            // 
            this.m_TablesListBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TablesListBox.ContextMenuStrip = this.m_TablesListBoxContextMenuStrip;
            this.m_TablesListBox.FormattingEnabled = true;
            this.m_TablesListBox.IntegralHeight = false;
            this.m_TablesListBox.ItemHeight = 14;
            this.m_TablesListBox.Location = new System.Drawing.Point(21, 44);
            this.m_TablesListBox.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.m_TablesListBox.Name = "m_TablesListBox";
            this.m_TablesListBox.Size = new System.Drawing.Size(823, 187);
            this.m_TablesListBox.Sorted = true;
            this.m_TablesListBox.TabIndex = 0;
            this.m_TablesListBox.SelectedIndexChanged += new System.EventHandler(this.m_TablesListBox_SelectedIndexChanged);
            // 
            // m_TablesListBoxContextMenuStrip
            // 
            this.m_TablesListBoxContextMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.m_AddExistingItemToolStripMenuItem,
            this.m_DeleteTableToolStripMenuItem});
            this.m_TablesListBoxContextMenuStrip.Name = "m_TablesListBoxContextMenuStrip";
            this.m_TablesListBoxContextMenuStrip.Size = new System.Drawing.Size(171, 48);
            // 
            // m_AddExistingItemToolStripMenuItem
            // 
            this.m_AddExistingItemToolStripMenuItem.Name = "m_AddExistingItemToolStripMenuItem";
            this.m_AddExistingItemToolStripMenuItem.Size = new System.Drawing.Size(170, 22);
            this.m_AddExistingItemToolStripMenuItem.Text = "Add Existing Table";
            this.m_AddExistingItemToolStripMenuItem.Click += new System.EventHandler(this.m_AddExistingItemToolStripMenuItem_Click);
            // 
            // m_DeleteTableToolStripMenuItem
            // 
            this.m_DeleteTableToolStripMenuItem.Name = "m_DeleteTableToolStripMenuItem";
            this.m_DeleteTableToolStripMenuItem.Size = new System.Drawing.Size(170, 22);
            this.m_DeleteTableToolStripMenuItem.Text = "Delete Table";
            this.m_DeleteTableToolStripMenuItem.Click += new System.EventHandler(this.m_DeleteTableToolStripMenuItem_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(14, 42);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(133, 14);
            this.label1.TabIndex = 1;
            this.label1.Text = "Dataset Identifier";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(49, 70);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(98, 14);
            this.label2.TabIndex = 2;
            this.label2.Text = "Dataset Title";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(7, 123);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(140, 14);
            this.label3.TabIndex = 3;
            this.label3.Text = "Dataset Description";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(56, 188);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(91, 14);
            this.label4.TabIndex = 4;
            this.label4.Text = "Dataset Tags";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(42, 216);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(105, 14);
            this.label5.TabIndex = 5;
            this.label5.Text = "Dataset Family";
            // 
            // m_DatasetIdentifierTextBox
            // 
            this.m_DatasetIdentifierTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_DatasetIdentifierTextBox.CharacterCasing = System.Windows.Forms.CharacterCasing.Lower;
            this.m_DatasetIdentifierTextBox.Location = new System.Drawing.Point(153, 39);
            this.m_DatasetIdentifierTextBox.Name = "m_DatasetIdentifierTextBox";
            this.m_DatasetIdentifierTextBox.ReadOnly = true;
            this.m_DatasetIdentifierTextBox.Size = new System.Drawing.Size(311, 22);
            this.m_DatasetIdentifierTextBox.TabIndex = 6;
            this.m_DatasetIdentifierTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // m_DatasetTitleTextBox
            // 
            this.m_DatasetTitleTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_DatasetTitleTextBox.Location = new System.Drawing.Point(153, 67);
            this.m_DatasetTitleTextBox.Name = "m_DatasetTitleTextBox";
            this.m_DatasetTitleTextBox.Size = new System.Drawing.Size(729, 22);
            this.m_DatasetTitleTextBox.TabIndex = 7;
            // 
            // m_DatasetDescriptionTextBox
            // 
            this.m_DatasetDescriptionTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_DatasetDescriptionTextBox.Location = new System.Drawing.Point(153, 95);
            this.m_DatasetDescriptionTextBox.Multiline = true;
            this.m_DatasetDescriptionTextBox.Name = "m_DatasetDescriptionTextBox";
            this.m_DatasetDescriptionTextBox.Size = new System.Drawing.Size(729, 84);
            this.m_DatasetDescriptionTextBox.TabIndex = 8;
            // 
            // m_DatasetTagsTextBox
            // 
            this.m_DatasetTagsTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_DatasetTagsTextBox.Location = new System.Drawing.Point(153, 185);
            this.m_DatasetTagsTextBox.Name = "m_DatasetTagsTextBox";
            this.m_DatasetTagsTextBox.Size = new System.Drawing.Size(729, 22);
            this.m_DatasetTagsTextBox.TabIndex = 9;
            // 
            // m_DatasetFamilyComboBox
            // 
            this.m_DatasetFamilyComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.m_DatasetFamilyComboBox.FormattingEnabled = true;
            this.m_DatasetFamilyComboBox.Location = new System.Drawing.Point(153, 213);
            this.m_DatasetFamilyComboBox.Name = "m_DatasetFamilyComboBox";
            this.m_DatasetFamilyComboBox.Size = new System.Drawing.Size(528, 22);
            this.m_DatasetFamilyComboBox.TabIndex = 10;
            // 
            // m_TablesGroupBox
            // 
            this.m_TablesGroupBox.Controls.Add(this.label6);
            this.m_TablesGroupBox.Controls.Add(this.m_TablesListBox);
            this.m_TablesGroupBox.Location = new System.Drawing.Point(10, 241);
            this.m_TablesGroupBox.Name = "m_TablesGroupBox";
            this.m_TablesGroupBox.Size = new System.Drawing.Size(872, 252);
            this.m_TablesGroupBox.TabIndex = 11;
            this.m_TablesGroupBox.TabStop = false;
            this.m_TablesGroupBox.Text = "Tables";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(18, 27);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(553, 14);
            this.label6.TabIndex = 12;
            this.label6.Text = "Use the right click context menu to Add/Edit/Remove tables from the list below";
            // 
            // m_MainMenuStrip
            // 
            this.m_MainMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.publishToolStripMenuItem,
            this.aboutToolStripMenuItem});
            this.m_MainMenuStrip.Location = new System.Drawing.Point(0, 0);
            this.m_MainMenuStrip.Name = "m_MainMenuStrip";
            this.m_MainMenuStrip.Size = new System.Drawing.Size(897, 24);
            this.m_MainMenuStrip.TabIndex = 12;
            this.m_MainMenuStrip.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.m_NewToolStripMenuItem,
            this.m_OpenToolStripMenuItem,
            this.m_SaveToolStripMenuItem,
            this.m_CloseToolStripMenuItem,
            this.toolStripSeparator1,
            this.m_ExitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "&File";
            // 
            // m_NewToolStripMenuItem
            // 
            this.m_NewToolStripMenuItem.Name = "m_NewToolStripMenuItem";
            this.m_NewToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.m_NewToolStripMenuItem.Text = "&New";
            this.m_NewToolStripMenuItem.Click += new System.EventHandler(this.m_NewToolStripMenuItem_Click);
            // 
            // m_OpenToolStripMenuItem
            // 
            this.m_OpenToolStripMenuItem.Name = "m_OpenToolStripMenuItem";
            this.m_OpenToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.m_OpenToolStripMenuItem.Text = "&Open";
            this.m_OpenToolStripMenuItem.Click += new System.EventHandler(this.m_OpenToolStripMenuItem_Click);
            // 
            // m_SaveToolStripMenuItem
            // 
            this.m_SaveToolStripMenuItem.Name = "m_SaveToolStripMenuItem";
            this.m_SaveToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.m_SaveToolStripMenuItem.Text = "&Save";
            this.m_SaveToolStripMenuItem.Click += new System.EventHandler(this.m_SaveToolStripMenuItem_Click);
            // 
            // m_CloseToolStripMenuItem
            // 
            this.m_CloseToolStripMenuItem.Name = "m_CloseToolStripMenuItem";
            this.m_CloseToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.m_CloseToolStripMenuItem.Text = "&Close";
            this.m_CloseToolStripMenuItem.Click += new System.EventHandler(this.m_CloseToolStripMenuItem_Click);
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(100, 6);
            // 
            // m_ExitToolStripMenuItem
            // 
            this.m_ExitToolStripMenuItem.Name = "m_ExitToolStripMenuItem";
            this.m_ExitToolStripMenuItem.Size = new System.Drawing.Size(103, 22);
            this.m_ExitToolStripMenuItem.Text = "E&xit";
            this.m_ExitToolStripMenuItem.Click += new System.EventHandler(this.m_ExitToolStripMenuItem_Click);
            // 
            // publishToolStripMenuItem
            // 
            this.publishToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.m_PublishNowToolStripMenuItem});
            this.publishToolStripMenuItem.Name = "publishToolStripMenuItem";
            this.publishToolStripMenuItem.Size = new System.Drawing.Size(58, 20);
            this.publishToolStripMenuItem.Text = "&Publish";
            // 
            // m_PublishNowToolStripMenuItem
            // 
            this.m_PublishNowToolStripMenuItem.Name = "m_PublishNowToolStripMenuItem";
            this.m_PublishNowToolStripMenuItem.Size = new System.Drawing.Size(141, 22);
            this.m_PublishNowToolStripMenuItem.Text = "Publish &Now";
            this.m_PublishNowToolStripMenuItem.Click += new System.EventHandler(this.m_PublishNowToolStripMenuItem_Click);
            // 
            // aboutToolStripMenuItem
            // 
            this.aboutToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.m_AboutToolStripMenuItem});
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(44, 20);
            this.aboutToolStripMenuItem.Text = "&Help";
            // 
            // m_AboutToolStripMenuItem
            // 
            this.m_AboutToolStripMenuItem.Name = "m_AboutToolStripMenuItem";
            this.m_AboutToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.m_AboutToolStripMenuItem.Text = "A&bout";
            this.m_AboutToolStripMenuItem.Click += new System.EventHandler(this.m_AboutToolStripMenuItem_Click);
            // 
            // m_OpenFileDialog
            // 
            this.m_OpenFileDialog.Filter = "Packaged Table|*.sailtable";
            // 
            // m_RefreshDatasetFamiliesLinkLabel
            // 
            this.m_RefreshDatasetFamiliesLinkLabel.AutoSize = true;
            this.m_RefreshDatasetFamiliesLinkLabel.Location = new System.Drawing.Point(688, 216);
            this.m_RefreshDatasetFamiliesLinkLabel.Name = "m_RefreshDatasetFamiliesLinkLabel";
            this.m_RefreshDatasetFamiliesLinkLabel.Size = new System.Drawing.Size(49, 14);
            this.m_RefreshDatasetFamiliesLinkLabel.TabIndex = 13;
            this.m_RefreshDatasetFamiliesLinkLabel.TabStop = true;
            this.m_RefreshDatasetFamiliesLinkLabel.Text = "Update";
            this.m_RefreshDatasetFamiliesLinkLabel.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.m_RefreshDatasetFamiliesLinkLabel_LinkClicked);
            // 
            // m_UpdateMenuItemStates
            // 
            this.m_UpdateMenuItemStates.Enabled = true;
            this.m_UpdateMenuItemStates.Tick += new System.EventHandler(this.m_UpdateMenuItemStates_Tick);
            // 
            // MainDialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(897, 504);
            this.ControlBox = false;
            this.Controls.Add(this.m_RefreshDatasetFamiliesLinkLabel);
            this.Controls.Add(this.m_TablesGroupBox);
            this.Controls.Add(this.m_DatasetFamilyComboBox);
            this.Controls.Add(this.m_DatasetTagsTextBox);
            this.Controls.Add(this.m_DatasetDescriptionTextBox);
            this.Controls.Add(this.m_DatasetTitleTextBox);
            this.Controls.Add(this.m_DatasetIdentifierTextBox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.m_MainMenuStrip);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MainMenuStrip = this.m_MainMenuStrip;
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "MainDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Dataset Packager";
            this.m_TablesListBoxContextMenuStrip.ResumeLayout(false);
            this.m_TablesGroupBox.ResumeLayout(false);
            this.m_TablesGroupBox.PerformLayout();
            this.m_MainMenuStrip.ResumeLayout(false);
            this.m_MainMenuStrip.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListBox m_TablesListBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox m_DatasetIdentifierTextBox;
        private System.Windows.Forms.TextBox m_DatasetTitleTextBox;
        private System.Windows.Forms.TextBox m_DatasetDescriptionTextBox;
        private System.Windows.Forms.TextBox m_DatasetTagsTextBox;
        private System.Windows.Forms.ComboBox m_DatasetFamilyComboBox;
        private System.Windows.Forms.GroupBox m_TablesGroupBox;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.MenuStrip m_MainMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_OpenToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_SaveToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_CloseToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
        private System.Windows.Forms.ToolStripMenuItem m_ExitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem publishToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_PublishNowToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem;
        private System.Windows.Forms.SaveFileDialog m_SaveFileDialog;
        private System.Windows.Forms.OpenFileDialog m_OpenFileDialog;
        private System.Windows.Forms.LinkLabel m_RefreshDatasetFamiliesLinkLabel;
        private System.Windows.Forms.ContextMenuStrip m_TablesListBoxContextMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem m_DeleteTableToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_AboutToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_NewToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_AddExistingItemToolStripMenuItem;
        private System.Windows.Forms.Timer m_UpdateMenuItemStates;
    }
}

