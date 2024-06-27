using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Coin
    {
        public Physics physics;
        public Image sprite;

        public Coin(PointF pos)
        {
            sprite = Image.FromFile("coin.png");
            physics = new Physics(pos, new Size(20, 20));
        }

        public void DrawSprite(Graphics g)
        {
            g.DrawImage(sprite, physics.transform.position.X, physics.transform.position.Y, physics.transform.size.Width, physics.transform.size.Height);
        }
    }
}