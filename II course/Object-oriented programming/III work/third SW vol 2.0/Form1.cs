using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

// 2D-игра
// 1. WPF/WF
// 2. Анимации:
//      а) векторные
//      б) покадровые
// 3. События
// 4. Управление (и/или):
//      а) мышь
//      б) клавиатура
// 5. Саунд сопровождение
// 6. Физика
// 7. Динамическое создание элементов


//формы: меню, настройки, форма с игрой, +форма с магазином?
//чтобы при выходе за пределы экране прходил с другой стороны



namespace third_SW_vol_2._0
{
  public partial class Form1 : Form
  {
      public Form1()
        {
        InitializeComponent();
        }
      private void button1_Click(object sender, EventArgs e)
      {
          GameForm gf = new GameForm();
          gf.Show(); 
          Hide();
      }

      private void button2_Click(object sender, EventArgs e)
      {
          ShopForm sf = new ShopForm();
          sf.Show();
          Hide();
      }

      private void button3_Click(object sender, EventArgs e)
      {
          Application.Exit();
      }
  }
}
