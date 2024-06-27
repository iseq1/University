using System;
using System.Linq;

namespace SWpart2
{
    public class TGon : NGon
    {
        public TGon(Point2D[] p) : base(p)
        {
            base.n = p.Length;
            base.p = p;
        }
        
        public new double square()
        {
            double semiPerimeter = new NGon(p).length()/2;
            return Math.Sqrt(semiPerimeter*
                             (semiPerimeter - (new Segment(p[0], p[1]).length()))*
                             (semiPerimeter - (new Segment(p[1], p[2]).length()))*
                             (semiPerimeter - (new Segment(p[2], p[0]).length())));
        }
        
        public override String ToString()
        {
            string str = "TGon: (";
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