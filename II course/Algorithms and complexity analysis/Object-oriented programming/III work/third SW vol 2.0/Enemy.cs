using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Enemy : Player
    {
        public Enemy(PointF pos, int type)
        {
            switch (type)
            {
                case 1:
                    sprite = Image.FromFile("enemy1.png");
                    physics = new Physics(pos, new Size(40, 40));
                    break;
                case 2:
                    sprite = Image.FromFile("enemy2.png");
                    physics = new Physics(pos, new Size(70, 50));
                    break;
                case 3:
                    sprite = Image.FromFile("enemy3.png");
                    physics = new Physics(pos, new Size(70, 60));
                    break;
                case 4:
                    sprite = Image.FromFile("enemy4.png");
                    physics = new Physics(pos, new Size(55, 45));
                    break;
                case 5:
                    sprite = Image.FromFile("enemy5.png");
                    physics = new Physics(pos, new Size(70, 60));
                    break;
            }
            
        }
    }
}