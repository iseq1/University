using System;
using System.Data;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace second_SW
{
    public partial class MainFormDB : Form
    {
        
        public MainFormDB()
        {
            InitializeComponent();
            label3.SendToBack();
        }
        static string connetStr = "server=localhost;user=root;database=people;password=123456;";
        private void buttonSave_Click(object sender, EventArgs e)
        {
            try
            {
                string Query = "INSERT INTO people.fruit VALUES ('" 
                               + this.textBoxFruitID.Text + "','" 
                               + this.textBoxName.Text + "','" 
                               + this.textBoxWeight.Text + "','" 
                               + this.comboBoxClassification.Text + "','" 
                               + this.textBoxCountry.Text + "');";
                MySqlConnection MyConnection = new MySqlConnection(connetStr);
                MySqlCommand MyCommand = new MySqlCommand(Query, MyConnection);
                MySqlDataReader MyReader;
                MyConnection.Open();
                MyReader = MyCommand.ExecuteReader();
                MessageBox.Show("Save Data");
                while (MyReader.Read())
                {
                }
                MyConnection.Close();
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void buttonUpdate_Click(object sender, EventArgs e)
        {
            try
            {
                string Query = "UPDATE people.fruit SET idfruit='" + this.textBoxFruitID.Text 
                                                                   + "', name='" + this.textBoxName.Text 
                                                                   + "', weight='" + this.textBoxWeight.Text 
                                                                   + "', classification='" + this.comboBoxClassification.Text 
                                                                   + "', country='" + textBoxCountry.Text 
                                                                   + "' WHERE idfruit='" + this.textBoxFruitID.Text + "';";
                MySqlConnection MyConnection = new MySqlConnection(connetStr);
                MySqlCommand MyCommand = new MySqlCommand(Query, MyConnection);
                MySqlDataReader MyReader;
                MyConnection.Open();
                MyReader = MyCommand.ExecuteReader();
                MessageBox.Show("Data Update");
                while (MyReader.Read())
                {
                }
                MyConnection.Close();
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            try
            {
                string Query = "DELETE FROM people.fruit WHERE idfruit='" + this.textBoxFruitID.Text + "';";
                MySqlConnection MyConnection = new MySqlConnection(connetStr);
                MySqlCommand MyCommand = new MySqlCommand(Query, MyConnection);
                MySqlDataReader MyReader;
                MyConnection.Open();
                MyReader = MyCommand.ExecuteReader();
                MessageBox.Show("Data Deleted");
                while (MyReader.Read())
                {
                }
                MyConnection.Close();
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void buttonShow_Click(object sender, EventArgs e)
        {
            try
            {
                string Query = "SELECT * FROM people.fruit;";
                MySqlConnection MyConnection = new MySqlConnection(connetStr);
                MySqlCommand MyCommand = new MySqlCommand(Query, MyConnection);
                MySqlDataAdapter MyAdapter = new MySqlDataAdapter();
                MyAdapter.SelectCommand = MyCommand;
                DataTable dataTable = new DataTable();
                MyAdapter.Fill(dataTable);
                dataGridView1.DataSource = dataTable;
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}