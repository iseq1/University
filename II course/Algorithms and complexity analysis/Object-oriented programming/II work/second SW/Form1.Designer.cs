namespace second_SW
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
            System.Windows.Forms.Label label1;
            System.Windows.Forms.Button button1;
            System.Windows.Forms.Button button2;
            System.Windows.Forms.Label labelPassword;
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.labelUsername = new System.Windows.Forms.Label();
            this.textBoxUsername = new System.Windows.Forms.TextBox();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.buttonLogin = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            label1 = new System.Windows.Forms.Label();
            button1 = new System.Windows.Forms.Button();
            button2 = new System.Windows.Forms.Button();
            labelPassword = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            label1.CausesValidation = false;
            label1.Enabled = false;
            label1.Location = new System.Drawing.Point(550, 34);
            label1.Name = "label1";
            label1.Size = new System.Drawing.Size(32, 11);
            label1.TabIndex = 0;
            label1.Text = "Database of members";
            label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            label1.Visible = false;
            // 
            // button1
            // 
            button1.CausesValidation = false;
            button1.Enabled = false;
            button1.Location = new System.Drawing.Point(530, 12);
            button1.Name = "button1";
            button1.Size = new System.Drawing.Size(10, 23);
            button1.TabIndex = 12;
            button1.Visible = false;
            // 
            // button2
            // 
            button2.CausesValidation = false;
            button2.Enabled = false;
            button2.Location = new System.Drawing.Point(591, 57);
            button2.Name = "button2";
            button2.Size = new System.Drawing.Size(23, 12);
            button2.TabIndex = 11;
            button2.Visible = false;
            // 
            // labelPassword
            // 
            labelPassword.CausesValidation = false;
            labelPassword.Enabled = false;
            labelPassword.Location = new System.Drawing.Point(591, 34);
            labelPassword.Name = "labelPassword";
            labelPassword.Size = new System.Drawing.Size(23, 11);
            labelPassword.TabIndex = 4;
            labelPassword.Text = "Password";
            labelPassword.Visible = false;
            // 
            // labelUsername
            // 
            this.labelUsername.BackColor = System.Drawing.Color.Transparent;
            this.labelUsername.Font = new System.Drawing.Font("MV Boli", 16.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelUsername.ForeColor = System.Drawing.Color.SaddleBrown;
            this.labelUsername.Location = new System.Drawing.Point(273, 233);
            this.labelUsername.Name = "labelUsername";
            this.labelUsername.Size = new System.Drawing.Size(167, 43);
            this.labelUsername.TabIndex = 3;
            this.labelUsername.Text = "Username";
            this.labelUsername.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // textBoxUsername
            // 
            this.textBoxUsername.Location = new System.Drawing.Point(446, 248);
            this.textBoxUsername.Name = "textBoxUsername";
            this.textBoxUsername.Size = new System.Drawing.Size(136, 22);
            this.textBoxUsername.TabIndex = 5;
            // 
            // textBoxPassword
            // 
            this.textBoxPassword.Location = new System.Drawing.Point(446, 300);
            this.textBoxPassword.Name = "textBoxPassword";
            this.textBoxPassword.PasswordChar = '●';
            this.textBoxPassword.Size = new System.Drawing.Size(136, 22);
            this.textBoxPassword.TabIndex = 6;
            // 
            // buttonLogin
            // 
            this.buttonLogin.BackColor = System.Drawing.SystemColors.Control;
            this.buttonLogin.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("buttonLogin.BackgroundImage")));
            this.buttonLogin.Font = new System.Drawing.Font("MV Boli", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonLogin.ForeColor = System.Drawing.Color.SaddleBrown;
            this.buttonLogin.Location = new System.Drawing.Point(465, 343);
            this.buttonLogin.Name = "buttonLogin";
            this.buttonLogin.Size = new System.Drawing.Size(117, 38);
            this.buttonLogin.TabIndex = 7;
            this.buttonLogin.Text = "✅ Login";
            this.buttonLogin.UseVisualStyleBackColor = false;
            this.buttonLogin.Click += new System.EventHandler(this.buttonLogin_Click);
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Font = new System.Drawing.Font("MV Boli", 16.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.Color.SaddleBrown;
            this.label2.Location = new System.Drawing.Point(273, 285);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(167, 43);
            this.label2.TabIndex = 10;
            this.label2.Text = "Password";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label3
            // 
            this.label3.BackColor = System.Drawing.Color.Transparent;
            this.label3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label3.Font = new System.Drawing.Font("MV Boli", 22.2F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.ForeColor = System.Drawing.Color.SaddleBrown;
            this.label3.Location = new System.Drawing.Point(12, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(602, 114);
            this.label3.TabIndex = 13;
            this.label3.Text = "Healthy Fruit Nutrition\r\nDatabase";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(626, 417);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.buttonLogin);
            this.Controls.Add(this.textBoxPassword);
            this.Controls.Add(this.textBoxUsername);
            this.Controls.Add(labelPassword);
            this.Controls.Add(this.labelUsername);
            this.Controls.Add(button2);
            this.Controls.Add(button1);
            this.Controls.Add(label1);
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Main_menu";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Label label3;

        private System.Windows.Forms.Label label2;

        private System.Windows.Forms.Button buttonLogin;

        private System.Windows.Forms.TextBox textBoxPassword;

        private System.Windows.Forms.TextBox textBoxUsername;

        private System.Windows.Forms.Label labelUsername;

        #endregion
    }
}