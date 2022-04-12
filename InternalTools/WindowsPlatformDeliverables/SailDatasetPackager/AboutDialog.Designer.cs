namespace SailDatasetPackager
{
    partial class AboutDialog
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(AboutDialog));
            this.m_SailLogoPictureBox = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.m_OkButton = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.m_SailLogoPictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // m_SailLogoPictureBox
            // 
            this.m_SailLogoPictureBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.m_SailLogoPictureBox.Image = ((System.Drawing.Image)(resources.GetObject("m_SailLogoPictureBox.Image")));
            this.m_SailLogoPictureBox.Location = new System.Drawing.Point(10, 11);
            this.m_SailLogoPictureBox.Margin = new System.Windows.Forms.Padding(1, 2, 1, 2);
            this.m_SailLogoPictureBox.Name = "m_SailLogoPictureBox";
            this.m_SailLogoPictureBox.Size = new System.Drawing.Size(120, 120);
            this.m_SailLogoPictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.m_SailLogoPictureBox.TabIndex = 10;
            this.m_SailLogoPictureBox.TabStop = false;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Consolas", 9F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Italic))), System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(134, 39);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(420, 56);
            this.label1.TabIndex = 11;
            this.label1.Text = "SAIL Dataset Packager Tool\r\nVersion 0.1.0\r\nDecember 9th, 2021\r\nCopyright (C) 2021" +
    " Secure AI Labs, Inc. All Rights Reserved";
            // 
            // m_OkButton
            // 
            this.m_OkButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_OkButton.Location = new System.Drawing.Point(251, 108);
            this.m_OkButton.Name = "m_OkButton";
            this.m_OkButton.Size = new System.Drawing.Size(75, 23);
            this.m_OkButton.TabIndex = 12;
            this.m_OkButton.Text = "OK";
            this.m_OkButton.UseVisualStyleBackColor = true;
            // 
            // AboutDialog
            // 
            this.AcceptButton = this.m_OkButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.GradientActiveCaption;
            this.ClientSize = new System.Drawing.Size(574, 143);
            this.Controls.Add(this.m_OkButton);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.m_SailLogoPictureBox);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "AboutDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "About";
            ((System.ComponentModel.ISupportInitialize)(this.m_SailLogoPictureBox)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox m_SailLogoPictureBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button m_OkButton;
    }
}