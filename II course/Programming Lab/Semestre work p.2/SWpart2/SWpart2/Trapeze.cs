using System;
using System.Linq;
using System.Runtime.InteropServices;

namespace SWpart2
{
    public class Trapeze : QGon
    {
        public Trapeze(Point2D[] p) : base(p)
        {
            bool k1 = false;
            bool k2 = false;
            if ((p[1].x[1] - p[0].x[1]) / (p[1].x[0] - p[0].x[0]) == (p[3].x[1] - p[2].x[1]) / (p[3].x[0] - p[2].x[0]))
            {
                k1 = true;
            }
            if ((p[2].x[1] - p[1].x[1]) / (p[2].x[0] - p[1].x[0]) == (p[3].x[1] - p[0].x[1]) / (p[3].x[0] - p[0].x[0]))
            {
                k2 = true;
            }
            
            if ((k1 && !k2) || (!k1 && k2))
            {
                //если 2 стороны параллельны а две другие нет
                base.n = p.Length;
                base.p = p;
            }
            else
            {
                throw new ArgumentException("This shape is not a trapze!");
            }
        }
        

        public new double square()
        {
            double a, b, c, d;
            if (((p[1].x[1] - p[0].x[1]) / (p[1].x[0] - p[0].x[0])) ==
                ((p[3].x[1] - p[2].x[1]) / (p[3].x[0] - p[2].x[0])))
            {
                // Проверяем паралельность сторон чтобы правильно взять a и d как основания
                d = new Segment(p[0], p[1]).length();
                b = new Segment(p[1], p[2]).length();
                a = new Segment(p[2], p[3]).length();
                c = new Segment(p[3], p[0]).length();
            }
            else
            {
                c =  new Segment(p[0], p[1]).length();
                d = new Segment(p[1], p[2]).length();
                b = new Segment(p[2], p[3]).length();
                a = new Segment(p[3], p[0]).length();
            }
            // Вычисление высоты трапеции
            double h = Math.Sqrt(Math.Pow(c,2) - ((Math.Pow(a-d,2) + Math.Pow(c,2) - Math.Pow(b,2)))/Math.Pow(2*(a-d),2));
            // Вычисление площади трапеции
            return (a + d) * h / 2;
            
            
            
            //работает только если (p[0]; p[1]) и (p[2]; p[3]) = боковые линии
            //double[] forH = {p[1].x[0], p[0].x[1] };
            //double h = Math.Sqrt(Math.Pow(new Segment(p[0],p[1]).length(),2) - Math.Pow(new Segment(p[0], new Point2D(forH)).length(),2));
            //return ((new Segment(p[1], p[2]).length() + new Segment(p[0], p[3]).length())*h)/2;
        }
        
        public override String ToString()
        {
            string str = "Trapeze: (";
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