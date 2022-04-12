namespace SailDatasetPackager
{
    partial class DatasetPackagerDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(DatasetPackagerDialog));
            this.m_NotificationsListBox = new System.Windows.Forms.ListBox();
            this.m_DoneButton = new System.Windows.Forms.Button();
            this.m_RefreshTimer = new System.Windows.Forms.Timer(this.components);
            this.SuspendLayout();
            // 
            // m_NotificationsListBox
            // 
            this.m_NotificationsListBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_NotificationsListBox.FormattingEnabled = true;
            this.m_NotificationsListBox.HorizontalScrollbar = true;
            this.m_NotificationsListBox.ItemHeight = 14;
            this.m_NotificationsListBox.Location = new System.Drawing.Point(15, 14);
            this.m_NotificationsListBox.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.m_NotificationsListBox.Name = "m_NotificationsListBox";
            this.m_NotificationsListBox.Size = new System.Drawing.Size(903, 410);
            this.m_NotificationsListBox.TabIndex = 0;
            // 
            // m_DoneButton
            // 
            this.m_DoneButton.Location = new System.Drawing.Point(424, 432);
            this.m_DoneButton.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.m_DoneButton.Name = "m_DoneButton";
            this.m_DoneButton.Size = new System.Drawing.Size(88, 25);
            this.m_DoneButton.TabIndex = 1;
            this.m_DoneButton.Text = "Done";
            this.m_DoneButton.UseVisualStyleBackColor = true;
            this.m_DoneButton.Click += new System.EventHandler(this.m_DoneButton_Click);
            // 
            // m_RefreshTimer
            // 
            this.m_RefreshTimer.Enabled = true;
            this.m_RefreshTimer.Interval = 16;
            this.m_RefreshTimer.Tick += new System.EventHandler(this.m_RefreshTimer_Tick);
            // 
            // DatasetPackagerDialog
            // 
            this.AcceptButton = this.m_DoneButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(933, 465);
            this.Controls.Add(this.m_DoneButton);
            this.Controls.Add(this.m_NotificationsListBox);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "DatasetPackagerDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "SAIL Dataset Packager";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ListBox m_NotificationsListBox;
        private System.Windows.Forms.Button m_DoneButton;
        private System.Windows.Forms.Timer m_RefreshTimer;
    }
}