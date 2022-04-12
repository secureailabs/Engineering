namespace SailTablePackagerForCsv
{
    partial class FileSelectionDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FileSelectionDialog));
            this.label1 = new System.Windows.Forms.Label();
            this.m_CvsFilenameTextBox = new System.Windows.Forms.TextBox();
            this.m_BrowseForCsvFileLinkLabel = new System.Windows.Forms.LinkLabel();
            this.m_CancelButton = new System.Windows.Forms.Button();
            this.m_NextButton = new System.Windows.Forms.Button();
            this.m_OpenCvsFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.label2 = new System.Windows.Forms.Label();
            this.m_TemplateFilenameTextBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.m_BrowseForTemplateFileLinkLabel = new System.Windows.Forms.LinkLabel();
            this.m_OpenTemplateFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(12, 52);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(483, 15);
            this.label1.TabIndex = 0;
            this.label1.Text = "(MANDATORY) Please select the CSV file which contains the source data for this ne" +
    "w table.";
            // 
            // m_CvsFilenameTextBox
            // 
            this.m_CvsFilenameTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_CvsFilenameTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_CvsFilenameTextBox.Location = new System.Drawing.Point(15, 70);
            this.m_CvsFilenameTextBox.Name = "m_CvsFilenameTextBox";
            this.m_CvsFilenameTextBox.ReadOnly = true;
            this.m_CvsFilenameTextBox.Size = new System.Drawing.Size(777, 22);
            this.m_CvsFilenameTextBox.TabIndex = 1;
            // 
            // m_BrowseForCsvFileLinkLabel
            // 
            this.m_BrowseForCsvFileLinkLabel.AutoSize = true;
            this.m_BrowseForCsvFileLinkLabel.Location = new System.Drawing.Point(12, 95);
            this.m_BrowseForCsvFileLinkLabel.Name = "m_BrowseForCsvFileLinkLabel";
            this.m_BrowseForCsvFileLinkLabel.Size = new System.Drawing.Size(45, 15);
            this.m_BrowseForCsvFileLinkLabel.TabIndex = 2;
            this.m_BrowseForCsvFileLinkLabel.TabStop = true;
            this.m_BrowseForCsvFileLinkLabel.Text = "Browse";
            this.m_BrowseForCsvFileLinkLabel.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.m_BrowseForFileLinkLabel_LinkClicked);
            // 
            // m_CancelButton
            // 
            this.m_CancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_CancelButton.Location = new System.Drawing.Point(325, 186);
            this.m_CancelButton.Name = "m_CancelButton";
            this.m_CancelButton.Size = new System.Drawing.Size(75, 23);
            this.m_CancelButton.TabIndex = 3;
            this.m_CancelButton.Text = "&Cancel";
            this.m_CancelButton.UseVisualStyleBackColor = true;
            this.m_CancelButton.Click += new System.EventHandler(this.m_CancelButton_Click);
            // 
            // m_NextButton
            // 
            this.m_NextButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_NextButton.Location = new System.Drawing.Point(406, 186);
            this.m_NextButton.Name = "m_NextButton";
            this.m_NextButton.Size = new System.Drawing.Size(75, 23);
            this.m_NextButton.TabIndex = 4;
            this.m_NextButton.Text = "&Next";
            this.m_NextButton.UseVisualStyleBackColor = true;
            this.m_NextButton.Click += new System.EventHandler(this.m_NextButton_Click);
            // 
            // m_OpenCvsFileDialog
            // 
            this.m_OpenCvsFileDialog.DefaultExt = "csv";
            this.m_OpenCvsFileDialog.Filter = "CSV Files|*.csv";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 9);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(780, 30);
            this.label2.TabIndex = 5;
            this.label2.Text = resources.GetString("label2.Text");
            // 
            // m_TemplateFilenameTextBox
            // 
            this.m_TemplateFilenameTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TemplateFilenameTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TemplateFilenameTextBox.Location = new System.Drawing.Point(15, 138);
            this.m_TemplateFilenameTextBox.Name = "m_TemplateFilenameTextBox";
            this.m_TemplateFilenameTextBox.ReadOnly = true;
            this.m_TemplateFilenameTextBox.Size = new System.Drawing.Size(777, 22);
            this.m_TemplateFilenameTextBox.TabIndex = 7;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(12, 120);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(492, 15);
            this.label3.TabIndex = 6;
            this.label3.Text = "(OPTIONAL) Please select the template file which contains the source data for thi" +
    "s new table.";
            // 
            // m_BrowseForTemplateFileLinkLabel
            // 
            this.m_BrowseForTemplateFileLinkLabel.AutoSize = true;
            this.m_BrowseForTemplateFileLinkLabel.Location = new System.Drawing.Point(12, 163);
            this.m_BrowseForTemplateFileLinkLabel.Name = "m_BrowseForTemplateFileLinkLabel";
            this.m_BrowseForTemplateFileLinkLabel.Size = new System.Drawing.Size(45, 15);
            this.m_BrowseForTemplateFileLinkLabel.TabIndex = 8;
            this.m_BrowseForTemplateFileLinkLabel.TabStop = true;
            this.m_BrowseForTemplateFileLinkLabel.Text = "Browse";
            this.m_BrowseForTemplateFileLinkLabel.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.m_BrowseForTemplateFileLinkLabel_LinkClicked);
            // 
            // m_OpenTemplateFileDialog
            // 
            this.m_OpenTemplateFileDialog.DefaultExt = "stpt";
            this.m_OpenTemplateFileDialog.Filter = "Template Files|*.stpt";
            // 
            // FileSelectionDialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(804, 222);
            this.Controls.Add(this.m_TemplateFilenameTextBox);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.m_BrowseForTemplateFileLinkLabel);
            this.Controls.Add(this.m_CvsFilenameTextBox);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.m_BrowseForCsvFileLinkLabel);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.m_NextButton);
            this.Controls.Add(this.m_CancelButton);
            this.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(2);
            this.Name = "FileSelectionDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Table Packager for CSV Files";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox m_CvsFilenameTextBox;
        private System.Windows.Forms.LinkLabel m_BrowseForCsvFileLinkLabel;
        private System.Windows.Forms.Button m_CancelButton;
        private System.Windows.Forms.Button m_NextButton;
        private System.Windows.Forms.OpenFileDialog m_OpenCvsFileDialog;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox m_TemplateFilenameTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.LinkLabel m_BrowseForTemplateFileLinkLabel;
        private System.Windows.Forms.OpenFileDialog m_OpenTemplateFileDialog;
    }
}

