namespace SailTablePackagerForCsv
{
    partial class GlobalImportPropertiesDialog
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
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle1 = new System.Windows.Forms.DataGridViewCellStyle();
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle2 = new System.Windows.Forms.DataGridViewCellStyle();
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle3 = new System.Windows.Forms.DataGridViewCellStyle();
            this.label1 = new System.Windows.Forms.Label();
            this.m_SettingsGroupBox = new System.Windows.Forms.GroupBox();
            this.label10 = new System.Windows.Forms.Label();
            this.m_EscapeCharacterTextBox = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.m_QuoteCharacterTextBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.m_ParseCommentLinesCheckBox = new System.Windows.Forms.CheckBox();
            this.m_LineCommentCharacterTextBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.m_FirstLineHeadersCheckBox = new System.Windows.Forms.CheckBox();
            this.label3 = new System.Windows.Forms.Label();
            this.m_ValueSeparatorCharacterTextBox = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.m_LoadSettingsFromTemplateFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.m_DatasetViewPanel = new System.Windows.Forms.Panel();
            this.m_PreviewDataGrid = new System.Windows.Forms.DataGridView();
            this.m_NextButton = new System.Windows.Forms.Button();
            this.m_BackButton = new System.Windows.Forms.Button();
            this.m_SettingsGroupBox.SuspendLayout();
            this.m_DatasetViewPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.m_PreviewDataGrid)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(10, 8);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(1183, 28);
            this.label1.TabIndex = 0;
            this.label1.Text = "STEP 2: Select the settings to use for data importation. Different files might us" +
    "e different setting, so make sure to specify the correct settings here or the fi" +
    "le will\r\nnot be imported properly.";
            // 
            // m_SettingsGroupBox
            // 
            this.m_SettingsGroupBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.m_SettingsGroupBox.Controls.Add(this.label10);
            this.m_SettingsGroupBox.Controls.Add(this.m_EscapeCharacterTextBox);
            this.m_SettingsGroupBox.Controls.Add(this.label9);
            this.m_SettingsGroupBox.Controls.Add(this.label8);
            this.m_SettingsGroupBox.Controls.Add(this.label7);
            this.m_SettingsGroupBox.Controls.Add(this.m_QuoteCharacterTextBox);
            this.m_SettingsGroupBox.Controls.Add(this.label6);
            this.m_SettingsGroupBox.Controls.Add(this.m_ParseCommentLinesCheckBox);
            this.m_SettingsGroupBox.Controls.Add(this.m_LineCommentCharacterTextBox);
            this.m_SettingsGroupBox.Controls.Add(this.label5);
            this.m_SettingsGroupBox.Controls.Add(this.label4);
            this.m_SettingsGroupBox.Controls.Add(this.m_FirstLineHeadersCheckBox);
            this.m_SettingsGroupBox.Controls.Add(this.label3);
            this.m_SettingsGroupBox.Controls.Add(this.m_ValueSeparatorCharacterTextBox);
            this.m_SettingsGroupBox.Controls.Add(this.label2);
            this.m_SettingsGroupBox.Location = new System.Drawing.Point(13, 45);
            this.m_SettingsGroupBox.Name = "m_SettingsGroupBox";
            this.m_SettingsGroupBox.Size = new System.Drawing.Size(837, 175);
            this.m_SettingsGroupBox.TabIndex = 1;
            this.m_SettingsGroupBox.TabStop = false;
            this.m_SettingsGroupBox.Text = "Settings";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Font = new System.Drawing.Font("Segoe UI Semilight", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label10.Location = new System.Drawing.Point(193, 146);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(563, 15);
            this.label10.TabIndex = 16;
            this.label10.Text = "(character used to allow for the quote character to be escaped so that it may be " +
    "contained within strings, etc...)";
            // 
            // m_EscapeCharacterTextBox
            // 
            this.m_EscapeCharacterTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_EscapeCharacterTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_EscapeCharacterTextBox.Location = new System.Drawing.Point(10, 143);
            this.m_EscapeCharacterTextBox.MaxLength = 1;
            this.m_EscapeCharacterTextBox.Name = "m_EscapeCharacterTextBox";
            this.m_EscapeCharacterTextBox.Size = new System.Drawing.Size(56, 23);
            this.m_EscapeCharacterTextBox.TabIndex = 15;
            this.m_EscapeCharacterTextBox.Text = "\\";
            this.m_EscapeCharacterTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.m_EscapeCharacterTextBox.TextChanged += new System.EventHandler(this.m_EscapeCharacterTextBox_TextChanged);
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(68, 147);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(119, 14);
            this.label9.TabIndex = 14;
            this.label9.Text = "Escape Character";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Font = new System.Drawing.Font("Segoe UI Semilight", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label8.Location = new System.Drawing.Point(199, 92);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(252, 15);
            this.label8.TabIndex = 13;
            this.label8.Text = "(this character must be a punctuation character)";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Segoe UI Semilight", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(186, 119);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(574, 15);
            this.label7.TabIndex = 12;
            this.label7.Text = "(character used to quote strings so that string may contain parsing characters su" +
    "ch as the value separator, etc...)";
            // 
            // m_QuoteCharacterTextBox
            // 
            this.m_QuoteCharacterTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_QuoteCharacterTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_QuoteCharacterTextBox.Location = new System.Drawing.Point(10, 116);
            this.m_QuoteCharacterTextBox.MaxLength = 1;
            this.m_QuoteCharacterTextBox.Name = "m_QuoteCharacterTextBox";
            this.m_QuoteCharacterTextBox.Size = new System.Drawing.Size(56, 23);
            this.m_QuoteCharacterTextBox.TabIndex = 11;
            this.m_QuoteCharacterTextBox.Text = "\"";
            this.m_QuoteCharacterTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.m_QuoteCharacterTextBox.TextChanged += new System.EventHandler(this.m_QuoteCharacterTextBox_TextChanged);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(68, 120);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(112, 14);
            this.label6.TabIndex = 10;
            this.label6.Text = "Quote Character";
            // 
            // m_ParseCommentLinesCheckBox
            // 
            this.m_ParseCommentLinesCheckBox.AutoSize = true;
            this.m_ParseCommentLinesCheckBox.Checked = true;
            this.m_ParseCommentLinesCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.m_ParseCommentLinesCheckBox.Location = new System.Drawing.Point(31, 66);
            this.m_ParseCommentLinesCheckBox.Name = "m_ParseCommentLinesCheckBox";
            this.m_ParseCommentLinesCheckBox.Size = new System.Drawing.Size(201, 18);
            this.m_ParseCommentLinesCheckBox.TabIndex = 9;
            this.m_ParseCommentLinesCheckBox.Text = "Parse out commented lines";
            this.m_ParseCommentLinesCheckBox.UseVisualStyleBackColor = true;
            this.m_ParseCommentLinesCheckBox.CheckedChanged += new System.EventHandler(this.m_ParseCommentLinesCheckBox_CheckedChanged);
            // 
            // m_LineCommentCharacterTextBox
            // 
            this.m_LineCommentCharacterTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_LineCommentCharacterTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_LineCommentCharacterTextBox.Location = new System.Drawing.Point(10, 89);
            this.m_LineCommentCharacterTextBox.MaxLength = 1;
            this.m_LineCommentCharacterTextBox.Name = "m_LineCommentCharacterTextBox";
            this.m_LineCommentCharacterTextBox.Size = new System.Drawing.Size(56, 23);
            this.m_LineCommentCharacterTextBox.TabIndex = 8;
            this.m_LineCommentCharacterTextBox.Text = "#";
            this.m_LineCommentCharacterTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.m_LineCommentCharacterTextBox.TextChanged += new System.EventHandler(this.m_LineCommentCharacterTextBox_TextChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(67, 93);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(126, 14);
            this.label5.TabIndex = 7;
            this.label5.Text = "Comment Character";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Segoe UI Semilight", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(238, 66);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(256, 15);
            this.label4.TabIndex = 6;
            this.label4.Text = "(commented lines will be removed automatically)";
            // 
            // m_FirstLineHeadersCheckBox
            // 
            this.m_FirstLineHeadersCheckBox.AutoSize = true;
            this.m_FirstLineHeadersCheckBox.Checked = true;
            this.m_FirstLineHeadersCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.m_FirstLineHeadersCheckBox.Location = new System.Drawing.Point(31, 19);
            this.m_FirstLineHeadersCheckBox.Name = "m_FirstLineHeadersCheckBox";
            this.m_FirstLineHeadersCheckBox.Size = new System.Drawing.Size(502, 18);
            this.m_FirstLineHeadersCheckBox.TabIndex = 4;
            this.m_FirstLineHeadersCheckBox.Text = "First line is not data, instead it contains header with column names";
            this.m_FirstLineHeadersCheckBox.UseVisualStyleBackColor = true;
            this.m_FirstLineHeadersCheckBox.CheckedChanged += new System.EventHandler(this.m_FirstLineHeadersCheckBox_CheckedChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Segoe UI Semilight", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(255, 43);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(252, 15);
            this.label3.TabIndex = 3;
            this.label3.Text = "(this character must be a punctuation character)";
            // 
            // m_ValueSeparatorCharacterTextBox
            // 
            this.m_ValueSeparatorCharacterTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ValueSeparatorCharacterTextBox.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_ValueSeparatorCharacterTextBox.Location = new System.Drawing.Point(9, 40);
            this.m_ValueSeparatorCharacterTextBox.MaxLength = 1;
            this.m_ValueSeparatorCharacterTextBox.Name = "m_ValueSeparatorCharacterTextBox";
            this.m_ValueSeparatorCharacterTextBox.Size = new System.Drawing.Size(56, 23);
            this.m_ValueSeparatorCharacterTextBox.TabIndex = 2;
            this.m_ValueSeparatorCharacterTextBox.Text = ",";
            this.m_ValueSeparatorCharacterTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.m_ValueSeparatorCharacterTextBox.TextChanged += new System.EventHandler(this.m_ValueSeparatorCharacterTextBox_TextChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(67, 44);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(182, 14);
            this.label2.TabIndex = 1;
            this.label2.Text = "Value Separator Character";
            // 
            // m_LoadSettingsFromTemplateFileDialog
            // 
            this.m_LoadSettingsFromTemplateFileDialog.Filter = "Template File|*.template";
            // 
            // m_DatasetViewPanel
            // 
            this.m_DatasetViewPanel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.m_DatasetViewPanel.Controls.Add(this.m_PreviewDataGrid);
            this.m_DatasetViewPanel.Location = new System.Drawing.Point(13, 225);
            this.m_DatasetViewPanel.Name = "m_DatasetViewPanel";
            this.m_DatasetViewPanel.Size = new System.Drawing.Size(837, 393);
            this.m_DatasetViewPanel.TabIndex = 2;
            // 
            // m_PreviewDataGrid
            // 
            this.m_PreviewDataGrid.AllowUserToAddRows = false;
            this.m_PreviewDataGrid.AllowUserToDeleteRows = false;
            this.m_PreviewDataGrid.AllowUserToResizeRows = false;
            dataGridViewCellStyle1.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle1.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            dataGridViewCellStyle1.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle1.ForeColor = System.Drawing.SystemColors.WindowText;
            dataGridViewCellStyle1.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle1.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle1.WrapMode = System.Windows.Forms.DataGridViewTriState.True;
            this.m_PreviewDataGrid.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle1;
            this.m_PreviewDataGrid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridViewCellStyle2.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle2.BackColor = System.Drawing.SystemColors.Info;
            dataGridViewCellStyle2.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle2.ForeColor = System.Drawing.SystemColors.ControlText;
            dataGridViewCellStyle2.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle2.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle2.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
            this.m_PreviewDataGrid.DefaultCellStyle = dataGridViewCellStyle2;
            this.m_PreviewDataGrid.Dock = System.Windows.Forms.DockStyle.Fill;
            this.m_PreviewDataGrid.EditMode = System.Windows.Forms.DataGridViewEditMode.EditProgrammatically;
            this.m_PreviewDataGrid.Location = new System.Drawing.Point(0, 0);
            this.m_PreviewDataGrid.MultiSelect = false;
            this.m_PreviewDataGrid.Name = "m_PreviewDataGrid";
            this.m_PreviewDataGrid.ReadOnly = true;
            dataGridViewCellStyle3.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle3.BackColor = System.Drawing.SystemColors.ActiveCaption;
            dataGridViewCellStyle3.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle3.ForeColor = System.Drawing.SystemColors.WindowText;
            dataGridViewCellStyle3.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle3.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle3.WrapMode = System.Windows.Forms.DataGridViewTriState.True;
            this.m_PreviewDataGrid.RowHeadersDefaultCellStyle = dataGridViewCellStyle3;
            this.m_PreviewDataGrid.RowHeadersWidth = 23;
            this.m_PreviewDataGrid.RowHeadersWidthSizeMode = System.Windows.Forms.DataGridViewRowHeadersWidthSizeMode.DisableResizing;
            this.m_PreviewDataGrid.Size = new System.Drawing.Size(837, 393);
            this.m_PreviewDataGrid.TabIndex = 0;
            // 
            // m_NextButton
            // 
            this.m_NextButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_NextButton.Location = new System.Drawing.Point(434, 632);
            this.m_NextButton.Name = "m_NextButton";
            this.m_NextButton.Size = new System.Drawing.Size(75, 21);
            this.m_NextButton.TabIndex = 3;
            this.m_NextButton.Text = "Next";
            this.m_NextButton.UseVisualStyleBackColor = true;
            this.m_NextButton.Click += new System.EventHandler(this.m_NextButton_Click);
            // 
            // m_BackButton
            // 
            this.m_BackButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_BackButton.Location = new System.Drawing.Point(353, 632);
            this.m_BackButton.Name = "m_BackButton";
            this.m_BackButton.Size = new System.Drawing.Size(75, 21);
            this.m_BackButton.TabIndex = 4;
            this.m_BackButton.Text = "Back";
            this.m_BackButton.UseVisualStyleBackColor = true;
            // 
            // GlobalImportPropertiesDialog
            // 
            this.AcceptButton = this.m_NextButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_BackButton;
            this.ClientSize = new System.Drawing.Size(862, 665);
            this.ControlBox = false;
            this.Controls.Add(this.m_BackButton);
            this.Controls.Add(this.m_NextButton);
            this.Controls.Add(this.m_DatasetViewPanel);
            this.Controls.Add(this.m_SettingsGroupBox);
            this.Controls.Add(this.label1);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "GlobalImportPropertiesDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Table Packager for CSV Files";
            this.m_SettingsGroupBox.ResumeLayout(false);
            this.m_SettingsGroupBox.PerformLayout();
            this.m_DatasetViewPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.m_PreviewDataGrid)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.GroupBox m_SettingsGroupBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox m_ValueSeparatorCharacterTextBox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.OpenFileDialog m_LoadSettingsFromTemplateFileDialog;
        private System.Windows.Forms.CheckBox m_FirstLineHeadersCheckBox;
        private System.Windows.Forms.Panel m_DatasetViewPanel;
        private System.Windows.Forms.DataGridView m_PreviewDataGrid;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox m_LineCommentCharacterTextBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.CheckBox m_ParseCommentLinesCheckBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox m_QuoteCharacterTextBox;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.TextBox m_EscapeCharacterTextBox;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Button m_NextButton;
        private System.Windows.Forms.Button m_BackButton;
    }
}