namespace SailTablePackagerForCsv
{
    partial class TableEditDialog
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
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle1 = new System.Windows.Forms.DataGridViewCellStyle();
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle2 = new System.Windows.Forms.DataGridViewCellStyle();
            System.Windows.Forms.DataGridViewCellStyle dataGridViewCellStyle3 = new System.Windows.Forms.DataGridViewCellStyle();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(TableEditDialog));
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.m_TableDataGridPanel = new System.Windows.Forms.Panel();
            this.m_TableDataGrid = new System.Windows.Forms.DataGridView();
            this.m_TableIdentifierTextBox = new System.Windows.Forms.TextBox();
            this.m_TableTitleTextBox = new System.Windows.Forms.TextBox();
            this.m_TableDescriptionTextBox = new System.Windows.Forms.TextBox();
            this.m_TableTagsTextBox = new System.Windows.Forms.TextBox();
            this.m_TableCsvSourceFileTextBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.m_SelectedColumnSettingsGroupBox = new System.Windows.Forms.GroupBox();
            this.label7 = new System.Windows.Forms.Label();
            this.m_SelectedColumnDynamicPropertiesListBox = new System.Windows.Forms.ListBox();
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.m_AddPropertyToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_DeletePropertyToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_EditPropertyToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.m_NextButton = new System.Windows.Forms.Button();
            this.m_BackButton = new System.Windows.Forms.Button();
            this.m_TableDataGridPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.m_TableDataGrid)).BeginInit();
            this.m_SelectedColumnSettingsGroupBox.SuspendLayout();
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(18, 14);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(77, 14);
            this.label1.TabIndex = 0;
            this.label1.Text = "Identifier";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(52, 70);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(42, 14);
            this.label2.TabIndex = 1;
            this.label2.Text = "Title";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(11, 113);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(84, 14);
            this.label3.TabIndex = 2;
            this.label3.Text = "Description";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(59, 157);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(35, 14);
            this.label4.TabIndex = 3;
            this.label4.Text = "Tags";
            // 
            // m_TableDataGridPanel
            // 
            this.m_TableDataGridPanel.Controls.Add(this.m_TableDataGrid);
            this.m_TableDataGridPanel.Location = new System.Drawing.Point(12, 209);
            this.m_TableDataGridPanel.Name = "m_TableDataGridPanel";
            this.m_TableDataGridPanel.Size = new System.Drawing.Size(1195, 295);
            this.m_TableDataGridPanel.TabIndex = 4;
            // 
            // m_TableDataGrid
            // 
            this.m_TableDataGrid.AllowUserToAddRows = false;
            this.m_TableDataGrid.AllowUserToDeleteRows = false;
            this.m_TableDataGrid.AllowUserToResizeRows = false;
            dataGridViewCellStyle1.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle1.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            dataGridViewCellStyle1.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle1.ForeColor = System.Drawing.SystemColors.WindowText;
            dataGridViewCellStyle1.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle1.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle1.WrapMode = System.Windows.Forms.DataGridViewTriState.True;
            this.m_TableDataGrid.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle1;
            this.m_TableDataGrid.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            dataGridViewCellStyle2.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle2.BackColor = System.Drawing.SystemColors.Info;
            dataGridViewCellStyle2.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle2.ForeColor = System.Drawing.SystemColors.ControlText;
            dataGridViewCellStyle2.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle2.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle2.WrapMode = System.Windows.Forms.DataGridViewTriState.False;
            this.m_TableDataGrid.DefaultCellStyle = dataGridViewCellStyle2;
            this.m_TableDataGrid.Dock = System.Windows.Forms.DockStyle.Fill;
            this.m_TableDataGrid.EditMode = System.Windows.Forms.DataGridViewEditMode.EditProgrammatically;
            this.m_TableDataGrid.Location = new System.Drawing.Point(0, 0);
            this.m_TableDataGrid.MultiSelect = false;
            this.m_TableDataGrid.Name = "m_TableDataGrid";
            this.m_TableDataGrid.ReadOnly = true;
            dataGridViewCellStyle3.Alignment = System.Windows.Forms.DataGridViewContentAlignment.MiddleLeft;
            dataGridViewCellStyle3.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            dataGridViewCellStyle3.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            dataGridViewCellStyle3.ForeColor = System.Drawing.SystemColors.WindowText;
            dataGridViewCellStyle3.SelectionBackColor = System.Drawing.SystemColors.Highlight;
            dataGridViewCellStyle3.SelectionForeColor = System.Drawing.SystemColors.HighlightText;
            dataGridViewCellStyle3.WrapMode = System.Windows.Forms.DataGridViewTriState.True;
            this.m_TableDataGrid.RowHeadersDefaultCellStyle = dataGridViewCellStyle3;
            this.m_TableDataGrid.RowHeadersWidth = 23;
            this.m_TableDataGrid.RowHeadersWidthSizeMode = System.Windows.Forms.DataGridViewRowHeadersWidthSizeMode.DisableResizing;
            this.m_TableDataGrid.Size = new System.Drawing.Size(1195, 295);
            this.m_TableDataGrid.TabIndex = 0;
            this.m_TableDataGrid.SelectionChanged += new System.EventHandler(this.m_TableDataGrid_SelectionChanged);
            // 
            // m_TableIdentifierTextBox
            // 
            this.m_TableIdentifierTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TableIdentifierTextBox.CharacterCasing = System.Windows.Forms.CharacterCasing.Lower;
            this.m_TableIdentifierTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TableIdentifierTextBox.Location = new System.Drawing.Point(97, 10);
            this.m_TableIdentifierTextBox.MaxLength = 32;
            this.m_TableIdentifierTextBox.Name = "m_TableIdentifierTextBox";
            this.m_TableIdentifierTextBox.ReadOnly = true;
            this.m_TableIdentifierTextBox.Size = new System.Drawing.Size(395, 22);
            this.m_TableIdentifierTextBox.TabIndex = 5;
            this.m_TableIdentifierTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // m_TableTitleTextBox
            // 
            this.m_TableTitleTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TableTitleTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TableTitleTextBox.Location = new System.Drawing.Point(97, 66);
            this.m_TableTitleTextBox.Name = "m_TableTitleTextBox";
            this.m_TableTitleTextBox.Size = new System.Drawing.Size(1110, 22);
            this.m_TableTitleTextBox.TabIndex = 6;
            // 
            // m_TableDescriptionTextBox
            // 
            this.m_TableDescriptionTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TableDescriptionTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TableDescriptionTextBox.Location = new System.Drawing.Point(97, 94);
            this.m_TableDescriptionTextBox.Multiline = true;
            this.m_TableDescriptionTextBox.Name = "m_TableDescriptionTextBox";
            this.m_TableDescriptionTextBox.Size = new System.Drawing.Size(1110, 53);
            this.m_TableDescriptionTextBox.TabIndex = 7;
            // 
            // m_TableTagsTextBox
            // 
            this.m_TableTagsTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TableTagsTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TableTagsTextBox.Location = new System.Drawing.Point(97, 153);
            this.m_TableTagsTextBox.Name = "m_TableTagsTextBox";
            this.m_TableTagsTextBox.Size = new System.Drawing.Size(1110, 22);
            this.m_TableTagsTextBox.TabIndex = 8;
            // 
            // m_TableCsvSourceFileTextBox
            // 
            this.m_TableCsvSourceFileTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TableCsvSourceFileTextBox.CharacterCasing = System.Windows.Forms.CharacterCasing.Lower;
            this.m_TableCsvSourceFileTextBox.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.m_TableCsvSourceFileTextBox.Location = new System.Drawing.Point(97, 38);
            this.m_TableCsvSourceFileTextBox.MaxLength = 32;
            this.m_TableCsvSourceFileTextBox.Name = "m_TableCsvSourceFileTextBox";
            this.m_TableCsvSourceFileTextBox.ReadOnly = true;
            this.m_TableCsvSourceFileTextBox.Size = new System.Drawing.Size(1110, 22);
            this.m_TableCsvSourceFileTextBox.TabIndex = 9;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 42);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(84, 14);
            this.label5.TabIndex = 10;
            this.label5.Text = "Source File";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(13, 192);
            this.label6.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(595, 14);
            this.label6.TabIndex = 11;
            this.label6.Text = "Select individual columns within the table below and edit the column settings bel" +
    "ow.";
            // 
            // m_SelectedColumnSettingsGroupBox
            // 
            this.m_SelectedColumnSettingsGroupBox.Controls.Add(this.label7);
            this.m_SelectedColumnSettingsGroupBox.Controls.Add(this.m_SelectedColumnDynamicPropertiesListBox);
            this.m_SelectedColumnSettingsGroupBox.Location = new System.Drawing.Point(12, 511);
            this.m_SelectedColumnSettingsGroupBox.Name = "m_SelectedColumnSettingsGroupBox";
            this.m_SelectedColumnSettingsGroupBox.Size = new System.Drawing.Size(1195, 211);
            this.m_SelectedColumnSettingsGroupBox.TabIndex = 13;
            this.m_SelectedColumnSettingsGroupBox.TabStop = false;
            this.m_SelectedColumnSettingsGroupBox.Text = "Selected Column Settings";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(16, 63);
            this.label7.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(238, 98);
            this.label7.TabIndex = 16;
            this.label7.Text = "Use the list to the right to edit\r\ncolumn settings. Double click\r\non existing ite" +
    "ms to modify\r\nthe setting. Right click to open\r\nup the context menu which\r\nallow" +
    "s you to add/remove\r\nsettings.";
            this.label7.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // m_SelectedColumnDynamicPropertiesListBox
            // 
            this.m_SelectedColumnDynamicPropertiesListBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_SelectedColumnDynamicPropertiesListBox.ContextMenuStrip = this.m_SelectedColumnPropertiesListBoxContextMenuStrip;
            this.m_SelectedColumnDynamicPropertiesListBox.FormattingEnabled = true;
            this.m_SelectedColumnDynamicPropertiesListBox.IntegralHeight = false;
            this.m_SelectedColumnDynamicPropertiesListBox.ItemHeight = 14;
            this.m_SelectedColumnDynamicPropertiesListBox.Location = new System.Drawing.Point(270, 21);
            this.m_SelectedColumnDynamicPropertiesListBox.Name = "m_SelectedColumnDynamicPropertiesListBox";
            this.m_SelectedColumnDynamicPropertiesListBox.ScrollAlwaysVisible = true;
            this.m_SelectedColumnDynamicPropertiesListBox.Size = new System.Drawing.Size(911, 177);
            this.m_SelectedColumnDynamicPropertiesListBox.Sorted = true;
            this.m_SelectedColumnDynamicPropertiesListBox.TabIndex = 18;
            this.m_SelectedColumnDynamicPropertiesListBox.SelectedIndexChanged += new System.EventHandler(this.m_SelectedColumnDynamicPropertiesListBox_SelectedIndexChanged);
            this.m_SelectedColumnDynamicPropertiesListBox.DoubleClick += new System.EventHandler(this.m_SelectedColumnDynamicPropertiesListBox_DoubleClick);
            // 
            // m_SelectedColumnPropertiesListBoxContextMenuStrip
            // 
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.m_AddPropertyToolStripMenuItem,
            this.m_DeletePropertyToolStripMenuItem,
            this.m_EditPropertyToolStripMenuItem});
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip.Name = "m_SelectedColumnPropertiesListBoxContextMenuStrip";
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip.Size = new System.Drawing.Size(156, 70);
            // 
            // m_AddPropertyToolStripMenuItem
            // 
            this.m_AddPropertyToolStripMenuItem.Name = "m_AddPropertyToolStripMenuItem";
            this.m_AddPropertyToolStripMenuItem.Size = new System.Drawing.Size(155, 22);
            this.m_AddPropertyToolStripMenuItem.Text = "Add property";
            this.m_AddPropertyToolStripMenuItem.Click += new System.EventHandler(this.m_AddPropertyToolStripMenuItem_Click);
            // 
            // m_DeletePropertyToolStripMenuItem
            // 
            this.m_DeletePropertyToolStripMenuItem.Name = "m_DeletePropertyToolStripMenuItem";
            this.m_DeletePropertyToolStripMenuItem.Size = new System.Drawing.Size(155, 22);
            this.m_DeletePropertyToolStripMenuItem.Text = "Delete Property";
            this.m_DeletePropertyToolStripMenuItem.Click += new System.EventHandler(this.m_DeletePropertyToolStripMenuItem_Click);
            // 
            // m_EditPropertyToolStripMenuItem
            // 
            this.m_EditPropertyToolStripMenuItem.Name = "m_EditPropertyToolStripMenuItem";
            this.m_EditPropertyToolStripMenuItem.Size = new System.Drawing.Size(155, 22);
            this.m_EditPropertyToolStripMenuItem.Text = "Edit Property";
            this.m_EditPropertyToolStripMenuItem.Click += new System.EventHandler(this.m_EditPropertyToolStripMenuItem_Click);
            // 
            // m_NextButton
            // 
            this.m_NextButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_NextButton.Location = new System.Drawing.Point(612, 732);
            this.m_NextButton.Name = "m_NextButton";
            this.m_NextButton.Size = new System.Drawing.Size(75, 23);
            this.m_NextButton.TabIndex = 14;
            this.m_NextButton.Text = "Next";
            this.m_NextButton.UseVisualStyleBackColor = true;
            this.m_NextButton.Click += new System.EventHandler(this.m_NextButton_Click);
            // 
            // m_BackButton
            // 
            this.m_BackButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_BackButton.Location = new System.Drawing.Point(531, 732);
            this.m_BackButton.Name = "m_BackButton";
            this.m_BackButton.Size = new System.Drawing.Size(75, 23);
            this.m_BackButton.TabIndex = 15;
            this.m_BackButton.Text = "Back";
            this.m_BackButton.UseVisualStyleBackColor = true;
            // 
            // TableEditDialog
            // 
            this.AcceptButton = this.m_NextButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_BackButton;
            this.ClientSize = new System.Drawing.Size(1219, 763);
            this.Controls.Add(this.m_BackButton);
            this.Controls.Add(this.m_NextButton);
            this.Controls.Add(this.m_SelectedColumnSettingsGroupBox);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.m_TableCsvSourceFileTextBox);
            this.Controls.Add(this.m_TableTagsTextBox);
            this.Controls.Add(this.m_TableDescriptionTextBox);
            this.Controls.Add(this.m_TableTitleTextBox);
            this.Controls.Add(this.m_TableIdentifierTextBox);
            this.Controls.Add(this.m_TableDataGridPanel);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "TableEditDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Table Packager for CSV Files";
            this.m_TableDataGridPanel.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.m_TableDataGrid)).EndInit();
            this.m_SelectedColumnSettingsGroupBox.ResumeLayout(false);
            this.m_SelectedColumnSettingsGroupBox.PerformLayout();
            this.m_SelectedColumnPropertiesListBoxContextMenuStrip.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Panel m_TableDataGridPanel;
        private System.Windows.Forms.DataGridView m_TableDataGrid;
        private System.Windows.Forms.TextBox m_TableIdentifierTextBox;
        private System.Windows.Forms.TextBox m_TableTitleTextBox;
        private System.Windows.Forms.TextBox m_TableDescriptionTextBox;
        private System.Windows.Forms.TextBox m_TableTagsTextBox;
        private System.Windows.Forms.TextBox m_TableCsvSourceFileTextBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.GroupBox m_SelectedColumnSettingsGroupBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.ListBox m_SelectedColumnDynamicPropertiesListBox;
        private System.Windows.Forms.Button m_NextButton;
        private System.Windows.Forms.Button m_BackButton;
        private System.Windows.Forms.ContextMenuStrip m_SelectedColumnPropertiesListBoxContextMenuStrip;
        private System.Windows.Forms.ToolStripMenuItem m_AddPropertyToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_DeletePropertyToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem m_EditPropertyToolStripMenuItem;
    }
}