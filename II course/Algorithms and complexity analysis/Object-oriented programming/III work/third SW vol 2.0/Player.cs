using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    
    public class Player
    {
        public Physics physics;
        public Image sprite;
        public Shop shop = new Shop();
        

        public Player()
        {
            shop.InputTypeSprite();
            int typeSprite = Convert.ToInt32(shop.typesprite);
            switch (typeSprite)
            {
                case 1:
                    sprite = Image.FromFile("player1.png");
                    break;
                case 2:
                    sprite = Image.FromFile("player2.png");
                    break;
                case 3:
                    sprite = Image.FromFile("player3.png");
                    break;
                case 4:
                    sprite = Image.FromFile("player4.png");
                    break;
                case 5:
                    sprite = Image.FromFile("player5.png");
                    break;
                case 6:
                    sprite = Image.FromFile("player6.png");
                    break;
                case 7:
                    sprite = Image.FromFile("player7.png");
                    break;
                case 8:
                    sprite = Image.FromFile("player8.png");
                    break;
            }
            physics = new Physics(new PointF(100, 350), new Size(40, 40));
        }

        public void DrawSprite(Graphics g)
        {
            g.DrawImage(sprite, physics.transform.position.X, physics.transform.position.Y, physics.transform.size.Width, physics.transform.size.Height);
        }
    }
}