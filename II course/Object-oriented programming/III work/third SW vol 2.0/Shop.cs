using System.Drawing.Drawing2D;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.IO;    
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace third_SW_vol_2._0
{
    


    public class Shop
    {
        //меняем тут всё, будет файл с идексом скина
        public string typesprite;
        
        public void InputTypeSprite() //read
        {
            StreamReader sr = new StreamReader("PlayerSpriteData.txt");
            typesprite = sr.ReadLine();
            sr.Close();
            Console.ReadLine();
            //MessageBox.Show(this.score + " - " +  this.cash);
        }

        public void OutputTypeSprite()
        {
            StreamWriter sw = new StreamWriter("PlayerSpriteData.txt");
            sw.WriteLine(Convert.ToString(typesprite));
            sw.Close();
        }


    }
}