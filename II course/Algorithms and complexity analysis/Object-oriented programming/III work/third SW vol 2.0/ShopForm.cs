using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace third_SW_vol_2._0
{
    public partial class ShopForm : Form
    {
        public Shop shop = new Shop();
        public GameData gd = new GameData();

        public Dictionary<int, int> Unlocked = new Dictionary<int, int>()
        {
            [1] = 1,
            [2] = 0,
            [3] = 0,
            [4] = 0,
            [5] = 0,
            [6] = 0,
            [7] = 0,
            [8] = 0,
        };
        
        public ShopForm()
        {
            InitializeComponent();
            this.BackgroundImage = Image.FromFile("back.jpg");
            
            gd.InputCashData();
            label1.Text = "Gold: " + gd.cash ;
            
            
            PictureBox palyer1 = new PictureBox();
            palyer1.Image = Image.FromFile("player1.png");
            palyer1.SizeMode = PictureBoxSizeMode.StretchImage;
            palyer1.Size = new Size(100,100);
            palyer1.Location = new Point(22, 65);
            Controls.Add(palyer1);
            
            PictureBox player2 = new PictureBox();
            player2.Image = Image.FromFile("player2.png");
            player2.SizeMode = PictureBoxSizeMode.StretchImage;
            player2.Size = new Size(100,100);
            player2.Location = new Point(180, 65);
            Controls.Add(player2);
            
            PictureBox player3 = new PictureBox();
            player3.Image = Image.FromFile("player3.png");
            player3.SizeMode = PictureBoxSizeMode.StretchImage;
            player3.Size = new Size(100,100);
            player3.Location = new Point(345, 65);
            Controls.Add(player3);
            
            PictureBox player4 = new PictureBox();
            player4.Image = Image.FromFile("player4.png");
            player4.SizeMode = PictureBoxSizeMode.StretchImage;
            player4.Size = new Size(100,100);
            player4.Location = new Point(510, 65);
            Controls.Add(player4);
            
            PictureBox player5 = new PictureBox();
            player5.Image = Image.FromFile("player5.png");
            player5.SizeMode = PictureBoxSizeMode.StretchImage;
            player5.Size = new Size(100,100);
            player5.Location = new Point(22, 300);
            Controls.Add(player5);
            
            PictureBox player6 = new PictureBox();
            player6.Image = Image.FromFile("player6.png");
            player6.SizeMode = PictureBoxSizeMode.StretchImage;
            player6.Size = new Size(100,100);
            player6.Location = new Point(180, 300);
            Controls.Add(player6);
            
            PictureBox player7 = new PictureBox();
            player7.Image = Image.FromFile("player7.png");
            player7.SizeMode = PictureBoxSizeMode.StretchImage;
            player7.Size = new Size(100,100);
            player7.Location = new Point(345, 300);
            Controls.Add(player7);
            
            PictureBox player8 = new PictureBox();
            player8.Image = Image.FromFile("player8.png");
            player8.SizeMode = PictureBoxSizeMode.StretchImage;
            player8.Size = new Size(100,100);
            player8.Location = new Point(510, 300);
            Controls.Add(player8);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form form1 = Application.OpenForms[0];
            form1.Show();
            Close();
        }


        private void BuyBttn1_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(1);
                Unlocked.Add(1,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void SelectBttn1_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(1, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(1);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(2);
                Unlocked.Add(2,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void SelectBttn2_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(2, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(2);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button7_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(3);
                Unlocked.Add(3,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void SelectBttn3_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(3, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(3);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }      
        }

        private void button9_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(4);
                Unlocked.Add(4,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void SelectBttn4_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(4, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(4);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button12_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(5);
                Unlocked.Add(5,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void button11_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(5, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(5);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(6);
                Unlocked.Add(6,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void button8_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(6, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(6);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(7);
                Unlocked.Add(7,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(7, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(7);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            gd.InputCashData();
            if (Convert.ToInt32(gd.cash)-500>=0)
            {
                gd.cash = Convert.ToString(Convert.ToInt32(gd.cash) - 500);
                gd.OutputCashData();
                Unlocked.Remove(8);
                Unlocked.Add(8,1);
                label1.Text = "Gold: " + gd.cash ;
                MessageBox.Show("Вы приобрели новый образ!");
            }
            else
            {
                MessageBox.Show("Не достаточно монет!");
            }
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            int value;
            if (Unlocked.TryGetValue(8, out value))
            {
                if (value == 1)
                {
                    shop.InputTypeSprite();
                    shop.typesprite = Convert.ToString(8);
                    MessageBox.Show("Вы выбрали новый образ!");
                    shop.OutputTypeSprite();
                }
                else
                {
                    MessageBox.Show("Образ ещё не куплен!");
                }
            }
        }
    }
}