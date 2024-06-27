using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;


/*
    0. БД любая
    1. Получить список таблицу из БД
    2. Получить структуру таблицы
    3. Добавить запись - Insert
       Удалить запись - Delete
       Изменить запись - Update 
*/



/*
 Form1 - Application.OpenForms[0]
 Actions Menu - Application.OpenForms[1]
 View database - 
 Edit Database - 
 
 */



namespace second_SW
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
           
        }
        private void AllowAccess()
        {
            string username = "fruit";
            string password = "123";
            if (username != textBoxUsername.Text || password != textBoxPassword.Text)
            {
                MessageBox.Show("Wrong login or password! \n         Please, retry again");
            }
            else
            {
                this.Hide();
                MainFormDB MFDB = new MainFormDB();
                MFDB.Show();
            }
        }
        private void buttonLogin_Click(object sender, EventArgs e)
        {
            AllowAccess();
        }
        
    }
}