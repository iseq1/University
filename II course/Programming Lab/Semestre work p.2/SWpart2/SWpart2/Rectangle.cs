using System;
using System.Linq;

namespace SWpart2
{
    public class Rectangle : QGon
    {
        public Rectangle(Point2D[] p) : base(p)
        {
            if ((((p[1].x[1] - p[0].x[1]) / (p[1].x[0] - p[0].x[0])) ==
                 ((p[3].x[1] - p[2].x[1]) / (p[3].x[0] - p[2].x[0]))) &&
                (((p[2].x[1] - p[1].x[1]) / (p[2].x[0] - p[1].x[0])) ==
                 ((p[3].x[1] - p[0].x[1]) / (p[3].x[0] - p[0].x[0]))))
            {
                //проверяем, параллельны ли 2 стороны и равны диоганали
                if (new Segment(new Point2D(p[0].getX()), new Point2D(p[2].getX())).length() ==
                    new Segment(new Point2D(p[1].getX()), new Point2D(p[3].getX())).length())
                {
                    base.n = p.Length;
                    base.p = p;
                }
                else
                {
                    throw new Exception("This figure is a parallelogram, not a rectangle!");
                }
            }
            else{
                throw new Exception("This shape is not a rectangle!");
            }
                
        }

        public new double square()
        {
            return new Segment(p[0], p[1]).length() * new Segment(p[1], p[2]).length();
        }
        
        public override String ToString()
        {
            string str = "Rectangle: (";
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