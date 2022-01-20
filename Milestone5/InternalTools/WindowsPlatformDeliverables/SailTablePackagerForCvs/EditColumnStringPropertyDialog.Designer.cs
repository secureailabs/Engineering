namespace SailTablePackagerForCsv
{
    partial class EditColumnStringPropertyDialog
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
            this.m_PropertyTextBox = new System.Windows.Forms.TextBox();
            this.m_CancelButton = new System.Windows.Forms.Button();
            this.m_OkButton = new System.Windows.Forms.Button();
            this.m_DescriptionLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // m_PropertyTextBox
            // 
            this.m_PropertyTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_PropertyTextBox.Location = new System.Drawing.Point(13, 32);
            this.m_PropertyTextBox.Name = "m_PropertyTextBox";
            this.m_PropertyTextBox.Size = new System.Drawing.Size(908, 22);
            this.m_PropertyTextBox.TabIndex = 0;
            // 
            // m_CancelButton
            // 
            this.m_CancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_CancelButton.Location = new System.Drawing.Point(388, 70);
            this.m_CancelButton.Name = "m_CancelButton";
            this.m_CancelButton.Size = new System.Drawing.Size(75, 23);
            this.m_CancelButton.TabIndex = 1;
            this.m_CancelButton.Text = "Cancel";
            this.m_CancelButton.UseVisualStyleBackColor = true;
            // 
            // m_OkButton
            // 
            this.m_OkButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_OkButton.Location = new System.Drawing.Point(469, 70);
            this.m_OkButton.Name = "m_OkButton";
            this.m_OkButton.Size = new System.Drawing.Size(75, 23);
            this.m_OkButton.TabIndex = 2;
            this.m_OkButton.Text = "OK";
            this.m_OkButton.UseVisualStyleBackColor = true;
            // 
            // m_DescriptionLabel
            // 
            this.m_DescriptionLabel.AutoSize = true;
            this.m_DescriptionLabel.Location = new System.Drawing.Point(13, 13);
            this.m_DescriptionLabel.Name = "m_DescriptionLabel";
            this.m_DescriptionLabel.Size = new System.Drawing.Size(147, 14);
            this.m_DescriptionLabel.TabIndex = 3;
            this.m_DescriptionLabel.Text = "Edit Column Property";
            // 
            // EditColumnStringPropertyDialog
            // 
            this.AcceptButton = this.m_OkButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_CancelButton;
            this.ClientSize = new System.Drawing.Size(933, 105);
            this.ControlBox = false;
            this.Controls.Add(this.m_DescriptionLabel);
            this.Controls.Add(this.m_OkButton);
            this.Controls.Add(this.m_CancelButton);
            this.Controls.Add(this.m_PropertyTextBox);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "EditColumnStringPropertyDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Edit Column Property";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox m_PropertyTextBox;
        private System.Windows.Forms.Button m_CancelButton;
        private System.Windows.Forms.Button m_OkButton;
        private System.Windows.Forms.Label m_DescriptionLabel;
    }
}