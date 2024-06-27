using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Bullet
    {
        public Physics physics;
        public Image sprite;

        public Bullet(PointF pos)
        {
            sprite = Image.FromFile("bullet.png");;
            physics = new Physics(pos, new Size(15, 15));
        }

        public void MoveUp()
        {
            physics.transform.position.Y -= 15;
        }

        public void DrawSprite(Graphics g)
        {
            g.DrawImage(sprite, physics.transform.position.X, physics.transform.position.Y, physics.transform.size.Width, physics.transform.size.Height);
        }
    }
}