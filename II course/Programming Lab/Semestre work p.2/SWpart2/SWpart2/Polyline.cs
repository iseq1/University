using System;
using System.Linq;

namespace SWpart2
{
    public class Polyline : OpenFigure, IPolyPoint
    {
        private int n;
        private Point2D[] p;

        public Polyline(Point2D[] p)
        {
            this.n = p.Length;
            this.p = p;
        }

        public int getN()
        {
            return n;
        }

        public Point2D[] getP()
        {
            return p;
        }

        public Point2D getP(int i)
        {
            if ((i >= 0) && (i < p.Length)){
                return p[i];
            }
            else
            {
                throw new ArgumentException("Индекс за пределами массива.");
            }
        }

        public void setP(Point2D p, int i)
        {
            if ((i >= 0) && (i < this.p.Length))
            {
                this.p[i] = p;
            }
            else
            {
                throw new ArgumentException("Индекс за пределами массива.");
            }
        }

        public void setP(Point2D[] p)
        {
            this.p = p;
        }
        
        public override double length()
        {
            if (p.Length < 2)
            {
                return 0;
            }
            else
            {
                double length = 0;
                for (int i = 0; i < p.Length - 1; i++)
                {
                    length += new Segment(p[i], p[i + 1]).length();
                }
                return length;
            }
        }

        public override IShape shift(Point2D a)
        {
            //тут 2 способа: либо по точкам сдвигать(Point!=Point2D maybe error), либо по отрезкам(нужно запоминать лишь start)
            Point2D[] plshift = new Point2D[getN()];
            for (int i = 0; i < p.Length; i++)
            {
                plshift[i] = new Point2D(p[i].add(a).x);
            }
            return new Polyline(plshift);
        }

        public override IShape rot(double phi)
        {
            Point2D[] plshift = new Point2D[getN()];
            for (int i = 0; i < p.Length; i++)
            {
                plshift[i] = new Point2D(p[i].rot(phi).x);
            }
            return new Polyline(plshift);
        }

        public override IShape symAxis(int i)
        {
            Point2D[] newp = new Point2D[getN()];
            for (int j = 0; j < getN(); j++)
            {
                newp[j] = new Point2D(p[j].symAxis(i).x);
            }
            return new Polyline(newp);
        }

        public override bool cross(IShape i)
        {
            bool temp = false;
            if (i is Segment)
            {
                Segment segment = (Segment)i;
                temp = segment.cross(new Polyline(getP()));
            }
            else if (i is Polyline)
            {
                Polyline otherPolyline = (Polyline)i;
                bool flag;
                for (int j = 0; j < getN()-1; j++)
                {
                    Segment jSegment = new Segment(p[j], p[j + 1]);
                    flag = jSegment.cross(otherPolyline);
                    if (flag)
                    {
                        temp = true;
                    }
                }
            }
            else if (i is NGon)
            {
                NGon ngon = (NGon)i;
                bool flag;
                for (int j = 0; j < getN()-1; j++)
                {
                    Segment jSegment = new Segment(p[j], p[j + 1]);
                    flag = jSegment.cross(ngon);
                    if (flag)
                    {
                        temp = true;
                    }
                }
            }
            else if (i is Circle)
            {
                Circle circle = (Circle)i;
                bool flag;
                for (int j = 0; j < getN()-1; j++)
                {
                    Segment jSegment = new Segment(p[j], p[j + 1]);
                    flag = jSegment.cross(circle);
                    if (flag)
                    {
                        temp = true;
                    }
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
            string str = "Polyline: (";
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
        /*
        public override String ToString()
        {
            string str = "Polyline: (";
            for (int i = 0; i < getN(); i++)
            {
                string point = string.Join("; ", p[i].x.Select(d => d.ToString()).ToArray());
                str += string.Format("point({0})=[{1}], ",  Convert.ToString(i+1), point);
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }*/

    }
}