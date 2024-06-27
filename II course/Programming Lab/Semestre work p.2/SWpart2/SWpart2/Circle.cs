using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace SWpart2
{
    public class Circle : IShape
    {
        private Point2D p;
        private double r;

        public Circle(Point2D p, double r)
        {
            if (r > 0) 
            {
                this.p = p;
                this.r = r;
            }
            else
            {
                throw new Exception("Радиус более нуля!");
            }
        }

        public Point2D getP()
        {
            return p;
        }

        public void setP(Point2D p)
        {
            this.p = p;
        }

        public double getR()
        {
            return r;
        }

        public void setR(double r)
        {
            this.r = r;
        }

        public double square()
        {
            return Math.PI * Math.Pow(r, 2);
        }

        public double length()
        {
            return Math.PI * 2 * r;
        }

        public IShape shift(Point2D a)
        {
            return new Circle(new Point2D(p.add(a).x),r);
        }

        public IShape rot(double phi)
        {
            return new Circle(new Point2D(p.rot(phi).x), r);
        }

        public IShape symAxis(int i)
        {
            return new Circle(new Point2D(p.symAxis(i).x), r);
        }

        public bool cross(IShape i)
        {
            bool temp = false;
            if (i is Segment)
            {
                Segment segment = (Segment)i;
                temp = segment.cross(new Circle(getP(),getR()));
            }
            else if (i is Polyline)
            {
                Polyline polyline = (Polyline)i;
                temp = polyline.cross(new Circle(getP(),getR()));
            }
            else if (i is NGon)
            {
                NGon ngon = (NGon)i;
                temp = ngon.cross(new Circle(getP(),getR()));
            }
            else if (i is Circle)
            {
                Circle otherCircle = (Circle)i;
                double DistanceBetweenCenters = new Segment(getP(),otherCircle.getP()).length();
                if (getR() + otherCircle.getR() > DistanceBetweenCenters && 
                    getR() + DistanceBetweenCenters > otherCircle.getR() && 
                    DistanceBetweenCenters + otherCircle.getR() > getR())
                {
                    //Пересекающиемя окружности - Окружности ω1 и ω2 пересекаются тогда и только тогда, когда числа R1, R2, d
                    //являются длинами сторон некоторого треугольника, т. е. удовлетворяют всем неравенствам треугольника:
                    temp = true;
                }

                if (getR() + otherCircle.getR() == DistanceBetweenCenters ||
                    Math.Abs(getR()-otherCircle.getR()) == DistanceBetweenCenters)
                {
                    //Касающиеся окружности - Окружности ω1и ω2 касаются внешним образом,
                    //когда R1+R2=d, внутренним образом – когда |R1−R2|=d.
                    temp = true;
                }
                
                if (getR() + otherCircle.getR() < DistanceBetweenCenters ||
                    Math.Min(getR(), otherCircle.getR()) + DistanceBetweenCenters < Math.Max(getR(),otherCircle.getR()))
                {
                    //Непересекающиеся окружности - Окружность ω1и ω2расположены вне друг друга тогда и только тогда,
                    //когда R1+R2<d. Окружность ω1 лежит внутри ω2 тогда и только тогда, когда R1+d<R2.
                    temp = false;
                }
            }
            else
            {
                throw new ArgumentException("Invalid type of object.");
            }
            return temp;  
        }
        
        public override string ToString()
        {
            double[] centerPoints = { p.x[0], p.x[1] };
            string[] centerPointsStrings = Array.ConvertAll(centerPoints, d => d.ToString());
            string center = string.Join("; ", centerPointsStrings);
            return $"Circle: (center=[{center}], radius={r})";
        }
        
        /*
        public override String ToString()
        {
            string center = string.Join("; ", (string[])p.x.Select(d => d.ToString()));
            return string.Format("Circle: (center=[{0}], radius={1})", center, Convert.ToString(r));
        } 
        */
        
    }
}