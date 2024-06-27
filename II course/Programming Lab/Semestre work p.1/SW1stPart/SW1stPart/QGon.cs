using System;

namespace SW1stPart
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
                str += string.Format("point({0})=[{1}], ", string.Join(",", i+1), string.Join("; ", p[i].x));
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }
    }
}