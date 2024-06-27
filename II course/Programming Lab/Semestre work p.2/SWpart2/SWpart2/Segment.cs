using System;
using System.IO;
using System.Linq;

namespace SWpart2
{
    public class Segment : OpenFigure
    {
        private Point2D start;
        private Point2D finish;

        public Segment(Point2D s, Point2D f)
        {
            start = s;
            finish = f;
        }

        public Point2D getStart()
        {
            return start;
        }

        public void setStart(Point2D a)
        {
            this.start = a;
        }

        public Point2D getFinish()
        {
            return finish;
        }

        public void setFinish(Point2D a)
        {
            this.finish = a;
        }

        public override double length()
        {
            // ((x_2 - x_1)^2 + (y_2 - y_1)^2)^(1/2)
            return Math.Sqrt(Math.Pow(finish.x[0] - start.x[0], 2) + Math.Pow(finish.x[1] - start.x[1], 2));
        }

        public override IShape shift(Point2D a)
        {
            return new Segment(new Point2D(start.add(a).x), new Point2D(finish.add(a).x));
        }
        
        public override IShape rot(double phi)
        {
            return new Segment(start.rot(phi), finish.rot(phi));;
        }
        
        public override IShape symAxis(int i)
        {
            return new Segment(new Point2D(start.symAxis(i).x), new Point2D(finish.symAxis(i).x));
        }
        
        
        public override bool cross(IShape i)
        {
            //через уравнение прямой
            bool temp = false;
            if (i is Segment)
            {
                Segment otherSegment = (Segment)i;
                
                double x1 = start.x[0];
                double y1 = start.x[1];
                double x2 = finish.x[0];
                double y2 = finish.x[1];
                double x3 = otherSegment.start.x[0];
                double y3 = otherSegment.start.x[1];
                double x4 = otherSegment.finish.x[0];
                double y4 = otherSegment.finish.x[1];

                double a1 = y2 - y1;
                double b1 = x1 - x2;
                double c1 = x2 * y1 - x1 * y2;
                double a2 = y4 - y3;
                double b2 = x3 - x4;
                double c2 = x4 * y3 - x3 * y4;

                double det = a1 * b2 - a2 * b1;
                
                
                if (det == 0)
                {
                    if (y1 == y3)
                    {
                        if (x1<x3 && x2>x3 && x2<x4)
                        {
                            temp = true;
                        }

                        if (x1<x4 && x3<x1 && x3<x2)
                        {
                            temp = true;
                        }
                    }
                    else if (x1 == x3)
                    {
                        if (y1<y3 && y2>y3 && y2<y4)
                        {
                            temp = true;
                        }

                        if (y1<y4 && y3<y1 && y3<y2)
                        {
                            temp = true;
                        }
                    }
                    else
                    {
                        temp = false;    
                    }
                    
                }
                else
                {
                    double x = (b1 * c2 - b2 * c1) / det;
                    double y = (a2 * c1 - a1 * c2) / det;

                    if (x >= Math.Min(x1, x2) && x <= Math.Max(x1, x2) &&
                        x >= Math.Min(x3, x4) && x <= Math.Max(x3, x4) &&
                        y >= Math.Min(y1, y2) && y <= Math.Max(y1, y2) &&
                        y >= Math.Min(y3, y4) && y <= Math.Max(y3, y4))
                    {
                        temp = true;
                    }
                    else
                    {
                        temp = false;
                    }
                }
                //Этот метод использует формулу для нахождения уравнения прямой,
                //проходящей через две точки на плоскости, и определяет пересекаются ли две прямые.
                //Затем он проверяет, лежат ли точки пересечения на обоих отрезках.
                //Если да, то отрезки пересекаются, и метод возвращает true.
                //Если нет, метод возвращает false.
            }
            else if (i is Polyline)
            {
                Polyline polyline = (Polyline)i;
                Segment thisSegment = new Segment(start, finish);
                bool flag;
                for (int j = 0; j < polyline.getN()-1; j++)
                {
                    flag = thisSegment.cross(new Segment(polyline.getP(j), polyline.getP(j + 1)));
                    if (flag)
                    {
                        temp = true;
                    }
                }
            }
            else if (i is NGon)
            {
                NGon ngon = (NGon)i;
                Segment thisSegment = new Segment(start, finish);
                bool flag = false;
                for (int j = 0; j < ngon.getN(); j++)
                {
                    if (j < ngon.getN() - 1)
                    {
                        flag = thisSegment.cross(new Segment(ngon.getP(j), ngon.getP(j + 1)));
                    }
                    if (j == ngon.getN() - 1)
                    {
                        flag = thisSegment.cross(new Segment(ngon.getP(j), ngon.getP(0)));
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
                double dx = finish.x[0] - start.x[0];
                double dy = finish.x[1] - start.x[1];
                double a = dx * dx + dy * dy;
                double b = 2 * (dx * (start.x[0] - circle.getP().x[0]) + dy * (start.x[1] - circle.getP().x[1]));
                double cc = circle.getP().x[0] * circle.getP().x[0] + circle.getP().x[1] * circle.getP().x[1] + start.x[0] * start.x[0] + start.x[1] * start.x[1] -
                            2 * (circle.getP().x[0] * start.x[0] + circle.getP().x[1] * start.x[1]) - circle.getR() * circle.getR();
                double delta = b * b - 4 * a * cc;
                if (delta < 0) temp = false; // отрезок и круг не пересекаются
                double t1 = (-b + Math.Sqrt(delta)) / (2 * a);
                double t2 = (-b - Math.Sqrt(delta)) / (2 * a);
                if ((t1 >= 0 && t1 <= 1) || (t2 >= 0 && t2 <= 1)) temp = true; // отрезок пересекает круг
                
                Point2D p1 = new Point2D(new []{ start.x[0] + t1 * dx, start.x[1] + t1 * dy});
                Point2D p2 = new Point2D(new []{ start.x[0] + t2 * dx, start.x[1] + t2 * dy});
                
                if (p1.x[0] >= Math.Min(start.x[0], finish.x[0]) && p1.x[0] <= Math.Max(start.x[0], finish.x[0]) &&
                    p1.x[1] >= Math.Min(start.x[1], finish.x[1]) && p1.x[1] <= Math.Max(start.x[1], finish.x[1])) temp = true; // отрезок пересекает круг
                if (p2.x[0] >= Math.Min(start.x[0], finish.x[0]) && p2.x[0] <= Math.Max(start.x[0], finish.x[0]) &&
                    p2.x[1] >= Math.Min(start.x[1], finish.x[1]) && p2.x[1] <= Math.Max(start.x[1], finish.x[1])) temp = true; // отрезок пересекает круг
            }
            else
            {
                throw new ArgumentException("Invalid type of object.");
            }   
            
            
            return temp;
        }
        
        public override string ToString()
        {
            double[] PointsS = { start.x[0], start.x[1] };
            double[] PointsF = { finish.x[0], finish.x[1] };
            string[] PointsSStrings = Array.ConvertAll(PointsS, d => d.ToString());
            string startPoints = string.Join("; ", PointsSStrings);
            string[] PointsFStrings = Array.ConvertAll(PointsF, d => d.ToString());
            string finishPoints = string.Join("; ", PointsFStrings);
            return $"Segment: (start=[{startPoints}], finish=[{finishPoints}])";
        }    
        /*
        public override String ToString()
        {
            string Start = string.Join("; ", (string[])start.x.Select(d => d.ToString()));
            string Finish = string.Join("; ", (string[])finish.x.Select(d => d.ToString()));
            return string.Format("Segment: (start=[{0}], finish=[{1}])", Start, Finish);
        }
        */
        
    }
}