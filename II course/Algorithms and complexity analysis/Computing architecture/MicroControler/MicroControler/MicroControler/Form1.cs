using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;

namespace MicroControler
{
    public partial class Form1 : Form
    {

        public string s1, s2;
        public char c0;
        public Form1()
        {
            InitializeComponent();
            
        }

        private void buttonUpdatePorts_Click(object sender, EventArgs e)
        {
            string[] ports = SerialPort.GetPortNames();
            comboBoxPorts.Text = "";
            comboBoxPorts.Items.Clear();
            if (ports.Length != 0)
            {
                comboBoxPorts.Items.AddRange(ports);
                comboBoxPorts.SelectedIndex = 0;
            }
        }

        private void buttonConection1_Click(object sender, EventArgs e)
        {
            if (buttonConection1.Text == "Подключиться")
            {
                try
                {
                    serialPort1.PortName = comboBoxPorts.Text;
                    serialPort1.Open();
                    s1 = "#020" + '\r';
                    serialPort1.Write(s1);
                    s2 = "";
                    while ((c0 = (char)serialPort1.ReadChar()) != '\r')
                    {
                        s2 += c0;
                    }
                    label1.Text = s2;
                    
                    double convertToDouble;
                    String[] hexArray=label1.Text.Split('.');              
                    // Если у числа есть и дробная и целая часть, то длинна массива будет равна 2.
                    if(hexArray.Length==2)
                    {
                        // Конвертируем в 10тичную.
                        String tmp=Convert.ToInt32(hexArray[0], 16).ToString() + ","  + Convert.ToInt32(hexArray[1], 16).ToString();               
                        // Преобразуем строку Double.
                        convertToDouble=Convert.ToDouble(tmp);
                    }
                    else
                    {
                        // Иначе, если разделителя не было и число целое то просто конвертируем число.
                        String tmp=Convert.ToInt32(hexArray[0], 16).ToString();             
                        convertToDouble=Convert.ToDouble(tmp);                  
                    }

                    label1.Text = Convert.ToString(convertToDouble * (int)numericUpDown2.Value + (int)numericUpDown1.Value);
                    
                    comboBoxPorts.Enabled = false;
                    buttonConection1.Text = "Отключиться";
                }
                catch
                {
                    MessageBox.Show("Ошибка подключения!!!");
                }
            }
            else if (buttonConection1.Text == "Отключиться")
            {
                //Прерываем подключение
                buttonConection1.Text = "Подключиться";
                comboBoxPorts.Enabled = true;
            }
        }

        private void buttonConection2_Click(object sender, EventArgs e)
        {
            if (buttonConection2.Text == "Подключиться 2")
            {
                try
                {
                    serialPort1.PortName = comboBoxPorts.Text;
                    serialPort1.Open();
                    s1 = "#021" + '\r';
                    serialPort1.Write(s1);
                    s2 = "";
                    while ((c0 = (char)serialPort1.ReadChar()) != '\r')
                    {
                        s2 += c0;
                    }
                    label2.Text = s2;

                    double convertToDouble;
                    String[] hexArray=label2.Text.Split('.');              
                    // Если у числа есть и дробная и целая часть, то длинна массива будет равна 2.
                    if(hexArray.Length==2)
                    {
                        // Конвертируем в 10тичную.
                        String tmp=Convert.ToInt32(hexArray[0], 16).ToString() + ","  + Convert.ToInt32(hexArray[1], 16).ToString();               
                        // Преобразуем строку Double.
                        convertToDouble=Convert.ToDouble(tmp);
                    }
                    else
                    {
                        // Иначе, если разделителя не было и число целое то просто конвертируем число.
                        String tmp=Convert.ToInt32(hexArray[0], 16).ToString();             
                        convertToDouble=Convert.ToDouble(tmp);                  
                    }

                    label2.Text = Convert.ToString(convertToDouble * (int)numericUpDown2.Value + (int)numericUpDown1.Value);
                    
                    
                    comboBoxPorts.Enabled = false;
                    buttonConection2.Text = "Отключиться 2";
                }
                catch
                {
                    MessageBox.Show("Ошибка подключения!!!");
                }
            }
            else if (buttonConection2.Text == "Отключиться 2")
            {
                //Прерываем подключение
                buttonConection2.Text = "Подключиться 2";
                comboBoxPorts.Enabled = true;
            }
        }

        private void label3_Click(object sender, EventArgs e)
        {
            throw new System.NotImplementedException();
        }
    }
}