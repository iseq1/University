using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Security;
using System.Windows.Forms;

namespace first_SW
{
    public partial class OpenFileDialogForm : Form
    {
        private int data_from_form1;
        private Button selectButton;
        private Button accesButton;
        private OpenFileDialog openFileDialog1;
        public TextBox textBox1;
        public OpenFileDialogForm(int data)
        {
            InitializeComponent();
            data_from_form1 = data;
            openFileDialog1 = new OpenFileDialog();
            selectButton = new Button
            {
                Size = new Size(100, 20),
                Location = new Point(15, 15),
                Text = "Select file"
            };
            accesButton = new Button
            {
                Size = new Size(100, 20),
                Location = new Point(215, 15),
                Text = "Acces"
            };
            selectButton.Click += new EventHandler(SelectButton_Click);
            accesButton.Click += new EventHandler(AccesButton_Click);
            textBox1 = new TextBox
            {
                Size = new Size(300, 300),
                Location = new Point(15, 40),
                Multiline = true,
                ScrollBars = ScrollBars.Vertical
            };
            ClientSize = new Size(330, 360);
            Controls.Add(selectButton);
            Controls.Add(accesButton);
            Controls.Add(textBox1);
        }
        private void SetText(string text)
        {
            textBox1.Text = text;
        }
        private void AccesButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        private void SelectButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    var sr = new StreamReader(openFileDialog1.FileName);
                    SetText(sr.ReadToEnd());
                } 
                catch (SecurityException ex)
                {
                    MessageBox.Show($"Security error.\n\nError message: {ex.Message}\n\n" +
                                    $"Details:\n\n{ex.StackTrace}");
                }
            }
        }
    }
}