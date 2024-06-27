using System;
using System.Drawing;
using System.Windows.Forms;

namespace SWpart2
{
  partial class Form1
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
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPageMainForm = new System.Windows.Forms.TabPage();
            this.IsCrossLabel = new System.Windows.Forms.Label();
            this.SquareLabel = new System.Windows.Forms.Label();
            this.PerimeterSquareTextBox = new System.Windows.Forms.TextBox();
            this.PerimeterLabel = new System.Windows.Forms.Label();
            this.CanvasPictureBox = new System.Windows.Forms.PictureBox();
            this.SquareButton = new System.Windows.Forms.Button();
            this.PerimeterButton = new System.Windows.Forms.Button();
            this.CleanButton = new System.Windows.Forms.Button();
            this.tabPageAddShape = new System.Windows.Forms.TabPage();
            this.Point9YtextBox = new System.Windows.Forms.TextBox();
            this.Point9XtextBox = new System.Windows.Forms.TextBox();
            this.label46 = new System.Windows.Forms.Label();
            this.label47 = new System.Windows.Forms.Label();
            this.label48 = new System.Windows.Forms.Label();
            this.Point8YtextBox = new System.Windows.Forms.TextBox();
            this.Point8XtextBox = new System.Windows.Forms.TextBox();
            this.label49 = new System.Windows.Forms.Label();
            this.label50 = new System.Windows.Forms.Label();
            this.label51 = new System.Windows.Forms.Label();
            this.Point7YtextBox = new System.Windows.Forms.TextBox();
            this.Point7XtextBox = new System.Windows.Forms.TextBox();
            this.label52 = new System.Windows.Forms.Label();
            this.label53 = new System.Windows.Forms.Label();
            this.label54 = new System.Windows.Forms.Label();
            this.Point15YtextBox = new System.Windows.Forms.TextBox();
            this.Point15XtextBox = new System.Windows.Forms.TextBox();
            this.label37 = new System.Windows.Forms.Label();
            this.label38 = new System.Windows.Forms.Label();
            this.label39 = new System.Windows.Forms.Label();
            this.Point14YtextBox = new System.Windows.Forms.TextBox();
            this.Point14XtextBox = new System.Windows.Forms.TextBox();
            this.label40 = new System.Windows.Forms.Label();
            this.label41 = new System.Windows.Forms.Label();
            this.label42 = new System.Windows.Forms.Label();
            this.Point13YtextBox = new System.Windows.Forms.TextBox();
            this.Point13XtextBox = new System.Windows.Forms.TextBox();
            this.label43 = new System.Windows.Forms.Label();
            this.label44 = new System.Windows.Forms.Label();
            this.label45 = new System.Windows.Forms.Label();
            this.Point18YtextBox = new System.Windows.Forms.TextBox();
            this.Point18XtextBox = new System.Windows.Forms.TextBox();
            this.label28 = new System.Windows.Forms.Label();
            this.label29 = new System.Windows.Forms.Label();
            this.label30 = new System.Windows.Forms.Label();
            this.Point17YtextBox = new System.Windows.Forms.TextBox();
            this.Point17XtextBox = new System.Windows.Forms.TextBox();
            this.label31 = new System.Windows.Forms.Label();
            this.label32 = new System.Windows.Forms.Label();
            this.label33 = new System.Windows.Forms.Label();
            this.Point16YtextBox = new System.Windows.Forms.TextBox();
            this.Point16XtextBox = new System.Windows.Forms.TextBox();
            this.label34 = new System.Windows.Forms.Label();
            this.label35 = new System.Windows.Forms.Label();
            this.label36 = new System.Windows.Forms.Label();
            this.Point12YtextBox = new System.Windows.Forms.TextBox();
            this.Point12XtextBox = new System.Windows.Forms.TextBox();
            this.label19 = new System.Windows.Forms.Label();
            this.label20 = new System.Windows.Forms.Label();
            this.label21 = new System.Windows.Forms.Label();
            this.Point11YtextBox = new System.Windows.Forms.TextBox();
            this.Point11XtextBox = new System.Windows.Forms.TextBox();
            this.label22 = new System.Windows.Forms.Label();
            this.label23 = new System.Windows.Forms.Label();
            this.label24 = new System.Windows.Forms.Label();
            this.Point10YtextBox = new System.Windows.Forms.TextBox();
            this.Point10XtextBox = new System.Windows.Forms.TextBox();
            this.label25 = new System.Windows.Forms.Label();
            this.label26 = new System.Windows.Forms.Label();
            this.label27 = new System.Windows.Forms.Label();
            this.Point6YtextBox = new System.Windows.Forms.TextBox();
            this.Point6XtextBox = new System.Windows.Forms.TextBox();
            this.label10 = new System.Windows.Forms.Label();
            this.label11 = new System.Windows.Forms.Label();
            this.label12 = new System.Windows.Forms.Label();
            this.Point5YtextBox = new System.Windows.Forms.TextBox();
            this.Point5XtextBox = new System.Windows.Forms.TextBox();
            this.label13 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.label15 = new System.Windows.Forms.Label();
            this.Point4YtextBox = new System.Windows.Forms.TextBox();
            this.Point4XtextBox = new System.Windows.Forms.TextBox();
            this.label16 = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            this.label18 = new System.Windows.Forms.Label();
            this.Point3YtextBox = new System.Windows.Forms.TextBox();
            this.Point3XtextBox = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.Point2YtextBox = new System.Windows.Forms.TextBox();
            this.Point2XtextBox = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.Point1YtextBox = new System.Windows.Forms.TextBox();
            this.Point1XtextBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.RadiusTextBox = new System.Windows.Forms.TextBox();
            this.RadiusLabel = new System.Windows.Forms.Label();
            this.CountPointsNumericUpDown = new System.Windows.Forms.NumericUpDown();
            this.ShapeSelectionComboBox = new System.Windows.Forms.ComboBox();
            this.AddShapeButton = new System.Windows.Forms.Button();
            this.tabPageMoveShape = new System.Windows.Forms.TabPage();
            this.AxisSymDomainUpDown = new System.Windows.Forms.DomainUpDown();
            this.AngleRotateTextBox = new System.Windows.Forms.TextBox();
            this.ShiftYTextBox = new System.Windows.Forms.TextBox();
            this.ShiftXTextBox = new System.Windows.Forms.TextBox();
            this.ShiftYlabel = new System.Windows.Forms.Label();
            this.ShiftXlabel = new System.Windows.Forms.Label();
            this.AxisSymmetryLabel = new System.Windows.Forms.Label();
            this.AngleRotationLabel = new System.Windows.Forms.Label();
            this.ShiftVectorLabel = new System.Windows.Forms.Label();
            this.MoveShapeButton = new System.Windows.Forms.Button();
            this.ShapesComboBox = new System.Windows.Forms.ComboBox();
            this.MoveComboBox = new System.Windows.Forms.ComboBox();
            this.tabPageDeleteShape = new System.Windows.Forms.TabPage();
            this.DeleteShapeButton = new System.Windows.Forms.Button();
            this.DeleteShapeComboBox = new System.Windows.Forms.ComboBox();
            this.tabPageIntersectionShapes = new System.Windows.Forms.TabPage();
            this.CrossingShapesButton = new System.Windows.Forms.Button();
            this.label56 = new System.Windows.Forms.Label();
            this.label55 = new System.Windows.Forms.Label();
            this.SecondShapeIntersectionComboBox = new System.Windows.Forms.ComboBox();
            this.FirstShapeIntersectionComboBox = new System.Windows.Forms.ComboBox();
            this.label57 = new System.Windows.Forms.Label();
            this.label58 = new System.Windows.Forms.Label();
            this.label59 = new System.Windows.Forms.Label();
            this.tabControl1.SuspendLayout();
            this.tabPageMainForm.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.CanvasPictureBox)).BeginInit();
            this.tabPageAddShape.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.CountPointsNumericUpDown)).BeginInit();
            this.tabPageMoveShape.SuspendLayout();
            this.tabPageDeleteShape.SuspendLayout();
            this.tabPageIntersectionShapes.SuspendLayout();
            this.SuspendLayout();
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPageMainForm);
            this.tabControl1.Controls.Add(this.tabPageAddShape);
            this.tabControl1.Controls.Add(this.tabPageMoveShape);
            this.tabControl1.Controls.Add(this.tabPageDeleteShape);
            this.tabControl1.Controls.Add(this.tabPageIntersectionShapes);
            this.tabControl1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabControl1.Location = new System.Drawing.Point(0, 0);
            this.tabControl1.Margin = new System.Windows.Forms.Padding(2);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(847, 584);
            this.tabControl1.TabIndex = 0;
            // 
            // tabPageMainForm
            // 
            this.tabPageMainForm.Controls.Add(this.IsCrossLabel);
            this.tabPageMainForm.Controls.Add(this.SquareLabel);
            this.tabPageMainForm.Controls.Add(this.PerimeterSquareTextBox);
            this.tabPageMainForm.Controls.Add(this.PerimeterLabel);
            this.tabPageMainForm.Controls.Add(this.CanvasPictureBox);
            this.tabPageMainForm.Controls.Add(this.SquareButton);
            this.tabPageMainForm.Controls.Add(this.PerimeterButton);
            this.tabPageMainForm.Controls.Add(this.CleanButton);
            this.tabPageMainForm.Location = new System.Drawing.Point(4, 22);
            this.tabPageMainForm.Margin = new System.Windows.Forms.Padding(2);
            this.tabPageMainForm.Name = "tabPageMainForm";
            this.tabPageMainForm.Padding = new System.Windows.Forms.Padding(2);
            this.tabPageMainForm.Size = new System.Drawing.Size(839, 558);
            this.tabPageMainForm.TabIndex = 0;
            this.tabPageMainForm.Text = "Main Form";
            this.tabPageMainForm.UseVisualStyleBackColor = true;
            // 
            // IsCrossLabel
            // 
            this.IsCrossLabel.Location = new System.Drawing.Point(688, 437);
            this.IsCrossLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.IsCrossLabel.Name = "IsCrossLabel";
            this.IsCrossLabel.Size = new System.Drawing.Size(85, 30);
            this.IsCrossLabel.TabIndex = 7;
            this.IsCrossLabel.Text = "Do they cross?";
            this.IsCrossLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.IsCrossLabel.Visible = false;
            // 
            // SquareLabel
            // 
            this.SquareLabel.Location = new System.Drawing.Point(671, 437);
            this.SquareLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.SquareLabel.Name = "SquareLabel";
            this.SquareLabel.Size = new System.Drawing.Size(85, 30);
            this.SquareLabel.TabIndex = 6;
            this.SquareLabel.Text = "Square:";
            this.SquareLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.SquareLabel.Visible = false;
            // 
            // PerimeterSquareTextBox
            // 
            this.PerimeterSquareTextBox.Location = new System.Drawing.Point(688, 469);
            this.PerimeterSquareTextBox.Margin = new System.Windows.Forms.Padding(2);
            this.PerimeterSquareTextBox.Name = "PerimeterSquareTextBox";
            this.PerimeterSquareTextBox.Size = new System.Drawing.Size(142, 20);
            this.PerimeterSquareTextBox.TabIndex = 5;
            // 
            // PerimeterLabel
            // 
            this.PerimeterLabel.Location = new System.Drawing.Point(671, 437);
            this.PerimeterLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.PerimeterLabel.Name = "PerimeterLabel";
            this.PerimeterLabel.Size = new System.Drawing.Size(85, 30);
            this.PerimeterLabel.TabIndex = 4;
            this.PerimeterLabel.Text = "Perimeter:";
            this.PerimeterLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.PerimeterLabel.Visible = false;
            // 
            // CanvasPictureBox
            // 
            this.CanvasPictureBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.CanvasPictureBox.Location = new System.Drawing.Point(6, 5);
            this.CanvasPictureBox.Margin = new System.Windows.Forms.Padding(2);
            this.CanvasPictureBox.Name = "CanvasPictureBox";
            this.CanvasPictureBox.Size = new System.Drawing.Size(661, 551);
            this.CanvasPictureBox.TabIndex = 3;
            this.CanvasPictureBox.TabStop = false;
            // 
            // SquareButton
            // 
            this.SquareButton.Location = new System.Drawing.Point(715, 145);
            this.SquareButton.Margin = new System.Windows.Forms.Padding(2);
            this.SquareButton.Name = "SquareButton";
            this.SquareButton.Size = new System.Drawing.Size(98, 24);
            this.SquareButton.TabIndex = 2;
            this.SquareButton.Text = "Square";
            this.SquareButton.UseVisualStyleBackColor = true;
            this.SquareButton.Click += new System.EventHandler(this.SquareButton_Click);
            // 
            // PerimeterButton
            // 
            this.PerimeterButton.Location = new System.Drawing.Point(715, 98);
            this.PerimeterButton.Margin = new System.Windows.Forms.Padding(2);
            this.PerimeterButton.Name = "PerimeterButton";
            this.PerimeterButton.Size = new System.Drawing.Size(98, 24);
            this.PerimeterButton.TabIndex = 1;
            this.PerimeterButton.Text = "Perimeter";
            this.PerimeterButton.UseVisualStyleBackColor = true;
            this.PerimeterButton.Click += new System.EventHandler(this.PerimeterButton_Click);
            // 
            // CleanButton
            // 
            this.CleanButton.Location = new System.Drawing.Point(715, 55);
            this.CleanButton.Margin = new System.Windows.Forms.Padding(2);
            this.CleanButton.Name = "CleanButton";
            this.CleanButton.Size = new System.Drawing.Size(98, 24);
            this.CleanButton.TabIndex = 0;
            this.CleanButton.Text = "Clean";
            this.CleanButton.UseVisualStyleBackColor = true;
            this.CleanButton.Click += new System.EventHandler(this.CleanButton_Click);
            // 
            // tabPageAddShape
            // 
            this.tabPageAddShape.Controls.Add(this.Point9YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point9XtextBox);
            this.tabPageAddShape.Controls.Add(this.label46);
            this.tabPageAddShape.Controls.Add(this.label47);
            this.tabPageAddShape.Controls.Add(this.label48);
            this.tabPageAddShape.Controls.Add(this.Point8YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point8XtextBox);
            this.tabPageAddShape.Controls.Add(this.label49);
            this.tabPageAddShape.Controls.Add(this.label50);
            this.tabPageAddShape.Controls.Add(this.label51);
            this.tabPageAddShape.Controls.Add(this.Point7YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point7XtextBox);
            this.tabPageAddShape.Controls.Add(this.label52);
            this.tabPageAddShape.Controls.Add(this.label53);
            this.tabPageAddShape.Controls.Add(this.label54);
            this.tabPageAddShape.Controls.Add(this.Point15YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point15XtextBox);
            this.tabPageAddShape.Controls.Add(this.label37);
            this.tabPageAddShape.Controls.Add(this.label38);
            this.tabPageAddShape.Controls.Add(this.label39);
            this.tabPageAddShape.Controls.Add(this.Point14YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point14XtextBox);
            this.tabPageAddShape.Controls.Add(this.label40);
            this.tabPageAddShape.Controls.Add(this.label41);
            this.tabPageAddShape.Controls.Add(this.label42);
            this.tabPageAddShape.Controls.Add(this.Point13YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point13XtextBox);
            this.tabPageAddShape.Controls.Add(this.label43);
            this.tabPageAddShape.Controls.Add(this.label44);
            this.tabPageAddShape.Controls.Add(this.label45);
            this.tabPageAddShape.Controls.Add(this.Point18YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point18XtextBox);
            this.tabPageAddShape.Controls.Add(this.label28);
            this.tabPageAddShape.Controls.Add(this.label29);
            this.tabPageAddShape.Controls.Add(this.label30);
            this.tabPageAddShape.Controls.Add(this.Point17YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point17XtextBox);
            this.tabPageAddShape.Controls.Add(this.label31);
            this.tabPageAddShape.Controls.Add(this.label32);
            this.tabPageAddShape.Controls.Add(this.label33);
            this.tabPageAddShape.Controls.Add(this.Point16YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point16XtextBox);
            this.tabPageAddShape.Controls.Add(this.label34);
            this.tabPageAddShape.Controls.Add(this.label35);
            this.tabPageAddShape.Controls.Add(this.label36);
            this.tabPageAddShape.Controls.Add(this.Point12YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point12XtextBox);
            this.tabPageAddShape.Controls.Add(this.label19);
            this.tabPageAddShape.Controls.Add(this.label20);
            this.tabPageAddShape.Controls.Add(this.label21);
            this.tabPageAddShape.Controls.Add(this.Point11YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point11XtextBox);
            this.tabPageAddShape.Controls.Add(this.label22);
            this.tabPageAddShape.Controls.Add(this.label23);
            this.tabPageAddShape.Controls.Add(this.label24);
            this.tabPageAddShape.Controls.Add(this.Point10YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point10XtextBox);
            this.tabPageAddShape.Controls.Add(this.label25);
            this.tabPageAddShape.Controls.Add(this.label26);
            this.tabPageAddShape.Controls.Add(this.label27);
            this.tabPageAddShape.Controls.Add(this.Point6YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point6XtextBox);
            this.tabPageAddShape.Controls.Add(this.label10);
            this.tabPageAddShape.Controls.Add(this.label11);
            this.tabPageAddShape.Controls.Add(this.label12);
            this.tabPageAddShape.Controls.Add(this.Point5YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point5XtextBox);
            this.tabPageAddShape.Controls.Add(this.label13);
            this.tabPageAddShape.Controls.Add(this.label14);
            this.tabPageAddShape.Controls.Add(this.label15);
            this.tabPageAddShape.Controls.Add(this.Point4YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point4XtextBox);
            this.tabPageAddShape.Controls.Add(this.label16);
            this.tabPageAddShape.Controls.Add(this.label17);
            this.tabPageAddShape.Controls.Add(this.label18);
            this.tabPageAddShape.Controls.Add(this.Point3YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point3XtextBox);
            this.tabPageAddShape.Controls.Add(this.label7);
            this.tabPageAddShape.Controls.Add(this.label8);
            this.tabPageAddShape.Controls.Add(this.label9);
            this.tabPageAddShape.Controls.Add(this.Point2YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point2XtextBox);
            this.tabPageAddShape.Controls.Add(this.label4);
            this.tabPageAddShape.Controls.Add(this.label5);
            this.tabPageAddShape.Controls.Add(this.label6);
            this.tabPageAddShape.Controls.Add(this.Point1YtextBox);
            this.tabPageAddShape.Controls.Add(this.Point1XtextBox);
            this.tabPageAddShape.Controls.Add(this.label3);
            this.tabPageAddShape.Controls.Add(this.label2);
            this.tabPageAddShape.Controls.Add(this.label1);
            this.tabPageAddShape.Controls.Add(this.RadiusTextBox);
            this.tabPageAddShape.Controls.Add(this.RadiusLabel);
            this.tabPageAddShape.Controls.Add(this.CountPointsNumericUpDown);
            this.tabPageAddShape.Controls.Add(this.ShapeSelectionComboBox);
            this.tabPageAddShape.Controls.Add(this.AddShapeButton);
            this.tabPageAddShape.Location = new System.Drawing.Point(4, 22);
            this.tabPageAddShape.Margin = new System.Windows.Forms.Padding(2);
            this.tabPageAddShape.Name = "tabPageAddShape";
            this.tabPageAddShape.Padding = new System.Windows.Forms.Padding(2);
            this.tabPageAddShape.Size = new System.Drawing.Size(839, 558);
            this.tabPageAddShape.TabIndex = 1;
            this.tabPageAddShape.Text = "Add Shape";
            this.tabPageAddShape.UseVisualStyleBackColor = true;
            this.tabPageAddShape.Enter += new System.EventHandler(this.tabPage_Enter);
            // 
            // Point9YtextBox
            // 
            this.Point9YtextBox.Location = new System.Drawing.Point(482, 272);
            this.Point9YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point9YtextBox.Name = "Point9YtextBox";
            this.Point9YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point9YtextBox.TabIndex = 94;
            // 
            // Point9XtextBox
            // 
            this.Point9XtextBox.Location = new System.Drawing.Point(418, 272);
            this.Point9XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point9XtextBox.Name = "Point9XtextBox";
            this.Point9XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point9XtextBox.TabIndex = 93;
            // 
            // label46
            // 
            this.label46.Location = new System.Drawing.Point(462, 275);
            this.label46.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label46.Name = "label46";
            this.label46.Size = new System.Drawing.Size(16, 23);
            this.label46.TabIndex = 92;
            this.label46.Text = "Y";
            // 
            // label47
            // 
            this.label47.Location = new System.Drawing.Point(400, 275);
            this.label47.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label47.Name = "label47";
            this.label47.Size = new System.Drawing.Size(14, 23);
            this.label47.TabIndex = 91;
            this.label47.Text = "X";
            // 
            // label48
            // 
            this.label48.Location = new System.Drawing.Point(400, 240);
            this.label48.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label48.Name = "label48";
            this.label48.Size = new System.Drawing.Size(59, 21);
            this.label48.TabIndex = 90;
            this.label48.Text = "Point 9";
            this.label48.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point8YtextBox
            // 
            this.Point8YtextBox.Location = new System.Drawing.Point(283, 272);
            this.Point8YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point8YtextBox.Name = "Point8YtextBox";
            this.Point8YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point8YtextBox.TabIndex = 89;
            // 
            // Point8XtextBox
            // 
            this.Point8XtextBox.Location = new System.Drawing.Point(218, 272);
            this.Point8XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point8XtextBox.Name = "Point8XtextBox";
            this.Point8XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point8XtextBox.TabIndex = 88;
            // 
            // label49
            // 
            this.label49.Location = new System.Drawing.Point(262, 275);
            this.label49.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label49.Name = "label49";
            this.label49.Size = new System.Drawing.Size(16, 23);
            this.label49.TabIndex = 87;
            this.label49.Text = "Y";
            // 
            // label50
            // 
            this.label50.Location = new System.Drawing.Point(200, 275);
            this.label50.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label50.Name = "label50";
            this.label50.Size = new System.Drawing.Size(14, 23);
            this.label50.TabIndex = 86;
            this.label50.Text = "X";
            // 
            // label51
            // 
            this.label51.Location = new System.Drawing.Point(200, 240);
            this.label51.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label51.Name = "label51";
            this.label51.Size = new System.Drawing.Size(59, 21);
            this.label51.TabIndex = 85;
            this.label51.Text = "Point 8";
            this.label51.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point7YtextBox
            // 
            this.Point7YtextBox.Location = new System.Drawing.Point(103, 272);
            this.Point7YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point7YtextBox.Name = "Point7YtextBox";
            this.Point7YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point7YtextBox.TabIndex = 84;
            // 
            // Point7XtextBox
            // 
            this.Point7XtextBox.Location = new System.Drawing.Point(38, 272);
            this.Point7XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point7XtextBox.Name = "Point7XtextBox";
            this.Point7XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point7XtextBox.TabIndex = 83;
            // 
            // label52
            // 
            this.label52.Location = new System.Drawing.Point(82, 275);
            this.label52.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label52.Name = "label52";
            this.label52.Size = new System.Drawing.Size(16, 23);
            this.label52.TabIndex = 82;
            this.label52.Text = "Y";
            // 
            // label53
            // 
            this.label53.Location = new System.Drawing.Point(20, 275);
            this.label53.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label53.Name = "label53";
            this.label53.Size = new System.Drawing.Size(14, 23);
            this.label53.TabIndex = 81;
            this.label53.Text = "X";
            // 
            // label54
            // 
            this.label54.Location = new System.Drawing.Point(20, 240);
            this.label54.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label54.Name = "label54";
            this.label54.Size = new System.Drawing.Size(59, 21);
            this.label54.TabIndex = 80;
            this.label54.Text = "Point 7";
            this.label54.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point15YtextBox
            // 
            this.Point15YtextBox.Location = new System.Drawing.Point(482, 430);
            this.Point15YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point15YtextBox.Name = "Point15YtextBox";
            this.Point15YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point15YtextBox.TabIndex = 79;
            // 
            // Point15XtextBox
            // 
            this.Point15XtextBox.Location = new System.Drawing.Point(418, 430);
            this.Point15XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point15XtextBox.Name = "Point15XtextBox";
            this.Point15XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point15XtextBox.TabIndex = 78;
            // 
            // label37
            // 
            this.label37.Location = new System.Drawing.Point(462, 432);
            this.label37.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label37.Name = "label37";
            this.label37.Size = new System.Drawing.Size(16, 23);
            this.label37.TabIndex = 77;
            this.label37.Text = "Y";
            // 
            // label38
            // 
            this.label38.Location = new System.Drawing.Point(400, 432);
            this.label38.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label38.Name = "label38";
            this.label38.Size = new System.Drawing.Size(14, 23);
            this.label38.TabIndex = 76;
            this.label38.Text = "X";
            // 
            // label39
            // 
            this.label39.Location = new System.Drawing.Point(400, 397);
            this.label39.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label39.Name = "label39";
            this.label39.Size = new System.Drawing.Size(59, 21);
            this.label39.TabIndex = 75;
            this.label39.Text = "Point 15";
            this.label39.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point14YtextBox
            // 
            this.Point14YtextBox.Location = new System.Drawing.Point(283, 430);
            this.Point14YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point14YtextBox.Name = "Point14YtextBox";
            this.Point14YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point14YtextBox.TabIndex = 74;
            // 
            // Point14XtextBox
            // 
            this.Point14XtextBox.Location = new System.Drawing.Point(218, 430);
            this.Point14XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point14XtextBox.Name = "Point14XtextBox";
            this.Point14XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point14XtextBox.TabIndex = 73;
            // 
            // label40
            // 
            this.label40.Location = new System.Drawing.Point(262, 432);
            this.label40.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label40.Name = "label40";
            this.label40.Size = new System.Drawing.Size(16, 23);
            this.label40.TabIndex = 72;
            this.label40.Text = "Y";
            // 
            // label41
            // 
            this.label41.Location = new System.Drawing.Point(200, 432);
            this.label41.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label41.Name = "label41";
            this.label41.Size = new System.Drawing.Size(14, 23);
            this.label41.TabIndex = 71;
            this.label41.Text = "X";
            // 
            // label42
            // 
            this.label42.Location = new System.Drawing.Point(200, 397);
            this.label42.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label42.Name = "label42";
            this.label42.Size = new System.Drawing.Size(59, 21);
            this.label42.TabIndex = 70;
            this.label42.Text = "Point 14";
            this.label42.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point13YtextBox
            // 
            this.Point13YtextBox.Location = new System.Drawing.Point(103, 430);
            this.Point13YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point13YtextBox.Name = "Point13YtextBox";
            this.Point13YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point13YtextBox.TabIndex = 69;
            // 
            // Point13XtextBox
            // 
            this.Point13XtextBox.Location = new System.Drawing.Point(38, 430);
            this.Point13XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point13XtextBox.Name = "Point13XtextBox";
            this.Point13XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point13XtextBox.TabIndex = 68;
            // 
            // label43
            // 
            this.label43.Location = new System.Drawing.Point(82, 432);
            this.label43.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label43.Name = "label43";
            this.label43.Size = new System.Drawing.Size(16, 23);
            this.label43.TabIndex = 67;
            this.label43.Text = "Y";
            // 
            // label44
            // 
            this.label44.Location = new System.Drawing.Point(20, 432);
            this.label44.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label44.Name = "label44";
            this.label44.Size = new System.Drawing.Size(14, 23);
            this.label44.TabIndex = 66;
            this.label44.Text = "X";
            // 
            // label45
            // 
            this.label45.Location = new System.Drawing.Point(20, 397);
            this.label45.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label45.Name = "label45";
            this.label45.Size = new System.Drawing.Size(59, 21);
            this.label45.TabIndex = 65;
            this.label45.Text = "Point 13";
            this.label45.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point18YtextBox
            // 
            this.Point18YtextBox.Location = new System.Drawing.Point(482, 502);
            this.Point18YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point18YtextBox.Name = "Point18YtextBox";
            this.Point18YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point18YtextBox.TabIndex = 64;
            // 
            // Point18XtextBox
            // 
            this.Point18XtextBox.Location = new System.Drawing.Point(418, 502);
            this.Point18XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point18XtextBox.Name = "Point18XtextBox";
            this.Point18XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point18XtextBox.TabIndex = 63;
            // 
            // label28
            // 
            this.label28.Location = new System.Drawing.Point(463, 505);
            this.label28.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label28.Name = "label28";
            this.label28.Size = new System.Drawing.Size(16, 23);
            this.label28.TabIndex = 62;
            this.label28.Text = "Y";
            // 
            // label29
            // 
            this.label29.Location = new System.Drawing.Point(400, 505);
            this.label29.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label29.Name = "label29";
            this.label29.Size = new System.Drawing.Size(14, 23);
            this.label29.TabIndex = 61;
            this.label29.Text = "X";
            // 
            // label30
            // 
            this.label30.Location = new System.Drawing.Point(400, 470);
            this.label30.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label30.Name = "label30";
            this.label30.Size = new System.Drawing.Size(59, 21);
            this.label30.TabIndex = 60;
            this.label30.Text = "Point 18";
            this.label30.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point17YtextBox
            // 
            this.Point17YtextBox.Location = new System.Drawing.Point(283, 502);
            this.Point17YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point17YtextBox.Name = "Point17YtextBox";
            this.Point17YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point17YtextBox.TabIndex = 59;
            // 
            // Point17XtextBox
            // 
            this.Point17XtextBox.Location = new System.Drawing.Point(218, 502);
            this.Point17XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point17XtextBox.Name = "Point17XtextBox";
            this.Point17XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point17XtextBox.TabIndex = 58;
            // 
            // label31
            // 
            this.label31.Location = new System.Drawing.Point(262, 505);
            this.label31.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label31.Name = "label31";
            this.label31.Size = new System.Drawing.Size(16, 23);
            this.label31.TabIndex = 57;
            this.label31.Text = "Y";
            // 
            // label32
            // 
            this.label32.Location = new System.Drawing.Point(200, 505);
            this.label32.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label32.Name = "label32";
            this.label32.Size = new System.Drawing.Size(14, 23);
            this.label32.TabIndex = 56;
            this.label32.Text = "X";
            // 
            // label33
            // 
            this.label33.Location = new System.Drawing.Point(200, 470);
            this.label33.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label33.Name = "label33";
            this.label33.Size = new System.Drawing.Size(59, 21);
            this.label33.TabIndex = 55;
            this.label33.Text = "Point 17";
            this.label33.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point16YtextBox
            // 
            this.Point16YtextBox.Location = new System.Drawing.Point(103, 502);
            this.Point16YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point16YtextBox.Name = "Point16YtextBox";
            this.Point16YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point16YtextBox.TabIndex = 54;
            // 
            // Point16XtextBox
            // 
            this.Point16XtextBox.Location = new System.Drawing.Point(38, 502);
            this.Point16XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point16XtextBox.Name = "Point16XtextBox";
            this.Point16XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point16XtextBox.TabIndex = 53;
            // 
            // label34
            // 
            this.label34.Location = new System.Drawing.Point(82, 505);
            this.label34.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label34.Name = "label34";
            this.label34.Size = new System.Drawing.Size(16, 23);
            this.label34.TabIndex = 52;
            this.label34.Text = "Y";
            // 
            // label35
            // 
            this.label35.Location = new System.Drawing.Point(20, 505);
            this.label35.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label35.Name = "label35";
            this.label35.Size = new System.Drawing.Size(14, 23);
            this.label35.TabIndex = 51;
            this.label35.Text = "X";
            // 
            // label36
            // 
            this.label36.Location = new System.Drawing.Point(20, 470);
            this.label36.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label36.Name = "label36";
            this.label36.Size = new System.Drawing.Size(59, 21);
            this.label36.TabIndex = 50;
            this.label36.Text = "Point 16";
            this.label36.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point12YtextBox
            // 
            this.Point12YtextBox.Location = new System.Drawing.Point(482, 353);
            this.Point12YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point12YtextBox.Name = "Point12YtextBox";
            this.Point12YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point12YtextBox.TabIndex = 49;
            // 
            // Point12XtextBox
            // 
            this.Point12XtextBox.Location = new System.Drawing.Point(418, 353);
            this.Point12XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point12XtextBox.Name = "Point12XtextBox";
            this.Point12XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point12XtextBox.TabIndex = 48;
            // 
            // label19
            // 
            this.label19.Location = new System.Drawing.Point(462, 356);
            this.label19.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label19.Name = "label19";
            this.label19.Size = new System.Drawing.Size(16, 23);
            this.label19.TabIndex = 47;
            this.label19.Text = "Y";
            // 
            // label20
            // 
            this.label20.Location = new System.Drawing.Point(400, 356);
            this.label20.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label20.Name = "label20";
            this.label20.Size = new System.Drawing.Size(14, 23);
            this.label20.TabIndex = 46;
            this.label20.Text = "X";
            // 
            // label21
            // 
            this.label21.Location = new System.Drawing.Point(400, 321);
            this.label21.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label21.Name = "label21";
            this.label21.Size = new System.Drawing.Size(59, 21);
            this.label21.TabIndex = 45;
            this.label21.Text = "Point 12";
            this.label21.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point11YtextBox
            // 
            this.Point11YtextBox.Location = new System.Drawing.Point(283, 353);
            this.Point11YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point11YtextBox.Name = "Point11YtextBox";
            this.Point11YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point11YtextBox.TabIndex = 44;
            // 
            // Point11XtextBox
            // 
            this.Point11XtextBox.Location = new System.Drawing.Point(218, 353);
            this.Point11XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point11XtextBox.Name = "Point11XtextBox";
            this.Point11XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point11XtextBox.TabIndex = 43;
            // 
            // label22
            // 
            this.label22.Location = new System.Drawing.Point(262, 356);
            this.label22.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label22.Name = "label22";
            this.label22.Size = new System.Drawing.Size(16, 23);
            this.label22.TabIndex = 42;
            this.label22.Text = "Y";
            // 
            // label23
            // 
            this.label23.Location = new System.Drawing.Point(200, 356);
            this.label23.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label23.Name = "label23";
            this.label23.Size = new System.Drawing.Size(14, 23);
            this.label23.TabIndex = 41;
            this.label23.Text = "X";
            // 
            // label24
            // 
            this.label24.Location = new System.Drawing.Point(200, 321);
            this.label24.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label24.Name = "label24";
            this.label24.Size = new System.Drawing.Size(59, 21);
            this.label24.TabIndex = 40;
            this.label24.Text = "Point 11";
            this.label24.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point10YtextBox
            // 
            this.Point10YtextBox.Location = new System.Drawing.Point(103, 353);
            this.Point10YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point10YtextBox.Name = "Point10YtextBox";
            this.Point10YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point10YtextBox.TabIndex = 39;
            // 
            // Point10XtextBox
            // 
            this.Point10XtextBox.Location = new System.Drawing.Point(38, 353);
            this.Point10XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point10XtextBox.Name = "Point10XtextBox";
            this.Point10XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point10XtextBox.TabIndex = 38;
            // 
            // label25
            // 
            this.label25.Location = new System.Drawing.Point(82, 356);
            this.label25.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label25.Name = "label25";
            this.label25.Size = new System.Drawing.Size(16, 23);
            this.label25.TabIndex = 37;
            this.label25.Text = "Y";
            // 
            // label26
            // 
            this.label26.Location = new System.Drawing.Point(20, 356);
            this.label26.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label26.Name = "label26";
            this.label26.Size = new System.Drawing.Size(14, 23);
            this.label26.TabIndex = 36;
            this.label26.Text = "X";
            // 
            // label27
            // 
            this.label27.Location = new System.Drawing.Point(20, 321);
            this.label27.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label27.Name = "label27";
            this.label27.Size = new System.Drawing.Size(59, 21);
            this.label27.TabIndex = 35;
            this.label27.Text = "Point 10";
            this.label27.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point6YtextBox
            // 
            this.Point6YtextBox.Location = new System.Drawing.Point(482, 192);
            this.Point6YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point6YtextBox.Name = "Point6YtextBox";
            this.Point6YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point6YtextBox.TabIndex = 34;
            // 
            // Point6XtextBox
            // 
            this.Point6XtextBox.Location = new System.Drawing.Point(418, 192);
            this.Point6XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point6XtextBox.Name = "Point6XtextBox";
            this.Point6XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point6XtextBox.TabIndex = 33;
            // 
            // label10
            // 
            this.label10.Location = new System.Drawing.Point(462, 194);
            this.label10.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(16, 23);
            this.label10.TabIndex = 32;
            this.label10.Text = "Y";
            // 
            // label11
            // 
            this.label11.Location = new System.Drawing.Point(400, 194);
            this.label11.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(14, 23);
            this.label11.TabIndex = 31;
            this.label11.Text = "X";
            // 
            // label12
            // 
            this.label12.Location = new System.Drawing.Point(400, 159);
            this.label12.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(59, 21);
            this.label12.TabIndex = 30;
            this.label12.Text = "Point 6";
            this.label12.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point5YtextBox
            // 
            this.Point5YtextBox.Location = new System.Drawing.Point(283, 192);
            this.Point5YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point5YtextBox.Name = "Point5YtextBox";
            this.Point5YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point5YtextBox.TabIndex = 29;
            // 
            // Point5XtextBox
            // 
            this.Point5XtextBox.Location = new System.Drawing.Point(218, 192);
            this.Point5XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point5XtextBox.Name = "Point5XtextBox";
            this.Point5XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point5XtextBox.TabIndex = 28;
            // 
            // label13
            // 
            this.label13.Location = new System.Drawing.Point(262, 194);
            this.label13.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(16, 23);
            this.label13.TabIndex = 27;
            this.label13.Text = "Y";
            // 
            // label14
            // 
            this.label14.Location = new System.Drawing.Point(200, 194);
            this.label14.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(14, 23);
            this.label14.TabIndex = 26;
            this.label14.Text = "X";
            // 
            // label15
            // 
            this.label15.Location = new System.Drawing.Point(200, 159);
            this.label15.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(59, 21);
            this.label15.TabIndex = 25;
            this.label15.Text = "Point 5";
            this.label15.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point4YtextBox
            // 
            this.Point4YtextBox.Location = new System.Drawing.Point(103, 192);
            this.Point4YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point4YtextBox.Name = "Point4YtextBox";
            this.Point4YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point4YtextBox.TabIndex = 24;
            // 
            // Point4XtextBox
            // 
            this.Point4XtextBox.Location = new System.Drawing.Point(38, 192);
            this.Point4XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point4XtextBox.Name = "Point4XtextBox";
            this.Point4XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point4XtextBox.TabIndex = 23;
            // 
            // label16
            // 
            this.label16.Location = new System.Drawing.Point(82, 194);
            this.label16.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(16, 23);
            this.label16.TabIndex = 22;
            this.label16.Text = "Y";
            // 
            // label17
            // 
            this.label17.Location = new System.Drawing.Point(20, 194);
            this.label17.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(14, 23);
            this.label17.TabIndex = 21;
            this.label17.Text = "X";
            // 
            // label18
            // 
            this.label18.Location = new System.Drawing.Point(20, 159);
            this.label18.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(59, 21);
            this.label18.TabIndex = 20;
            this.label18.Text = "Point 4";
            this.label18.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point3YtextBox
            // 
            this.Point3YtextBox.Location = new System.Drawing.Point(482, 120);
            this.Point3YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point3YtextBox.Name = "Point3YtextBox";
            this.Point3YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point3YtextBox.TabIndex = 19;
            // 
            // Point3XtextBox
            // 
            this.Point3XtextBox.Location = new System.Drawing.Point(418, 120);
            this.Point3XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point3XtextBox.Name = "Point3XtextBox";
            this.Point3XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point3XtextBox.TabIndex = 18;
            // 
            // label7
            // 
            this.label7.Location = new System.Drawing.Point(462, 123);
            this.label7.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(16, 23);
            this.label7.TabIndex = 17;
            this.label7.Text = "Y";
            // 
            // label8
            // 
            this.label8.Location = new System.Drawing.Point(400, 123);
            this.label8.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(14, 23);
            this.label8.TabIndex = 16;
            this.label8.Text = "X";
            // 
            // label9
            // 
            this.label9.Location = new System.Drawing.Point(400, 88);
            this.label9.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(59, 21);
            this.label9.TabIndex = 15;
            this.label9.Text = "Point 3";
            this.label9.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point2YtextBox
            // 
            this.Point2YtextBox.Location = new System.Drawing.Point(283, 120);
            this.Point2YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point2YtextBox.Name = "Point2YtextBox";
            this.Point2YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point2YtextBox.TabIndex = 14;
            // 
            // Point2XtextBox
            // 
            this.Point2XtextBox.Location = new System.Drawing.Point(218, 120);
            this.Point2XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point2XtextBox.Name = "Point2XtextBox";
            this.Point2XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point2XtextBox.TabIndex = 13;
            // 
            // label4
            // 
            this.label4.Location = new System.Drawing.Point(262, 123);
            this.label4.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(16, 23);
            this.label4.TabIndex = 12;
            this.label4.Text = "Y";
            // 
            // label5
            // 
            this.label5.Location = new System.Drawing.Point(200, 123);
            this.label5.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(14, 23);
            this.label5.TabIndex = 11;
            this.label5.Text = "X";
            // 
            // label6
            // 
            this.label6.Location = new System.Drawing.Point(200, 88);
            this.label6.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(59, 21);
            this.label6.TabIndex = 10;
            this.label6.Text = "Point 2";
            this.label6.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Point1YtextBox
            // 
            this.Point1YtextBox.Location = new System.Drawing.Point(103, 120);
            this.Point1YtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point1YtextBox.Name = "Point1YtextBox";
            this.Point1YtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point1YtextBox.TabIndex = 9;
            // 
            // Point1XtextBox
            // 
            this.Point1XtextBox.Location = new System.Drawing.Point(38, 120);
            this.Point1XtextBox.Margin = new System.Windows.Forms.Padding(2);
            this.Point1XtextBox.Name = "Point1XtextBox";
            this.Point1XtextBox.Size = new System.Drawing.Size(41, 20);
            this.Point1XtextBox.TabIndex = 8;
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(82, 123);
            this.label3.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(16, 23);
            this.label3.TabIndex = 7;
            this.label3.Text = "Y";
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(20, 123);
            this.label2.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(14, 23);
            this.label2.TabIndex = 6;
            this.label2.Text = "X";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(20, 88);
            this.label1.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(59, 21);
            this.label1.TabIndex = 5;
            this.label1.Text = "Point 1";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // RadiusTextBox
            // 
            this.RadiusTextBox.Location = new System.Drawing.Point(400, 28);
            this.RadiusTextBox.Margin = new System.Windows.Forms.Padding(2);
            this.RadiusTextBox.Name = "RadiusTextBox";
            this.RadiusTextBox.Size = new System.Drawing.Size(41, 20);
            this.RadiusTextBox.TabIndex = 4;
            // 
            // RadiusLabel
            // 
            this.RadiusLabel.Location = new System.Drawing.Point(322, 24);
            this.RadiusLabel.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.RadiusLabel.Name = "RadiusLabel";
            this.RadiusLabel.Size = new System.Drawing.Size(92, 26);
            this.RadiusLabel.TabIndex = 3;
            this.RadiusLabel.Text = "Radius";
            this.RadiusLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // CountPointsNumericUpDown
            // 
            this.CountPointsNumericUpDown.Location = new System.Drawing.Point(200, 29);
            this.CountPointsNumericUpDown.Margin = new System.Windows.Forms.Padding(2);
            this.CountPointsNumericUpDown.Name = "CountPointsNumericUpDown";
            this.CountPointsNumericUpDown.Size = new System.Drawing.Size(109, 20);
            this.CountPointsNumericUpDown.TabIndex = 2;
            // 
            // ShapeSelectionComboBox
            // 
            this.ShapeSelectionComboBox.FormattingEnabled = true;
            this.ShapeSelectionComboBox.Items.AddRange(new object[] { "Segment", "Polyline", "Circle", "Polygon", "Triangle", "Quadrangle", "Rectangle", "Trapeze" });
            this.ShapeSelectionComboBox.Location = new System.Drawing.Point(20, 28);
            this.ShapeSelectionComboBox.Margin = new System.Windows.Forms.Padding(2);
            this.ShapeSelectionComboBox.Name = "ShapeSelectionComboBox";
            this.ShapeSelectionComboBox.Size = new System.Drawing.Size(149, 21);
            this.ShapeSelectionComboBox.TabIndex = 1;
            this.ShapeSelectionComboBox.SelectedIndexChanged += new System.EventHandler(this.ShapeSelectionComboBox_SelectedIndexChanged);
            // 
            // AddShapeButton
            // 
            this.AddShapeButton.Location = new System.Drawing.Point(645, 47);
            this.AddShapeButton.Margin = new System.Windows.Forms.Padding(2);
            this.AddShapeButton.Name = "AddShapeButton";
            this.AddShapeButton.Size = new System.Drawing.Size(144, 38);
            this.AddShapeButton.TabIndex = 0;
            this.AddShapeButton.Text = "Add Shape";
            this.AddShapeButton.UseVisualStyleBackColor = true;
            this.AddShapeButton.Click += new System.EventHandler(this.AddShapeButton_Click);
            // 
            // tabPageMoveShape
            // 
            this.tabPageMoveShape.Controls.Add(this.label58);
            this.tabPageMoveShape.Controls.Add(this.label57);
            this.tabPageMoveShape.Controls.Add(this.AxisSymDomainUpDown);
            this.tabPageMoveShape.Controls.Add(this.AngleRotateTextBox);
            this.tabPageMoveShape.Controls.Add(this.ShiftYTextBox);
            this.tabPageMoveShape.Controls.Add(this.ShiftXTextBox);
            this.tabPageMoveShape.Controls.Add(this.ShiftYlabel);
            this.tabPageMoveShape.Controls.Add(this.ShiftXlabel);
            this.tabPageMoveShape.Controls.Add(this.AxisSymmetryLabel);
            this.tabPageMoveShape.Controls.Add(this.AngleRotationLabel);
            this.tabPageMoveShape.Controls.Add(this.ShiftVectorLabel);
            this.tabPageMoveShape.Controls.Add(this.MoveShapeButton);
            this.tabPageMoveShape.Controls.Add(this.ShapesComboBox);
            this.tabPageMoveShape.Controls.Add(this.MoveComboBox);
            this.tabPageMoveShape.Location = new System.Drawing.Point(4, 22);
            this.tabPageMoveShape.Margin = new System.Windows.Forms.Padding(2);
            this.tabPageMoveShape.Name = "tabPageMoveShape";
            this.tabPageMoveShape.Padding = new System.Windows.Forms.Padding(2);
            this.tabPageMoveShape.Size = new System.Drawing.Size(839, 558);
            this.tabPageMoveShape.TabIndex = 2;
            this.tabPageMoveShape.Text = "Move Shape";
            this.tabPageMoveShape.UseVisualStyleBackColor = true;
            this.tabPageMoveShape.Enter += new System.EventHandler(this.tabPage_Enter);
            // 
            // AxisSymDomainUpDown
            // 
            this.AxisSymDomainUpDown.Items.Add("X");
            this.AxisSymDomainUpDown.Items.Add("Y");
            this.AxisSymDomainUpDown.Location = new System.Drawing.Point(24, 373);
            this.AxisSymDomainUpDown.Name = "AxisSymDomainUpDown";
            this.AxisSymDomainUpDown.ReadOnly = true;
            this.AxisSymDomainUpDown.Size = new System.Drawing.Size(108, 20);
            this.AxisSymDomainUpDown.TabIndex = 11;
            this.AxisSymDomainUpDown.TabStop = false;
            this.AxisSymDomainUpDown.Wrap = true;
            // 
            // AngleRotateTextBox
            // 
            this.AngleRotateTextBox.Location = new System.Drawing.Point(26, 291);
            this.AngleRotateTextBox.Name = "AngleRotateTextBox";
            this.AngleRotateTextBox.Size = new System.Drawing.Size(107, 20);
            this.AngleRotateTextBox.TabIndex = 10;
            // 
            // ShiftYTextBox
            // 
            this.ShiftYTextBox.Location = new System.Drawing.Point(140, 205);
            this.ShiftYTextBox.Name = "ShiftYTextBox";
            this.ShiftYTextBox.Size = new System.Drawing.Size(66, 20);
            this.ShiftYTextBox.TabIndex = 9;
            // 
            // ShiftXTextBox
            // 
            this.ShiftXTextBox.Location = new System.Drawing.Point(46, 205);
            this.ShiftXTextBox.Name = "ShiftXTextBox";
            this.ShiftXTextBox.Size = new System.Drawing.Size(66, 20);
            this.ShiftXTextBox.TabIndex = 8;
            // 
            // ShiftYlabel
            // 
            this.ShiftYlabel.Location = new System.Drawing.Point(118, 208);
            this.ShiftYlabel.Name = "ShiftYlabel";
            this.ShiftYlabel.Size = new System.Drawing.Size(32, 30);
            this.ShiftYlabel.TabIndex = 7;
            this.ShiftYlabel.Text = "Y";
            // 
            // ShiftXlabel
            // 
            this.ShiftXlabel.Location = new System.Drawing.Point(26, 208);
            this.ShiftXlabel.Name = "ShiftXlabel";
            this.ShiftXlabel.Size = new System.Drawing.Size(32, 30);
            this.ShiftXlabel.TabIndex = 6;
            this.ShiftXlabel.Text = "X";
            // 
            // AxisSymmetryLabel
            // 
            this.AxisSymmetryLabel.Location = new System.Drawing.Point(25, 343);
            this.AxisSymmetryLabel.Name = "AxisSymmetryLabel";
            this.AxisSymmetryLabel.Size = new System.Drawing.Size(107, 38);
            this.AxisSymmetryLabel.TabIndex = 5;
            this.AxisSymmetryLabel.Text = "Axis of symmetry:";
            // 
            // AngleRotationLabel
            // 
            this.AngleRotationLabel.Location = new System.Drawing.Point(26, 262);
            this.AngleRotationLabel.Name = "AngleRotationLabel";
            this.AngleRotationLabel.Size = new System.Drawing.Size(107, 38);
            this.AngleRotationLabel.TabIndex = 4;
            this.AngleRotationLabel.Text = "Angle of rotation:";
            // 
            // ShiftVectorLabel
            // 
            this.ShiftVectorLabel.Location = new System.Drawing.Point(25, 170);
            this.ShiftVectorLabel.Name = "ShiftVectorLabel";
            this.ShiftVectorLabel.Size = new System.Drawing.Size(107, 38);
            this.ShiftVectorLabel.TabIndex = 3;
            this.ShiftVectorLabel.Text = "Shift Vector:";
            // 
            // MoveShapeButton
            // 
            this.MoveShapeButton.Location = new System.Drawing.Point(584, 42);
            this.MoveShapeButton.Name = "MoveShapeButton";
            this.MoveShapeButton.Size = new System.Drawing.Size(175, 31);
            this.MoveShapeButton.TabIndex = 2;
            this.MoveShapeButton.Text = "Move Shape";
            this.MoveShapeButton.UseVisualStyleBackColor = true;
            this.MoveShapeButton.Click += new System.EventHandler(this.MoveShapeButton_Click);
            // 
            // ShapesComboBox
            // 
            this.ShapesComboBox.FormattingEnabled = true;
            this.ShapesComboBox.Location = new System.Drawing.Point(25, 119);
            this.ShapesComboBox.Name = "ShapesComboBox";
            this.ShapesComboBox.Size = new System.Drawing.Size(232, 21);
            this.ShapesComboBox.TabIndex = 1;
            // 
            // MoveComboBox
            // 
            this.MoveComboBox.FormattingEnabled = true;
            this.MoveComboBox.Items.AddRange(new object[] { "Shift", "Rotation", "Symmetry" });
            this.MoveComboBox.Location = new System.Drawing.Point(26, 54);
            this.MoveComboBox.Name = "MoveComboBox";
            this.MoveComboBox.Size = new System.Drawing.Size(232, 21);
            this.MoveComboBox.TabIndex = 0;
            this.MoveComboBox.SelectedIndexChanged += new System.EventHandler(this.MoveComboBox_SelectedIndexChanged);
            // 
            // tabPageDeleteShape
            // 
            this.tabPageDeleteShape.Controls.Add(this.label59);
            this.tabPageDeleteShape.Controls.Add(this.DeleteShapeButton);
            this.tabPageDeleteShape.Controls.Add(this.DeleteShapeComboBox);
            this.tabPageDeleteShape.Location = new System.Drawing.Point(4, 22);
            this.tabPageDeleteShape.Margin = new System.Windows.Forms.Padding(2);
            this.tabPageDeleteShape.Name = "tabPageDeleteShape";
            this.tabPageDeleteShape.Padding = new System.Windows.Forms.Padding(2);
            this.tabPageDeleteShape.Size = new System.Drawing.Size(839, 558);
            this.tabPageDeleteShape.TabIndex = 3;
            this.tabPageDeleteShape.Text = "Delete Shape";
            this.tabPageDeleteShape.UseVisualStyleBackColor = true;
            this.tabPageDeleteShape.Enter += new System.EventHandler(this.tabPage_Enter);
            // 
            // DeleteShapeButton
            // 
            this.DeleteShapeButton.Location = new System.Drawing.Point(633, 22);
            this.DeleteShapeButton.Name = "DeleteShapeButton";
            this.DeleteShapeButton.Size = new System.Drawing.Size(167, 34);
            this.DeleteShapeButton.TabIndex = 1;
            this.DeleteShapeButton.Text = "Delete Shape";
            this.DeleteShapeButton.UseVisualStyleBackColor = true;
            this.DeleteShapeButton.Click += new System.EventHandler(this.DeleteShapeButton_Click);
            // 
            // DeleteShapeComboBox
            // 
            this.DeleteShapeComboBox.FormattingEnabled = true;
            this.DeleteShapeComboBox.Location = new System.Drawing.Point(18, 76);
            this.DeleteShapeComboBox.Name = "DeleteShapeComboBox";
            this.DeleteShapeComboBox.Size = new System.Drawing.Size(308, 21);
            this.DeleteShapeComboBox.TabIndex = 0;
            // 
            // tabPageIntersectionShapes
            // 
            this.tabPageIntersectionShapes.Controls.Add(this.CrossingShapesButton);
            this.tabPageIntersectionShapes.Controls.Add(this.label56);
            this.tabPageIntersectionShapes.Controls.Add(this.label55);
            this.tabPageIntersectionShapes.Controls.Add(this.SecondShapeIntersectionComboBox);
            this.tabPageIntersectionShapes.Controls.Add(this.FirstShapeIntersectionComboBox);
            this.tabPageIntersectionShapes.Location = new System.Drawing.Point(4, 22);
            this.tabPageIntersectionShapes.Margin = new System.Windows.Forms.Padding(2);
            this.tabPageIntersectionShapes.Name = "tabPageIntersectionShapes";
            this.tabPageIntersectionShapes.Padding = new System.Windows.Forms.Padding(2);
            this.tabPageIntersectionShapes.Size = new System.Drawing.Size(839, 558);
            this.tabPageIntersectionShapes.TabIndex = 4;
            this.tabPageIntersectionShapes.Text = "Intersection of shapes";
            this.tabPageIntersectionShapes.UseVisualStyleBackColor = true;
            this.tabPageIntersectionShapes.Enter += new System.EventHandler(this.tabPage_Enter);
            // 
            // CrossingShapesButton
            // 
            this.CrossingShapesButton.Location = new System.Drawing.Point(667, 35);
            this.CrossingShapesButton.Name = "CrossingShapesButton";
            this.CrossingShapesButton.Size = new System.Drawing.Size(130, 39);
            this.CrossingShapesButton.TabIndex = 4;
            this.CrossingShapesButton.Text = "Crossing Shapes";
            this.CrossingShapesButton.UseVisualStyleBackColor = true;
            this.CrossingShapesButton.Click += new System.EventHandler(this.CrossingShapesButton_Click);
            // 
            // label56
            // 
            this.label56.Location = new System.Drawing.Point(11, 145);
            this.label56.Name = "label56";
            this.label56.Size = new System.Drawing.Size(120, 49);
            this.label56.TabIndex = 3;
            this.label56.Text = "Second figure to intersect:";
            this.label56.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label55
            // 
            this.label55.Location = new System.Drawing.Point(11, 11);
            this.label55.Name = "label55";
            this.label55.Size = new System.Drawing.Size(106, 49);
            this.label55.TabIndex = 2;
            this.label55.Text = "First figure to intersect:";
            this.label55.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // SecondShapeIntersectionComboBox
            // 
            this.SecondShapeIntersectionComboBox.FormattingEnabled = true;
            this.SecondShapeIntersectionComboBox.Location = new System.Drawing.Point(25, 197);
            this.SecondShapeIntersectionComboBox.Name = "SecondShapeIntersectionComboBox";
            this.SecondShapeIntersectionComboBox.Size = new System.Drawing.Size(384, 21);
            this.SecondShapeIntersectionComboBox.TabIndex = 1;
            // 
            // FirstShapeIntersectionComboBox
            // 
            this.FirstShapeIntersectionComboBox.FormattingEnabled = true;
            this.FirstShapeIntersectionComboBox.Location = new System.Drawing.Point(25, 63);
            this.FirstShapeIntersectionComboBox.Name = "FirstShapeIntersectionComboBox";
            this.FirstShapeIntersectionComboBox.Size = new System.Drawing.Size(384, 21);
            this.FirstShapeIntersectionComboBox.TabIndex = 0;
            // 
            // label57
            // 
            this.label57.Location = new System.Drawing.Point(8, 89);
            this.label57.Name = "label57";
            this.label57.Size = new System.Drawing.Size(107, 27);
            this.label57.TabIndex = 12;
            this.label57.Text = "Choose a Shape:";
            this.label57.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label58
            // 
            this.label58.Location = new System.Drawing.Point(8, 20);
            this.label58.Name = "label58";
            this.label58.Size = new System.Drawing.Size(107, 31);
            this.label58.TabIndex = 13;
            this.label58.Text = "Choose a Move:\r\n";
            this.label58.TextAlign = System.Drawing.ContentAlignment.BottomCenter;
            // 
            // label59
            // 
            this.label59.Location = new System.Drawing.Point(8, 46);
            this.label59.Name = "label59";
            this.label59.Size = new System.Drawing.Size(107, 27);
            this.label59.TabIndex = 13;
            this.label59.Text = "Choose a Shape:";
            this.label59.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(847, 584);
            this.Controls.Add(this.tabControl1);
            this.Location = new System.Drawing.Point(15, 15);
            this.Margin = new System.Windows.Forms.Padding(2);
            this.Name = "Form1";
            this.Text = "Geometric Shapes";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.tabControl1.ResumeLayout(false);
            this.tabPageMainForm.ResumeLayout(false);
            this.tabPageMainForm.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.CanvasPictureBox)).EndInit();
            this.tabPageAddShape.ResumeLayout(false);
            this.tabPageAddShape.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.CountPointsNumericUpDown)).EndInit();
            this.tabPageMoveShape.ResumeLayout(false);
            this.tabPageMoveShape.PerformLayout();
            this.tabPageDeleteShape.ResumeLayout(false);
            this.tabPageIntersectionShapes.ResumeLayout(false);
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label label59;

        private System.Windows.Forms.Label label57;
        private System.Windows.Forms.Label label58;

        private System.Windows.Forms.Label IsCrossLabel;

        private System.Windows.Forms.PictureBox pictureBox1;

        private System.Windows.Forms.Label SquareLabel;

        private System.Windows.Forms.Button CrossingShapesButton;

        private System.Windows.Forms.Label label55;
        private System.Windows.Forms.Label label56;

        private System.Windows.Forms.ComboBox FirstShapeIntersectionComboBox;
        private System.Windows.Forms.ComboBox SecondShapeIntersectionComboBox;

        private System.Windows.Forms.Button DeleteShapeButton;

        private System.Windows.Forms.ComboBox DeleteShapeComboBox;

        private System.Windows.Forms.Label ShiftXlabel;
        private System.Windows.Forms.Label ShiftYlabel;
        private System.Windows.Forms.TextBox ShiftXTextBox;
        private System.Windows.Forms.TextBox ShiftYTextBox;
        private System.Windows.Forms.TextBox AngleRotateTextBox;
        private System.Windows.Forms.DomainUpDown AxisSymDomainUpDown;

        private System.Windows.Forms.Label ShiftVectorLabel;
        private System.Windows.Forms.Label AngleRotationLabel;
        private System.Windows.Forms.Label AxisSymmetryLabel;

        private System.Windows.Forms.Button MoveShapeButton;

        private System.Windows.Forms.ComboBox MoveComboBox;
        private System.Windows.Forms.ComboBox ShapesComboBox;

        private System.Windows.Forms.TextBox Point15YtextBox;
        private System.Windows.Forms.TextBox Point15XtextBox;
        private System.Windows.Forms.Label label37;
        private System.Windows.Forms.Label label38;
        private System.Windows.Forms.Label label39;
        private System.Windows.Forms.TextBox Point14YtextBox;
        private System.Windows.Forms.TextBox Point14XtextBox;
        private System.Windows.Forms.Label label40;
        private System.Windows.Forms.Label label41;
        private System.Windows.Forms.Label label42;
        private System.Windows.Forms.TextBox Point13YtextBox;
        private System.Windows.Forms.TextBox Point13XtextBox;
        private System.Windows.Forms.Label label43;
        private System.Windows.Forms.Label label44;
        private System.Windows.Forms.Label label45;
        private System.Windows.Forms.TextBox Point9YtextBox;
        private System.Windows.Forms.TextBox Point9XtextBox;
        private System.Windows.Forms.Label label46;
        private System.Windows.Forms.Label label47;
        private System.Windows.Forms.Label label48;
        private System.Windows.Forms.TextBox Point8YtextBox;
        private System.Windows.Forms.TextBox Point8XtextBox;
        private System.Windows.Forms.Label label49;
        private System.Windows.Forms.Label label50;
        private System.Windows.Forms.Label label51;
        private System.Windows.Forms.TextBox Point7YtextBox;
        private System.Windows.Forms.TextBox Point7XtextBox;
        private System.Windows.Forms.Label label52;
        private System.Windows.Forms.Label label53;
        private System.Windows.Forms.Label label54;

        private System.Windows.Forms.TextBox Point2YtextBox;
        private System.Windows.Forms.TextBox Point2XtextBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox Point3YtextBox;
        private System.Windows.Forms.TextBox Point3XtextBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox Point6YtextBox;
        private System.Windows.Forms.TextBox Point6XtextBox;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.TextBox Point5YtextBox;
        private System.Windows.Forms.TextBox Point5XtextBox;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.TextBox Point4YtextBox;
        private System.Windows.Forms.TextBox Point4XtextBox;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.TextBox Point12YtextBox;
        private System.Windows.Forms.TextBox Point12XtextBox;
        private System.Windows.Forms.Label label19;
        private System.Windows.Forms.Label label20;
        private System.Windows.Forms.Label label21;
        private System.Windows.Forms.TextBox Point11YtextBox;
        private System.Windows.Forms.TextBox Point11XtextBox;
        private System.Windows.Forms.Label label22;
        private System.Windows.Forms.Label label23;
        private System.Windows.Forms.Label label24;
        private System.Windows.Forms.TextBox Point10YtextBox;
        private System.Windows.Forms.TextBox Point10XtextBox;
        private System.Windows.Forms.Label label25;
        private System.Windows.Forms.Label label26;
        private System.Windows.Forms.Label label27;
        private System.Windows.Forms.TextBox Point18YtextBox;
        private System.Windows.Forms.TextBox Point18XtextBox;
        private System.Windows.Forms.Label label28;
        private System.Windows.Forms.Label label29;
        private System.Windows.Forms.Label label30;
        private System.Windows.Forms.TextBox Point17YtextBox;
        private System.Windows.Forms.TextBox Point17XtextBox;
        private System.Windows.Forms.Label label31;
        private System.Windows.Forms.Label label32;
        private System.Windows.Forms.Label label33;
        private System.Windows.Forms.TextBox Point16YtextBox;
        private System.Windows.Forms.TextBox Point16XtextBox;
        private System.Windows.Forms.Label label34;
        private System.Windows.Forms.Label label35;
        private System.Windows.Forms.Label label36;

        private System.Windows.Forms.TextBox Point1XtextBox;
        private System.Windows.Forms.TextBox Point1YtextBox;

        private System.Windows.Forms.Label label3;

        private System.Windows.Forms.Label label2;

        private System.Windows.Forms.Label label1;

        private System.Windows.Forms.TextBox RadiusTextBox;

        private System.Windows.Forms.Label RadiusLabel;

        private System.Windows.Forms.NumericUpDown CountPointsNumericUpDown;

        private System.Windows.Forms.ComboBox ShapeSelectionComboBox;

        private System.Windows.Forms.TextBox PerimeterSquareTextBox;

        private System.Windows.Forms.Label PerimeterLabel;

        private System.Windows.Forms.PictureBox CanvasPictureBox;

        private System.Windows.Forms.Button CleanButton;
        private System.Windows.Forms.Button PerimeterButton;
        private System.Windows.Forms.Button SquareButton;

        private System.Windows.Forms.TabPage tabPageDeleteShape;
        private System.Windows.Forms.TabPage tabPageIntersectionShapes;

        private System.Windows.Forms.TabPage tabPageMoveShape;

        private System.Windows.Forms.Button AddShapeButton;

        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPageMainForm;
        private System.Windows.Forms.TabPage tabPageAddShape;

        #endregion
    }
}