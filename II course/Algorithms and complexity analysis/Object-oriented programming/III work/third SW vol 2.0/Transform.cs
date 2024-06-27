using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Transform
    {
        public PointF position;
        public Size size;

        public Transform(PointF position, Size size)
        {
            this.position = position;
            this.size = size;
        }
    }
}