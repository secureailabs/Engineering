namespace SailTablePackagerForCsv
{
    partial class EditColumnBooleanPropertyDialog
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
            this.m_TrueRadioButton = new System.Windows.Forms.RadioButton();
            this.m_FalseRadioButton = new System.Windows.Forms.RadioButton();
            this.m_CancelButton = new System.Windows.Forms.Button();
            this.m_OkButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // m_TrueRadioButton
            // 
            this.m_TrueRadioButton.AutoSize = true;
            this.m_TrueRadioButton.Location = new System.Drawing.Point(126, 24);
            this.m_TrueRadioButton.Name = "m_TrueRadioButton";
            this.m_TrueRadioButton.Size = new System.Drawing.Size(53, 18);
            this.m_TrueRadioButton.TabIndex = 0;
            this.m_TrueRadioButton.TabStop = true;
            this.m_TrueRadioButton.Text = "True";
            this.m_TrueRadioButton.UseVisualStyleBackColor = true;
            // 
            // m_FalseRadioButton
            // 
            this.m_FalseRadioButton.AutoSize = true;
            this.m_FalseRadioButton.Location = new System.Drawing.Point(185, 24);
            this.m_FalseRadioButton.Name = "m_FalseRadioButton";
            this.m_FalseRadioButton.Size = new System.Drawing.Size(60, 18);
            this.m_FalseRadioButton.TabIndex = 1;
            this.m_FalseRadioButton.TabStop = true;
            this.m_FalseRadioButton.Text = "False";
            this.m_FalseRadioButton.UseVisualStyleBackColor = true;
            // 
            // m_CancelButton
            // 
            this.m_CancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_CancelButton.Location = new System.Drawing.Point(107, 62);
            this.m_CancelButton.Name = "m_CancelButton";
            this.m_CancelButton.Size = new System.Drawing.Size(75, 23);
            this.m_CancelButton.TabIndex = 3;
            this.m_CancelButton.Text = "Cancel";
            this.m_CancelButton.UseVisualStyleBackColor = true;
            // 
            // m_OkButton
            // 
            this.m_OkButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_OkButton.Location = new System.Drawing.Point(189, 62);
            this.m_OkButton.Name = "m_OkButton";
            this.m_OkButton.Size = new System.Drawing.Size(75, 23);
            this.m_OkButton.TabIndex = 4;
            this.m_OkButton.Text = "OK";
            this.m_OkButton.UseVisualStyleBackColor = true;
            // 
            // EditColumnBooleanPropertyDialog
            // 
            this.AcceptButton = this.m_OkButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_CancelButton;
            this.ClientSize = new System.Drawing.Size(370, 102);
            this.ControlBox = false;
            this.Controls.Add(this.m_OkButton);
            this.Controls.Add(this.m_CancelButton);
            this.Controls.Add(this.m_FalseRadioButton);
            this.Controls.Add(this.m_TrueRadioButton);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "EditColumnBooleanPropertyDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "EditColumnBooleanPropertyDialog";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.RadioButton m_TrueRadioButton;
        private System.Windows.Forms.RadioButton m_FalseRadioButton;
        private System.Windows.Forms.Button m_CancelButton;
        private System.Windows.Forms.Button m_OkButton;
    }
}