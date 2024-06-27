using System;
using System.Linq;

namespace SWpart2
{
    public class Point
    {
        protected internal int dim;
        protected internal double[] x;

        public Point(int dim)
        {
            if (dim <= 0)
            {
                throw new ArgumentException("Размерность пространтсва должна быть более нуля.");
            }

            this.dim = dim;
            x = new double[dim];
        }
        public Point(int dim, double[] x)
        {
            if (dim <= 0) {
                throw new ArgumentException("Размерность пространтсва должна быть более нуля.");
            }
            if (x.Length != dim) {
                throw new ArgumentException("Количество координат не соответствует размерности.");
            }
            this.dim = dim;
            this.x = x;
        }

        public int getDim
        {
            get => dim; 
        }

        public double[] getX()
        {
            return x;
        }

        public double getX(int i)
        {
            if ((i >= 0) && (i < x.Length)){
                return x[i];
            }
            else
            {
                throw new ArgumentException("Индекс за пределами массива.");
            }
        }

        public void setX(double[] x)
        {
            this.x = x;
        }

        public void setX(double x, int i)
        {
            if ((i >= 0) && (i < this.x.Length))
            {
                this.x[i] = x;
            }
            else
            {
                throw new ArgumentException("Индекс за пределами массива.");
            }
        }

        public double abs() { //модуль точки(расстояние от 0.0)
            double sum = 0;
            for (int i = 0; i < dim; i++) {
                sum += x[i] * x[i];
            }
            return Math.Sqrt(sum);
        }
        
        public static Point add(Point a, Point b) //складывание двух точек по координатам
        {
            return a.add(b);
        }

        public Point add(Point b)
        {
            if (this.dim != b.dim) {
                throw new ArgumentException("Размерности пространств двух точек различны.");
            }
            Point c = new Point(this.dim);
            for (int i = 0; i < this.dim; i++) {
                c.x[i] = this.x[i] + b.x[i];
            }
            return c;
        }
         
        public static Point sub(Point a, Point b) //разность по координатам 
        {
            return a.sub(b);
        }

        public Point sub(Point b)
        {
            if (this.dim != b.dim) {
                throw new ArgumentException("Размерности пространств двух точек различны.");
            }
            Point c = new Point(this.dim);
            for (int i = 0; i < this.dim; i++) {
                c.x[i] = this.x[i] - b.x[i];
            }
            return c;
        }

        public static Point mult(Point a, double r) //умножение на число
        {
            return a.mult(r);
        }

        public Point mult(double r)
        {
            double[] result = new double[this.dim];
            for (int i = 0; i < this.dim; i++)
            {
                result[i] = r * this.x[i];
            }
            return new Point(this.dim, result);
        }

        public static double mult(Point a, Point b) // скалярное произведение двух точек
        {
            return a.mult(b);
        }

        public double mult(Point b)
        {
            if (this.dim != b.dim) {
                throw new ArgumentException("Размерности пространств двух точек различны.");
            }
            double result = 0;
            for (int i = 0; i < this.dim; i++)
            {
                result += this.x[i] * b.x[i];
            }
            return result;
        }

        public static Point symAxis(Point a, int i) // симметрия относительно оси I
        {
            return a.symAxis(i);
        }
        
        public Point symAxis(int i)
        {
            if (i > dim)
            {
                throw new Exception("Индекс больше размерности пространства точки.");
            }

            double[] newx = new double[getDim];
            if (getDim == 1)
            {
                newx[0] = -x[0];
            }

            if (getDim == 2)
            {
                if (i == 0)
                {
                    newx[0] = x[0];
                    newx[1] = -x[1];
                }

                if (i == 1)
                {
                    newx[0] = -x[0];
                    newx[1] = x[1];
                }
            }

            if (getDim == 3)
            {
                if (i == 0)
                {
                    newx[0] = x[0];
                    newx[1] = -x[1];
                    newx[2] = x[2];
                }

                if (i == 1)
                {
                    newx[0] = -x[0];
                    newx[1] = x[1];
                    newx[2] = x[2];
                }
                
                if (i == 1)
                {
                    newx[0] = x[0];
                    newx[1] = x[1];
                    newx[2] = -x[2];
                }
                
            }

            if (getDim>3)
            {
                for (int j = 0; j < getDim; j++)
                {
                    if (j == i)
                    {
                        newx[j] = -x[j];
                    }
                }
            }

            return new Point(dim, newx);
        }

        public override string ToString()
        {
            string xStr = string.Join("; ", (string[])x.Select(d => d.ToString()));
            return string.Format("Point: (dim={0}, x=[{1}])", dim, xStr);
        }
        
    }
}