namespace SailDatasetPackager
{
    partial class StructuredBufferTestDialog
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
            this.m_SourceJsonStringTextBox = new System.Windows.Forms.TextBox();
            this.m_ResultingStructureBufferTextBox = new System.Windows.Forms.TextBox();
            this.m_ConvertStandardButton = new System.Windows.Forms.Button();
            this.m_DoneButton = new System.Windows.Forms.Button();
            this.m_ReconvertedStructureBufferTextBox = new System.Windows.Forms.TextBox();
            this.m_ConvertTypedButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // m_SourceJsonStringTextBox
            // 
            this.m_SourceJsonStringTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_SourceJsonStringTextBox.Location = new System.Drawing.Point(13, 13);
            this.m_SourceJsonStringTextBox.MaxLength = 999999;
            this.m_SourceJsonStringTextBox.Multiline = true;
            this.m_SourceJsonStringTextBox.Name = "m_SourceJsonStringTextBox";
            this.m_SourceJsonStringTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.m_SourceJsonStringTextBox.Size = new System.Drawing.Size(775, 249);
            this.m_SourceJsonStringTextBox.TabIndex = 0;
            // 
            // m_ResultingStructureBufferTextBox
            // 
            this.m_ResultingStructureBufferTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ResultingStructureBufferTextBox.Location = new System.Drawing.Point(13, 297);
            this.m_ResultingStructureBufferTextBox.MaxLength = 999999;
            this.m_ResultingStructureBufferTextBox.Multiline = true;
            this.m_ResultingStructureBufferTextBox.Name = "m_ResultingStructureBufferTextBox";
            this.m_ResultingStructureBufferTextBox.ReadOnly = true;
            this.m_ResultingStructureBufferTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.m_ResultingStructureBufferTextBox.Size = new System.Drawing.Size(775, 249);
            this.m_ResultingStructureBufferTextBox.TabIndex = 1;
            // 
            // m_ConvertStandardButton
            // 
            this.m_ConvertStandardButton.Location = new System.Drawing.Point(260, 268);
            this.m_ConvertStandardButton.Name = "m_ConvertStandardButton";
            this.m_ConvertStandardButton.Size = new System.Drawing.Size(137, 23);
            this.m_ConvertStandardButton.TabIndex = 2;
            this.m_ConvertStandardButton.Text = "Convert Standard";
            this.m_ConvertStandardButton.UseVisualStyleBackColor = true;
            this.m_ConvertStandardButton.Click += new System.EventHandler(this.m_ConvertButton_Click);
            // 
            // m_DoneButton
            // 
            this.m_DoneButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_DoneButton.Location = new System.Drawing.Point(363, 807);
            this.m_DoneButton.Name = "m_DoneButton";
            this.m_DoneButton.Size = new System.Drawing.Size(75, 23);
            this.m_DoneButton.TabIndex = 3;
            this.m_DoneButton.Text = "Done";
            this.m_DoneButton.UseVisualStyleBackColor = true;
            this.m_DoneButton.Click += new System.EventHandler(this.m_DoneButton_Click);
            // 
            // m_ReconvertedStructureBufferTextBox
            // 
            this.m_ReconvertedStructureBufferTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ReconvertedStructureBufferTextBox.Location = new System.Drawing.Point(13, 552);
            this.m_ReconvertedStructureBufferTextBox.MaxLength = 999999;
            this.m_ReconvertedStructureBufferTextBox.Multiline = true;
            this.m_ReconvertedStructureBufferTextBox.Name = "m_ReconvertedStructureBufferTextBox";
            this.m_ReconvertedStructureBufferTextBox.ReadOnly = true;
            this.m_ReconvertedStructureBufferTextBox.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.m_ReconvertedStructureBufferTextBox.Size = new System.Drawing.Size(775, 249);
            this.m_ReconvertedStructureBufferTextBox.TabIndex = 4;
            // 
            // m_ConvertTypedButton
            // 
            this.m_ConvertTypedButton.Location = new System.Drawing.Point(403, 268);
            this.m_ConvertTypedButton.Name = "m_ConvertTypedButton";
            this.m_ConvertTypedButton.Size = new System.Drawing.Size(137, 23);
            this.m_ConvertTypedButton.TabIndex = 5;
            this.m_ConvertTypedButton.Text = "Convert Typed";
            this.m_ConvertTypedButton.UseVisualStyleBackColor = true;
            this.m_ConvertTypedButton.Click += new System.EventHandler(this.m_ConvertTypedButton_Click);
            // 
            // StructuredBufferTestDialog
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_DoneButton;
            this.ClientSize = new System.Drawing.Size(800, 837);
            this.ControlBox = false;
            this.Controls.Add(this.m_ConvertTypedButton);
            this.Controls.Add(this.m_ReconvertedStructureBufferTextBox);
            this.Controls.Add(this.m_DoneButton);
            this.Controls.Add(this.m_ConvertStandardButton);
            this.Controls.Add(this.m_ResultingStructureBufferTextBox);
            this.Controls.Add(this.m_SourceJsonStringTextBox);
            this.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Name = "StructuredBufferTestDialog";
            this.Text = "StructuredBufferTestDialog";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox m_SourceJsonStringTextBox;
        private System.Windows.Forms.TextBox m_ResultingStructureBufferTextBox;
        private System.Windows.Forms.Button m_ConvertStandardButton;
        private System.Windows.Forms.Button m_DoneButton;
        private System.Windows.Forms.TextBox m_ReconvertedStructureBufferTextBox;
        private System.Windows.Forms.Button m_ConvertTypedButton;
    }
}