using System;

namespace SWpart2
{
    public class Point3D : Point
    {
        public Point3D() : base(dim: 3)
        {
            x = new double[dim];
        }
         
        public Point3D(double[] x) : base(dim: 3)
        {
            if (dim <= 0) {
                throw new ArgumentException("Размерность пространтсва должна быть более нуля.");
            }
            if (x.Length != dim) {
                throw new ArgumentException("Количество координат не соответствует размерности.");
            }
            this.x = x;
        }

        public static Point3D cross_prod(Point3D p1, Point3D p2)
        {
            return p1.cross_prod(p2);
        }

        public Point3D cross_prod(Point3D p1) // векторное произведение двух точек
        {
            var newX = x[1]*p1.x[2] - x[2]*p1.x[1];
            var newY = x[2]*p1.x[0] - x[0]*p1.x[2];
            var newZ = x[0]*p1.x[1] - x[1]*p1.x[0];
            double[] mas = {newX, newY, newZ}; 
            return new Point3D(mas);
        }

        public static double mix_prod(Point3D p1, Point3D p2, Point3D p3) //смешанное произведение трёх точек

        {
            return p1.mix_prod(p2, p3);
        }
        
        public double mix_prod(Point3D p1, Point3D p2)
        {
            var positivPart = x[0]*p1.x[1]*p2.x[2] + x[1]*p1.x[2]*p2.x[0] + x[2]*p1.x[0]*p2.x[1];
            var negativePart = x[2]*p1.x[1]*p2.x[0] + x[1]*p1.x[0]*p2.x[2] + x[0]*p1.x[2]*p2.x[1];
            return positivPart - negativePart;
        }
        
    }
}