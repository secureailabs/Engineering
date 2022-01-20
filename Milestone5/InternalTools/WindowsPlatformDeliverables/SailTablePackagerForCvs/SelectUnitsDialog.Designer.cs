namespace SailTablePackagerForCsv
{
    partial class SelectUnitsDialog
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
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.m_ColumnOriginalNameTextBox = new System.Windows.Forms.TextBox();
            this.m_ColumnDisplayNameTextBox = new System.Windows.Forms.TextBox();
            this.m_PropertyNameTextBox = new System.Windows.Forms.TextBox();
            this.m_UnitsComboBox = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.m_TypeTextBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.m_CancelButton = new System.Windows.Forms.Button();
            this.m_OkButton = new System.Windows.Forms.Button();
            this.m_CategoriesTextBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(9, 15);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(147, 14);
            this.label1.TabIndex = 0;
            this.label1.Text = "Column Original Name";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(16, 43);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(140, 14);
            this.label2.TabIndex = 1;
            this.label2.Text = "Column Display Name";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(58, 71);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(98, 14);
            this.label3.TabIndex = 2;
            this.label3.Text = "Property Name";
            // 
            // m_ColumnOriginalNameTextBox
            // 
            this.m_ColumnOriginalNameTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ColumnOriginalNameTextBox.Location = new System.Drawing.Point(162, 12);
            this.m_ColumnOriginalNameTextBox.Name = "m_ColumnOriginalNameTextBox";
            this.m_ColumnOriginalNameTextBox.ReadOnly = true;
            this.m_ColumnOriginalNameTextBox.Size = new System.Drawing.Size(337, 22);
            this.m_ColumnOriginalNameTextBox.TabIndex = 3;
            // 
            // m_ColumnDisplayNameTextBox
            // 
            this.m_ColumnDisplayNameTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_ColumnDisplayNameTextBox.Location = new System.Drawing.Point(162, 40);
            this.m_ColumnDisplayNameTextBox.Name = "m_ColumnDisplayNameTextBox";
            this.m_ColumnDisplayNameTextBox.ReadOnly = true;
            this.m_ColumnDisplayNameTextBox.Size = new System.Drawing.Size(337, 22);
            this.m_ColumnDisplayNameTextBox.TabIndex = 4;
            // 
            // m_PropertyNameTextBox
            // 
            this.m_PropertyNameTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_PropertyNameTextBox.Location = new System.Drawing.Point(162, 68);
            this.m_PropertyNameTextBox.Name = "m_PropertyNameTextBox";
            this.m_PropertyNameTextBox.ReadOnly = true;
            this.m_PropertyNameTextBox.Size = new System.Drawing.Size(337, 22);
            this.m_PropertyNameTextBox.TabIndex = 5;
            // 
            // m_UnitsComboBox
            // 
            this.m_UnitsComboBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_UnitsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.m_UnitsComboBox.FormattingEnabled = true;
            this.m_UnitsComboBox.Items.AddRange(new object[] {
            "GenericString",
            "Integer",
            "DecimalNumber",
            "Boolean",
            "Categorical",
            "Meters",
            "Millimeters",
            "Centimeters",
            "Inches",
            "Feet",
            "Celcius",
            "Farenheit"});
            this.m_UnitsComboBox.Location = new System.Drawing.Point(162, 97);
            this.m_UnitsComboBox.Name = "m_UnitsComboBox";
            this.m_UnitsComboBox.Size = new System.Drawing.Size(337, 22);
            this.m_UnitsComboBox.TabIndex = 6;
            this.m_UnitsComboBox.SelectedIndexChanged += new System.EventHandler(this.m_UnitsComboBox_SelectedIndexChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(114, 100);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(42, 14);
            this.label4.TabIndex = 7;
            this.label4.Text = "Units";
            // 
            // m_TypeTextBox
            // 
            this.m_TypeTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_TypeTextBox.Location = new System.Drawing.Point(162, 125);
            this.m_TypeTextBox.Name = "m_TypeTextBox";
            this.m_TypeTextBox.ReadOnly = true;
            this.m_TypeTextBox.Size = new System.Drawing.Size(337, 22);
            this.m_TypeTextBox.TabIndex = 8;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(121, 128);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(35, 14);
            this.label5.TabIndex = 9;
            this.label5.Text = "Type";
            // 
            // m_CancelButton
            // 
            this.m_CancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.m_CancelButton.Location = new System.Drawing.Point(184, 194);
            this.m_CancelButton.Name = "m_CancelButton";
            this.m_CancelButton.Size = new System.Drawing.Size(75, 23);
            this.m_CancelButton.TabIndex = 17;
            this.m_CancelButton.Text = "Cancel";
            this.m_CancelButton.UseVisualStyleBackColor = true;
            // 
            // m_OkButton
            // 
            this.m_OkButton.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.m_OkButton.Location = new System.Drawing.Point(265, 194);
            this.m_OkButton.Name = "m_OkButton";
            this.m_OkButton.Size = new System.Drawing.Size(75, 23);
            this.m_OkButton.TabIndex = 16;
            this.m_OkButton.Text = "OK";
            this.m_OkButton.UseVisualStyleBackColor = true;
            this.m_OkButton.Click += new System.EventHandler(this.m_OkButton_Click);
            // 
            // m_CategoriesTextBox
            // 
            this.m_CategoriesTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.m_CategoriesTextBox.Location = new System.Drawing.Point(162, 153);
            this.m_CategoriesTextBox.Name = "m_CategoriesTextBox";
            this.m_CategoriesTextBox.Size = new System.Drawing.Size(337, 22);
            this.m_CategoriesTextBox.TabIndex = 18;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(79, 156);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(77, 14);
            this.label6.TabIndex = 19;
            this.label6.Text = "Categories";
            // 
            // SelectUnitsDialog
            // 
            this.AcceptButton = this.m_OkButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.m_CancelButton;
            this.ClientSize = new System.Drawing.Size(524, 232);
            this.ControlBox = false;
            this.Controls.Add(this.label6);
            this.Controls.Add(this.m_CategoriesTextBox);
            this.Controls.Add(this.m_CancelButton);
            this.Controls.Add(this.m_OkButton);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.m_TypeTextBox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.m_UnitsComboBox);
            this.Controls.Add(this.m_PropertyNameTextBox);
            this.Controls.Add(this.m_ColumnDisplayNameTextBox);
            this.Controls.Add(this.m_ColumnOriginalNameTextBox);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Font = new System.Drawing.Font("Consolas", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Margin = new System.Windows.Forms.Padding(4, 3, 4, 3);
            this.Name = "SelectUnitsDialog";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Select Units To Assign to the Current Column";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox m_ColumnOriginalNameTextBox;
        private System.Windows.Forms.TextBox m_ColumnDisplayNameTextBox;
        private System.Windows.Forms.TextBox m_PropertyNameTextBox;
        private System.Windows.Forms.ComboBox m_UnitsComboBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox m_TypeTextBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button m_CancelButton;
        private System.Windows.Forms.Button m_OkButton;
        private System.Windows.Forms.TextBox m_CategoriesTextBox;
        private System.Windows.Forms.Label label6;
    }
}