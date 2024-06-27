using System;
using System.Linq;

namespace SWpart2
{
    public class QGon : NGon
    {
        public QGon(Point2D[] p) : base(p)
        {
            base.n = p.Length;
            base.p = p;
        }

        public new double square()
        {
            //по координатам
            return Math.Abs((p[0].x[0] - p[1].x[0])*(p[0].x[1] + p[1].x[1]) + 
                            (p[1].x[0] - p[2].x[0])*(p[1].x[1] + p[2].x[1]) +
                            (p[2].x[0] - p[3].x[0])*(p[2].x[1] + p[3].x[1]) +
                            (p[3].x[0] - p[0].x[0])*(p[3].x[1] + p[0].x[1]))/2;
        }
        
        public override String ToString()
        {
            string str = "QGon: (";
            for (int i = 0; i < getN(); i++)
            {
                double[] centerPoints = { p[i].x[0], p[i].x[1] };
                string[] centerPointsStrings = Array.ConvertAll(centerPoints, d => d.ToString());
                string center = string.Join("; ", centerPointsStrings);
                str += string.Format("point({0})=[{1}], ",  Convert.ToString(i+1), center);
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }
    }
}