using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Platform
    {
        Image sprite;
        public Transform transform;
        public int sizeX;
        public int sizeY;
        public bool isTouchedByPlayer;

        public Platform(PointF pos)
        {
            sprite = Image.FromFile("platform.png");
            sizeX = 60;
            sizeY = 25;
            transform = new Transform(pos, new Size(sizeX, sizeY));
            isTouchedByPlayer = false;
        }

        public void DrawSprite(Graphics g)
        {
            g.DrawImage(sprite, transform.position.X, transform.position.Y, transform.size.Width, transform.size.Height);
        }

    }
}