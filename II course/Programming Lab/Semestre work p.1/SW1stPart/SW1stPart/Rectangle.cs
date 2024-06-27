using System;

namespace SW1stPart
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
                    throw new AggregateException("Данная фигура является параллелограмом, а не прямоугольником");
                }
            }
            else{
                    throw new AggregateException("Данная фигура не является прямоугольником");
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
                str += string.Format("point({0})=[{1}], ", string.Join(",", i+1), string.Join("; ", p[i].x));
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }
    }
}