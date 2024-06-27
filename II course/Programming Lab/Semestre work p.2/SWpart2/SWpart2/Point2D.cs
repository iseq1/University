using System;


namespace SWpart2
{
    public class Point2D : Point
    {
       
        public Point2D() : base(dim:2)
        {
            x = new double[dim];
        }
 
        public Point2D(double[] x) : base(dim:2) 
        {
            if (dim <= 0) {
                throw new ArgumentException("Размерность пространтсва должна быть более нуля.");
            }
            if (x.Length != dim) {
                throw new ArgumentException("Количество координат не соответствует размерности.");
            }
            this.x = x;
        }

        public static Point2D rot(Point2D p, double phi) //поворот точки на угол phi относительно 0.0
        {
            return p.rot(phi);
        }

        public Point2D rot(double phi)
        {
            double sinPhi = Math.Sin(phi);
            double cosPhi = Math.Cos(phi);
            double newX = x[0] * cosPhi - x[1] * sinPhi;
            double newY = x[0] * sinPhi + x[1] * cosPhi;
            double[] mas = {newX, newY}; 
            return new Point2D(mas);
        }
    }
}