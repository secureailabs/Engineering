﻿using System;
using System.IO;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace DataSetSpecification
{
    public partial class TableInfo : UserControl
    {
        public Guid m_tableUUID;
        public string m_tableName = "";
        public string m_tableDescription = "";
        public string m_tableTags = "";
        public uint m_numberOfColumns = 0;
        public uint m_numberOfRows = 0;
        public string m_columnNames = "";
        public string m_columnTypes = "";
        public Byte m_tablePrivacy = 0;

        // To store the Visibility state of the 3 Add Header Button status
        // 0 : Add/Edit Header Button
        // 1 : Done and Revert Button
        private UInt16 m_addHeaderButtonVisibility = 00;
        private UInt16 m_editHeaderButtonVisibility = 00;
 
        private DataRow headerRow;
        public TableInfo()
        {
            InitializeComponent();
        }

        public StructuredBuffer GetTableStructuredBuffer()
        {
            StructuredBuffer oStructuredBuffer = new StructuredBuffer();
            oStructuredBuffer.PutGuid("Guid", m_tableUUID);
            oStructuredBuffer.PutByte("Type", 0);
            oStructuredBuffer.PutString("Name", m_tableName);
            oStructuredBuffer.PutString("Description", m_tableDescription);
            oStructuredBuffer.PutString("Keywords", m_tableTags);
            oStructuredBuffer.PutUnsignedInt32("Coulumns", m_numberOfColumns);
            oStructuredBuffer.PutUnsignedInt64("Rows", m_numberOfRows);
            oStructuredBuffer.PutByte("Privacy", m_tablePrivacy);
            
            StructuredBuffer oColumnMetadata = new StructuredBuffer();
            int ColumnId = 0;
            foreach (UserControlTableColumn cc in FlowPanelColumnInfo.Controls)
            {
                StructuredBuffer oThisColumnMetaData = cc.GetColumnStructuredBuffer();
                oColumnMetadata.PutStructuredBuffer("Column"+ColumnId, oThisColumnMetaData);
                ColumnId += 1;
            }
            oStructuredBuffer.PutStructuredBuffer("ColumnMetadata", oColumnMetadata);
            return oStructuredBuffer;
        }

        public string GetTableAsCSVString()
        {
            DataTable dataTable = (DataTable)dataGridView1.DataSource;
            StringBuilder sb = new StringBuilder();
            foreach (DataRow row in dataTable.Rows)
            {
                IEnumerable<string> fields = row.ItemArray.Select(field => field.ToString());
                sb.AppendLine(string.Join(",", fields));
            }
            return sb.ToString();
        }

        public string GetColumnType()
        {
            StringBuilder sb = new StringBuilder();
            foreach (UserControlTableColumn cc in FlowPanelColumnInfo.Controls)
            {
                sb.Append("," + cc.m_dataType);
            }
            return sb.ToString();
        }

        public string GetColumnSensitivity()
        {
            StringBuilder sb = new StringBuilder();
            foreach (UserControlTableColumn cc in FlowPanelColumnInfo.Controls)
            {
                sb.Append("," + cc.m_sensitivityLevel);
            }
            return sb.ToString();
        }

        private void UpdateColumnControl()
        {
            StringBuilder sb = new StringBuilder();
            int i = 0;
            foreach (UserControlTableColumn cc in FlowPanelColumnInfo.Controls)
            {
                DataTable dataTable = (DataTable)dataGridView1.DataSource;
                cc.label1_setvalue(dataTable.Rows[0].ItemArray[i].ToString());
                sb.Append("," + dataTable.Rows[0].ItemArray[i]);
                i++;               
            }
            m_columnNames =  sb.ToString();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog dialog = new OpenFileDialog
            {
                Filter = "CSV | *.csv",
                Multiselect = false
            };
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                textBox1.Text = dialog.FileName;
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            m_numberOfColumns = 0;
            m_numberOfRows = 0;
            FlowPanelColumnInfo.Controls.Clear();
            DataTable dataTable = new DataTable();
            string filePath = textBox1.Text;
            if (filePath != "")
            {
                FileInfo fi = new FileInfo(filePath);
                filesize.Text = fi.Length.ToString() + " bytes";
                bool first = true;
                IEnumerable<string> lines;
                try
                {
                    lines = System.IO.File.ReadLines(filePath);
                    foreach (string line in lines)
                    {
                        string[] oneLine = line.Split(',');
                        if (first)
                        {
                            foreach (string entry in oneLine)
                            {
                                dataTable.Columns.Add(m_numberOfColumns.ToString());
                                m_numberOfColumns++;
                                UserControlTableColumn cc = new UserControlTableColumn();
                                cc.Controls.Find("label1", true)[0].Text = entry;
                                FlowPanelColumnInfo.Controls.Add(cc);
                            }
                            first = false;
                        }
                        dataTable.Rows.Add(oneLine);
                        m_numberOfRows++;
                    }
                    dataGridView1.DataSource = dataTable;
                    foreach (DataGridViewRow onerow in dataGridView1.Rows)
                    {
                        onerow.ReadOnly = true;
                    }
                    rows.Text = m_numberOfRows.ToString();
                    columns.Text = m_numberOfColumns.ToString();
                    m_tableUUID = System.Guid.NewGuid();
                    ButtonAddHeader.Show();
                    ButtonEditHeader.Show();
                    m_addHeaderButtonVisibility = 10;
                    m_editHeaderButtonVisibility = 10;
                }
                catch (System.Exception)
                {
                    ;
                }
            }
        }

        private void LabelClose_Click(object sender, EventArgs e)
        {
            Label oLabelDelete = (Label)sender;
            UserControl oUserControlToDelete = (UserControl)oLabelDelete.Parent;
            FlowLayoutPanel oParentOfUserControlToDelete = (FlowLayoutPanel)oLabelDelete.Parent.Parent;
            FormMain oFlowLayoutPanelContainer = (FormMain)oParentOfUserControlToDelete.Parent;
            oFlowLayoutPanelContainer.m_nNumberOfTables -= 1;
            Panel flowLayoutPanel = (Panel)oFlowLayoutPanelContainer.Controls.Find("PanelDataSetInfo", true)[0];
            Label labelTableNumber = (Label)flowLayoutPanel.Controls.Find("numTables", true)[0];
            labelTableNumber.Text = oFlowLayoutPanelContainer.m_nNumberOfTables.ToString();
            oParentOfUserControlToDelete.Controls.Remove(oUserControlToDelete);
            oUserControlToDelete.Dispose();
        }

        private void DataSetID_Click(object sender, EventArgs e)
        {
            Label label = (Label)sender;
            UserControl UC = (UserControl)label.Parent;
            bool currentState = UC.Controls.Find("dataGridView1", true)[0].Visible;
            foreach (Control control in UC.Controls)
            {
                if (("ButtonAddHeaderDone" == control.Name) || ("ButtonAddHeaderRevert" == control.Name))
                {
                    if (false == currentState && (01 == m_addHeaderButtonVisibility))
                    {
                        control.Visible = true;
                    }
                    else
                    {
                        control.Visible = false;
                    }
                }
                else if (("ButtonEditHeaderDone" == control.Name) || ("ButtonEditHeaderRevert" == control.Name))
                {
                    if ((false == currentState) && (01 == m_editHeaderButtonVisibility))
                    {
                        control.Visible = true;
                    }
                    else
                    {
                        control.Visible = false;
                    }
                }
                else if (control.Name == "ButtonAddHeader")
                {
                    if ((false == currentState) && (10 == m_addHeaderButtonVisibility) && (01 != m_editHeaderButtonVisibility))
                    {
                        control.Visible = true;
                    }
                    else
                    {
                        control.Visible = false;
                    }
                }
                else if (control.Name == "ButtonEditHeader")
                {
                    if ((false == currentState) && (10 == m_editHeaderButtonVisibility) && (01 != m_addHeaderButtonVisibility))
                    {
                        control.Visible = true;
                    }
                    else
                    {
                        control.Visible = false;
                    }
                }
                else if (control.Name != "DataSetID" && control.Name != "LabelClose" && control.Name != "LabelMinimize")
                {
                    control.Visible = !currentState;
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            DataTable dataTable = (DataTable)dataGridView1.DataSource;
            DataRow newrow = dataTable.NewRow();
            dataTable.Rows.InsertAt(newrow, 0);
            ButtonAddHeader.Hide();
            ButtonEditHeader.Hide();
            ButtonAddHeaderRevert.Show();
            ButtonAddHeaderDone.Show();
            m_addHeaderButtonVisibility = 01;
        }

        // TODO : make datatable a private member and use it then
        private void ButtonEditHeader_Click(object sender, EventArgs e)
        {
            dataGridView1.Rows[0].ReadOnly = false;
            DataTable dataTable = (DataTable)dataGridView1.DataSource;
            headerRow = dataTable.NewRow();
            headerRow.ItemArray = dataTable.Rows[0].ItemArray.Clone() as object[];
            ButtonEditHeader.Hide();
            ButtonAddHeader.Hide();
            ButtonEditHeaderDone.Show();
            ButtonEditHeaderRevert.Show();
            m_editHeaderButtonVisibility = 01;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            dataGridView1.Rows[0].ReadOnly = true;
            ButtonEditHeader.Show();
            ButtonEditHeaderDone.Hide();
            ButtonEditHeaderRevert.Hide();
            if (00 == m_addHeaderButtonVisibility)
            {
                ButtonAddHeader.Hide();
            }
            else
            {
                ButtonAddHeader.Show();
            }
            m_editHeaderButtonVisibility = 10;
            UpdateColumnControl();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            dataGridView1.Rows[0].ReadOnly = true;
            DataTable dataTable = (DataTable)dataGridView1.DataSource;
            dataTable.Rows.Remove(dataTable.Rows[0]);
            dataTable.Rows.InsertAt(headerRow, 0);
            ButtonEditHeader.Show();
            ButtonEditHeaderDone.Hide();
            ButtonEditHeaderRevert.Hide();
            if (00 == m_addHeaderButtonVisibility)
            {
                ButtonAddHeader.Hide();
            }
            else
            {
                ButtonAddHeader.Show();
            }
            m_editHeaderButtonVisibility = 10;
        }

        private void ButtonAddHeaderDone_Click(object sender, EventArgs e)
        {
            dataGridView1.Rows[0].ReadOnly = true;
            ButtonAddHeader.Show();
            ButtonEditHeader.Show();
            ButtonAddHeaderRevert.Hide();
            ButtonAddHeaderDone.Hide();
            ButtonAddHeader.Hide();
            m_addHeaderButtonVisibility = 00;
            UpdateColumnControl();
            m_numberOfRows++;
            rows.Text = m_numberOfRows.ToString();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            DataTable dataTable = (DataTable)dataGridView1.DataSource;
            dataTable.Rows.Remove(dataTable.Rows[0]);
            ButtonAddHeader.Show();
            ButtonEditHeader.Show();
            ButtonAddHeaderRevert.Hide();
            ButtonAddHeaderDone.Hide();
            m_addHeaderButtonVisibility = 10;
        }

        private void ButtonReload_Click(object sender, EventArgs e)
        {
            textBox1_TextChanged(sender, e);
            ButtonEditHeaderDone.Hide();
            ButtonEditHeaderRevert.Hide();
            ButtonAddHeaderRevert.Hide();
            ButtonAddHeaderDone.Hide();
            ButtonAddHeader.Show();
            ButtonEditHeader.Show();
        }

        private void LabelMinimize_Click(object sender, EventArgs e)
        {
            DataSetID_Click(sender, e);
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            foreach (UserControlTableColumn cc in FlowPanelColumnInfo.Controls)
            {
                TrackBar incol = (TrackBar)cc.Controls.Find("trackBar1", true)[0];
                if (incol.Value < trackBar1.Value)
                {
                    incol.Value = trackBar1.Value;
                }
            }
            m_tablePrivacy = (Byte)trackBar1.Value;
        }

        private void textBoxTableName_TextChanged(object sender, EventArgs e)
        {
            
            m_tableName = textBoxTableName.Text;
        }

        private void TextBoxTableDescription_TextChanged(object sender, EventArgs e)
        {
            m_tableDescription = textBoxTableDescription.Text;
        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {
            m_tableTags = textBox3.Text;
        }
    }
}
