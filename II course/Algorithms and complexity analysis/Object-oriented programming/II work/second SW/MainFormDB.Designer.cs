using System.ComponentModel;
using System.Drawing;

namespace second_SW
{
    partial class MainFormDB
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private IContainer components = null;

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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainFormDB));
            this.labelFruitID = new System.Windows.Forms.Label();
            this.labelName = new System.Windows.Forms.Label();
            this.labelWeight = new System.Windows.Forms.Label();
            this.labelClassification = new System.Windows.Forms.Label();
            this.labelCountry = new System.Windows.Forms.Label();
            this.textBoxFruitID = new System.Windows.Forms.TextBox();
            this.textBoxName = new System.Windows.Forms.TextBox();
            this.textBoxWeight = new System.Windows.Forms.TextBox();
            this.textBoxCountry = new System.Windows.Forms.TextBox();
            this.comboBoxClassification = new System.Windows.Forms.ComboBox();
            this.buttonSave = new System.Windows.Forms.Button();
            this.buttonUpdate = new System.Windows.Forms.Button();
            this.buttonDelete = new System.Windows.Forms.Button();
            this.buttonShow = new System.Windows.Forms.Button();
            this.dataGridView1 = new System.Windows.Forms.DataGridView();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).BeginInit();
            this.SuspendLayout();
            // 
            // labelFruitID
            // 
            this.labelFruitID.BackColor = System.Drawing.Color.Transparent;
            this.labelFruitID.Font = new System.Drawing.Font("MV Boli", 13.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelFruitID.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelFruitID.Location = new System.Drawing.Point(53, 151);
            this.labelFruitID.Name = "labelFruitID";
            this.labelFruitID.Size = new System.Drawing.Size(149, 35);
            this.labelFruitID.TabIndex = 0;
            this.labelFruitID.Text = "Fruit ID";
            // 
            // labelName
            // 
            this.labelName.BackColor = System.Drawing.Color.Transparent;
            this.labelName.Font = new System.Drawing.Font("MV Boli", 14F, System.Drawing.FontStyle.Bold);
            this.labelName.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelName.Location = new System.Drawing.Point(53, 194);
            this.labelName.Name = "labelName";
            this.labelName.Size = new System.Drawing.Size(149, 36);
            this.labelName.TabIndex = 1;
            this.labelName.Text = "Name";
            // 
            // labelWeight
            // 
            this.labelWeight.BackColor = System.Drawing.Color.Transparent;
            this.labelWeight.Font = new System.Drawing.Font("MV Boli", 14F, System.Drawing.FontStyle.Bold);
            this.labelWeight.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelWeight.Location = new System.Drawing.Point(53, 242);
            this.labelWeight.Name = "labelWeight";
            this.labelWeight.Size = new System.Drawing.Size(203, 39);
            this.labelWeight.TabIndex = 2;
            this.labelWeight.Text = "Weight (kg)";
            // 
            // labelClassification
            // 
            this.labelClassification.BackColor = System.Drawing.Color.Transparent;
            this.labelClassification.Font = new System.Drawing.Font("MV Boli", 14F, System.Drawing.FontStyle.Bold);
            this.labelClassification.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelClassification.Location = new System.Drawing.Point(53, 293);
            this.labelClassification.Name = "labelClassification";
            this.labelClassification.Size = new System.Drawing.Size(222, 33);
            this.labelClassification.TabIndex = 3;
            this.labelClassification.Text = "Classification";
            // 
            // labelCountry
            // 
            this.labelCountry.BackColor = System.Drawing.Color.Transparent;
            this.labelCountry.Font = new System.Drawing.Font("MV Boli", 14F, System.Drawing.FontStyle.Bold);
            this.labelCountry.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelCountry.Location = new System.Drawing.Point(53, 337);
            this.labelCountry.Name = "labelCountry";
            this.labelCountry.Size = new System.Drawing.Size(148, 37);
            this.labelCountry.TabIndex = 4;
            this.labelCountry.Text = "Country";
            // 
            // textBoxFruitID
            // 
            this.textBoxFruitID.Location = new System.Drawing.Point(243, 158);
            this.textBoxFruitID.Name = "textBoxFruitID";
            this.textBoxFruitID.Size = new System.Drawing.Size(157, 22);
            this.textBoxFruitID.TabIndex = 5;
            // 
            // textBoxName
            // 
            this.textBoxName.Location = new System.Drawing.Point(243, 201);
            this.textBoxName.Name = "textBoxName";
            this.textBoxName.Size = new System.Drawing.Size(157, 22);
            this.textBoxName.TabIndex = 6;
            // 
            // textBoxWeight
            // 
            this.textBoxWeight.Location = new System.Drawing.Point(243, 249);
            this.textBoxWeight.Name = "textBoxWeight";
            this.textBoxWeight.Size = new System.Drawing.Size(157, 22);
            this.textBoxWeight.TabIndex = 7;
            // 
            // textBoxCountry
            // 
            this.textBoxCountry.Location = new System.Drawing.Point(243, 344);
            this.textBoxCountry.Name = "textBoxCountry";
            this.textBoxCountry.Size = new System.Drawing.Size(157, 22);
            this.textBoxCountry.TabIndex = 8;
            // 
            // comboBoxClassification
            // 
            this.comboBoxClassification.FormattingEnabled = true;
            this.comboBoxClassification.Items.AddRange(new object[] { "Pome fruits", "Stone fruits", "Berries", "Nut fruits", "Subtropical and Tropical" });
            this.comboBoxClassification.Location = new System.Drawing.Point(243, 300);
            this.comboBoxClassification.Name = "comboBoxClassification";
            this.comboBoxClassification.Size = new System.Drawing.Size(157, 24);
            this.comboBoxClassification.TabIndex = 9;
            // 
            // buttonSave
            // 
            this.buttonSave.BackColor = System.Drawing.SystemColors.Control;
            this.buttonSave.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("buttonSave.BackgroundImage")));
            this.buttonSave.Font = new System.Drawing.Font("MV Boli", 10.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonSave.ForeColor = System.Drawing.Color.SaddleBrown;
            this.buttonSave.Location = new System.Drawing.Point(67, 436);
            this.buttonSave.Name = "buttonSave";
            this.buttonSave.Size = new System.Drawing.Size(135, 38);
            this.buttonSave.TabIndex = 10;
            this.buttonSave.Text = "Save Data";
            this.buttonSave.UseVisualStyleBackColor = false;
            this.buttonSave.Click += new System.EventHandler(this.buttonSave_Click);
            // 
            // buttonUpdate
            // 
            this.buttonUpdate.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("buttonUpdate.BackgroundImage")));
            this.buttonUpdate.Font = new System.Drawing.Font("MV Boli", 10.2F, System.Drawing.FontStyle.Bold);
            this.buttonUpdate.ForeColor = System.Drawing.Color.SaddleBrown;
            this.buttonUpdate.Location = new System.Drawing.Point(222, 436);
            this.buttonUpdate.Name = "buttonUpdate";
            this.buttonUpdate.Size = new System.Drawing.Size(135, 38);
            this.buttonUpdate.TabIndex = 11;
            this.buttonUpdate.Text = "Update Data";
            this.buttonUpdate.UseVisualStyleBackColor = true;
            this.buttonUpdate.Click += new System.EventHandler(this.buttonUpdate_Click);
            // 
            // buttonDelete
            // 
            this.buttonDelete.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("buttonDelete.BackgroundImage")));
            this.buttonDelete.Font = new System.Drawing.Font("MV Boli", 10.2F, System.Drawing.FontStyle.Bold);
            this.buttonDelete.ForeColor = System.Drawing.Color.SaddleBrown;
            this.buttonDelete.Location = new System.Drawing.Point(67, 498);
            this.buttonDelete.Name = "buttonDelete";
            this.buttonDelete.Size = new System.Drawing.Size(135, 38);
            this.buttonDelete.TabIndex = 12;
            this.buttonDelete.Text = "Delete Data";
            this.buttonDelete.UseVisualStyleBackColor = true;
            this.buttonDelete.Click += new System.EventHandler(this.buttonDelete_Click);
            // 
            // buttonShow
            // 
            this.buttonShow.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("buttonShow.BackgroundImage")));
            this.buttonShow.Font = new System.Drawing.Font("MV Boli", 10.2F, System.Drawing.FontStyle.Bold);
            this.buttonShow.ForeColor = System.Drawing.Color.SaddleBrown;
            this.buttonShow.Location = new System.Drawing.Point(222, 498);
            this.buttonShow.Name = "buttonShow";
            this.buttonShow.Size = new System.Drawing.Size(135, 38);
            this.buttonShow.TabIndex = 13;
            this.buttonShow.Text = "Show Data";
            this.buttonShow.UseVisualStyleBackColor = true;
            this.buttonShow.Click += new System.EventHandler(this.buttonShow_Click);
            // 
            // dataGridView1
            // 
            this.dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView1.Location = new System.Drawing.Point(458, 99);
            this.dataGridView1.Name = "dataGridView1";
            this.dataGridView1.RowTemplate.Height = 24;
            this.dataGridView1.Size = new System.Drawing.Size(748, 466);
            this.dataGridView1.TabIndex = 14;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label1.Font = new System.Drawing.Font("MV Boli", 28.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.SaddleBrown;
            this.label1.Location = new System.Drawing.Point(535, 21);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(597, 61);
            this.label1.TabIndex = 15;
            this.label1.Text = "Fruit Information";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label2.Font = new System.Drawing.Font("MV Boli", 20F, System.Drawing.FontStyle.Bold);
            this.label2.ForeColor = System.Drawing.Color.SaddleBrown;
            this.label2.Location = new System.Drawing.Point(53, 26);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(347, 55);
            this.label2.TabIndex = 16;
            this.label2.Text = "Adding Section";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label3
            // 
            this.label3.BackColor = System.Drawing.Color.Transparent;
            this.label3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label3.Cursor = System.Windows.Forms.Cursors.Default;
            this.label3.Location = new System.Drawing.Point(53, 411);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(317, 143);
            this.label3.TabIndex = 17;
            // 
            // MainFormDB
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(1221, 595);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.dataGridView1);
            this.Controls.Add(this.buttonShow);
            this.Controls.Add(this.buttonDelete);
            this.Controls.Add(this.buttonUpdate);
            this.Controls.Add(this.buttonSave);
            this.Controls.Add(this.comboBoxClassification);
            this.Controls.Add(this.textBoxCountry);
            this.Controls.Add(this.textBoxWeight);
            this.Controls.Add(this.textBoxName);
            this.Controls.Add(this.textBoxFruitID);
            this.Controls.Add(this.labelCountry);
            this.Controls.Add(this.labelClassification);
            this.Controls.Add(this.labelWeight);
            this.Controls.Add(this.labelName);
            this.Controls.Add(this.labelFruitID);
            this.Name = "MainFormDB";
            this.Text = "MainFormDB";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label label3;

        private System.Windows.Forms.Label label2;

        private System.Windows.Forms.Label label1;

        private System.Windows.Forms.Button buttonUpdate;

        private System.Windows.Forms.DataGridView dataGridView1;

        private System.Windows.Forms.Button buttonSave;
        private System.Windows.Forms.Button buttonDelete;
        private System.Windows.Forms.Button buttonShow;

        private System.Windows.Forms.ComboBox comboBoxClassification;

        private System.Windows.Forms.TextBox textBoxWeight;
        private System.Windows.Forms.TextBox textBoxCountry;

        private System.Windows.Forms.Label labelFruitID;
        private System.Windows.Forms.Label labelName;
        private System.Windows.Forms.Label labelWeight;
        private System.Windows.Forms.Label labelClassification;
        private System.Windows.Forms.Label labelCountry;
        private System.Windows.Forms.TextBox textBoxFruitID;
        private System.Windows.Forms.TextBox textBoxName;

        #endregion
    }
}