using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Serialization;

namespace third_SW_vol_2._0
{
    public class GameData
    {
        public string score ;
        public string cash ;
        
        // создаешь текстовик с рекордом и мани
        // нужно метод для считывания из файла, записи в файл и метод для проверки рекорд ли это новый score и мб для мани тоже 

        public void InpuScoretData() //read
        {
            StreamReader sr = new StreamReader("PlayerScoreData.txt");
            score = sr.ReadLine();
            sr.Close();
            Console.ReadLine();
            //MessageBox.Show(this.score + " - " +  this.cash);
        }

        public void InputCashData() //read
        {
            
            StreamReader sr = new StreamReader("PlayerCashData.txt");
            cash = sr.ReadLine();
            sr.Close();
            Console.ReadLine();
            //MessageBox.Show(this.score + " - " +  this.cash);
        }
        
        public void OutputCashData() //write
        {
            
            if (PlatformController.money >= 100)
            {
                int temp = Convert.ToInt32(cash);
                temp = temp - (PlatformController.money-100) + PlatformController.money;
                StreamWriter sw = new StreamWriter("PlayerCashData.txt");
                sw.WriteLine(Convert.ToString(temp));
                sw.Close();
            }
            else if (PlatformController.money == 0)
            {
                StreamWriter sw = new StreamWriter("PlayerCashData.txt");
                sw.WriteLine(cash);
                sw.Close();
            }
        }
        
        public void OutputScoreData() //write
        {
            if (PlatformController.score > Convert.ToInt32(score))
            {
                StreamWriter sw = new StreamWriter("PlayerScoreData.txt");
                sw.WriteLine(Convert.ToString(PlatformController.score));
                sw.Close();
            }
            else
            {
                StreamWriter sw = new StreamWriter("PlayerScoreData.txt");
                sw.WriteLine(score);
                sw.Close();
            }
        }

        
        
    }
    
    
}