using System;
using System.Linq;

namespace SWpart2
{
    public class NGon : IShape, IPolyPoint
    {
        protected internal int n;
        protected internal Point2D[] p;

        public NGon(Point2D[] p)
        {
            n = p.Length;
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
            throw new ArgumentException("Индекс за пределами массива.");
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

        public double square()
        {
            // формула гаусса
            double square = 0;
            for (int i = 0; i < getN(); i++)
            {
                if (i<getN()-1)
                {
                    square += (p[i + 1].x[0] - p[i].x[0]) * (p[i].x[1] + p[i+1].x[1]);
                }
                else
                {
                    square += (p[0].x[0] - p[i].x[0]) * (p[i].x[1] + p[0].x[1]);
                }
            }
            return square / 2;
        }

        public double length()
        {
            double len = new Polyline(p).length();
            len += new Segment(p[getN() - 1], p[0]).length();
            return len;
        }

        public IShape shift(Point2D a)
        {
            var temp = new Polyline(p).shift(a);
            return new NGon(((Polyline)temp).getP());
        }

        public IShape rot(double phi)
        {
            var temp = new Polyline(p).rot(phi);
            return new NGon(((Polyline)temp).getP());
        }

        public IShape symAxis(int i)
        {
            var temp = new Polyline(p).symAxis(i);
            return new NGon(((Polyline)temp).getP());
        }

        public bool cross(IShape i)
        {
            bool temp = false;
            if (i is Segment)
            {
                Segment segment = (Segment)i;
                temp = segment.cross(new NGon(getP()));
            }
            else if (i is Polyline)
            {
                Polyline polyline = (Polyline)i;
                temp = polyline.cross(new NGon(getP()));
            }
            else if (i is NGon)
            {
                NGon otherNGon = (NGon)i;
                bool flag = false;
                for (int j = 0; j < getN(); j++)
                {
                    if (j < getN() - 1)
                    {
                        Segment jSegment = new Segment(p[j], p[j + 1]);
                        flag = jSegment.cross(otherNGon);
                    }
                    if (j == getN() - 1)
                    {
                        Segment jSegment = new Segment(p[j], p[0]);
                        flag = jSegment.cross(otherNGon);
                    }

                    if (flag)
                    {
                        temp = true;
                    }
                }
            }
            else if (i is Circle)
            {
                Circle circle = (Circle)i;
                bool flag = false;
                for (int j = 0; j < getN(); j++)
                {
                    if (j < getN() - 1)
                    {
                        Segment jSegment = new Segment(p[j], p[j + 1]);
                        flag = jSegment.cross(circle);
                    }
                    if (j == getN() - 1)
                    {
                        Segment jSegment = new Segment(p[j], p[0]);
                        flag = jSegment.cross(circle);
                    }
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
        
        public override String ToString()
        {
            string str = "NGon: (";
            for (int i = 0; i < getN(); i++)
            {
                string point = string.Join("; ", p[i].x.Select(d => d.ToString()).ToArray());
                str += string.Format("point({0})=[{1}], ",  Convert.ToString(i+1), point);
            }
            str = str.Substring(0, str.Length - 2);
            str = str.Insert(str.Length, ")");
            return str;
        }
        
    }
}