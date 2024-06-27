using System;

namespace SW1stPart
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
                str += string.Format("point({0})=[{1}], ", string.Join(",", i+1), string.Join("; ", p[i].x));
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }
    }
}