namespace SailTablePackagerForCsv
{
    partial class TablePackagerDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(TablePackagerDialog));
            this.label1 = new System.Windows.Forms.Label();
            this.m_ExecutionGroupBox = new System.Windows.Forms.GroupBox();
            this.m_ProgressTextBox = new System.Windows.Forms.TextBox();
            this.m_GoButton = new System.Windows.Forms.Button();
            this.m_NotificationsListBox = new System.Windows.Forms.ListBox();
            this.m_RefreshTimer = new System.Windows.Forms.Timer(this.components);
            this.m_ExitButton = new System.Windows.Forms.Button();
            this.m_SaveFileDialog = new System.Windows.Forms.SaveFileDialog();
            this.m_ExecutionGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(13, 13);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(735, 42);
            this.label1.TabIndex = 1;
            this.label1.Text = resources.GetString("label1.Text");
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // m_ExecutionGroupBox
            // 
            this.m_ExecutionGroupBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.m_ExecutionGroupBox.Controls.Add(this.m_ProgressTextBox);
            this.m_ExecutionGroupBox.Controls.Add(this.m_GoButton);
            this.m_ExecutionGroupBox.Controls.Add(this.m_NotificationsListBox);
            this.m_ExecutionGroupBox.Location = new System.Drawing.Point(12, 71);
            this.m_ExecutionGroupBox.Name = "m_ExecutionGroupBox";
            this.m_ExecutionGroupBox.Size = new System.Drawing.Size(736, 368);
            this.m_ExecutionGroupBox.TabIndex = 2;
            this.m_ExecutionGroupBox.TabStop = false;
            this.m_ExecutionGroupBox.Text = "Package and Save";
            // 
            // m_ProgressTextBox
            // 
            this.m_ProgressTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ProgressTextBox.Location = new System.Drawing.Point(6, 21);
            this.m_ProgressTextBox.Name = "m_ProgressTextBox";
            this.m_ProgressTextBox.ReadOnly = true;
            this.m_ProgressTextBox.Size = new System.Drawing.Size(350, 22);
            this.m_ProgressTextBox.TabIndex = 3;
            this.m_ProgressTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // m_GoButton
            // 
            this.m_GoButton.Location = new System.Drawing.Point(362, 20);
            this.m_GoButton.Name = "m_GoButton";
            this.m_GoButton.Size = new System.Drawing.Size(131, 23);
            this.m_GoButton.TabIndex = 2;
            this.m_GoButton.Text = "GO!";
            this.m_GoButton.UseVisualStyleBackColor = true;
            this.m_GoButton.Click += new System.EventHandler(this.m_GoButton_Click);
            // 
            // m_NotificationsListBox
            // 
            this.m_NotificationsListBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.m_NotificationsListBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_NotificationsListBox.FormattingEnabled = true;
            this.m_NotificationsListBox.IntegralHeight = false;
            this.m_NotificationsListBox.ItemHeight = 14;
            this.m_NotificationsListBox.Location = new System.Drawing.Point(6, 49);
            this.m_NotificationsListBox.Name = "m_NotificationsListBox";
            this.m_NotificationsListBox.Size = new System.Drawing.Size(724, 309);
            this.m_NotificationsListBox.TabIndex = 1;
            // 
            // m_RefreshTimer
            // 
            this.m_RefreshTimer.Interval = 17;
            this.m_RefreshTimer.Tick += new System.EventHandler(this.m_RefreshTimer_Tick);
            // 
            // m_ExitButton
            // 
            this.m_ExitButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.m_ExitButton.Location = new System.Drawing.Point(666, 446);
            this.m_ExitButton.Name = "m_ExitButton";
            this.m_ExitButton.Size = new System.Drawing.Size(75, 23);
            this.m_ExitButton.TabIndex = 3;
            this.m_ExitButton.Text = "Exit";
            this.m_ExitButton.UseVisualStyleBackColor = true;
            this.m_ExitButton.Click += new System.EventHandler(this.m_ExitButton_Click);
            // 
            // m_SaveFileDialog
            // 
            this.m_SaveFileDialog.Filter = "Packaged Table|*.sailtable";
            // 
            // TablePackagerDialog
            // 
            this.AcceptButton = this.m_GoButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(762, 504);
            this.Controls.Add(this.m_ExitButton);
            this.Controls.Add(this.m_ExecutionGroupBox);
            this.Controls.Add(this.label1);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.MinimumSize = new System.Drawing.Size(778, 520);
            this.Name = "TablePackagerDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Table Packager for CSV Files";
            this.m_ExecutionGroupBox.ResumeLayout(false);
            this.m_ExecutionGroupBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.GroupBox m_ExecutionGroupBox;
        private System.Windows.Forms.Button m_GoButton;
        private System.Windows.Forms.ListBox m_NotificationsListBox;
        private System.Windows.Forms.TextBox m_ProgressTextBox;
        private System.Windows.Forms.Timer m_RefreshTimer;
        private System.Windows.Forms.Button m_ExitButton;
        private System.Windows.Forms.SaveFileDialog m_SaveFileDialog;
    }
}