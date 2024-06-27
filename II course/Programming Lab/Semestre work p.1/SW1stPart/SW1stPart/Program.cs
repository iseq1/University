using System;
using System.Collections.Generic;

namespace SW1stPart
{
    internal class Program
    {
        /*
        Общие замечания:
        1. Нужно переопределить toString для всех классов, в которых указан, чтобы 
            выводил все внутренние параметры.
        2. В конструкторах необходимо выполнить проверку на корректность 
            входных данных (Количество координат совпадает с указанной 
            размерностью, в прямоугольнике смежные стороны под прямым углом, 
            …) через соответствующие исключения(Exception).
        3. В схемах, представленных ниже подчёркнуты статические функции (static).
        4. Для каждого внутреннего параметра должен быть реализован get-метод.
        5. Для каждого внутреннего параметра, кроме количества точек и 
            размерности пространства, должен быть реализован set-метод.
        6. Если внутренний параметр массив, то get/set-методы должны быть 
            реализованы в двух вариантах:
            a. Работа с цельным массивом.
            b. Работа с элементом по номеру.
                
        */
        public static void Main(string[] args)
        {
            Console.WriteLine(10+Math.Pow(10,0));
            // 
            Console.WriteLine("Введите количество фигур: ");
            int countShapes = Convert.ToInt32(Console.ReadLine());
            List<IShape> shapesList = new List<IShape>(countShapes);
            for (int i = 0; i < countShapes; i++)
            {
                Console.WriteLine("\nВведите название фигуры: ");
                var shape = Console.ReadLine();
                if (shape == "Segment")
                {
                    Console.WriteLine("Введите координаты начала и конца отрезка: ");
                    shapesList.Add(new Segment(fromStrToPoint2D(Console.ReadLine()),fromStrToPoint2D(Console.ReadLine())));
                }
                if (shape == "Polyline")
                { 
                    Console.WriteLine("Введите количество точек кривой: ");
                    int countPoint = Convert.ToInt32(Console.ReadLine());
                    Point2D[] point2Ds = new Point2D[countPoint];
                    Console.WriteLine("Введите координаты каждой точки кривой: ");
                    for (int j = 0; j < countPoint; j++)
                    {
                        point2Ds[j] = fromStrToPoint2D(Console.ReadLine());
                    }
                    shapesList.Add(new Polyline(point2Ds));
                }
                if (shape == "NGon")
                {
                    Console.WriteLine("Введите количество точек н-угольника: ");
                    int countPoint = Convert.ToInt32(Console.ReadLine());
                    Point2D[] point2Ds = new Point2D[countPoint];
                    Console.WriteLine("Введите координаты каждой точки н-угольника: ");
                    for (int j = 0; j < countPoint; j++)
                    {
                        point2Ds[j] = fromStrToPoint2D(Console.ReadLine());
                    }
                    shapesList.Add(new NGon(point2Ds));
                } 
                if (shape == "TGon")
                {
                    Console.WriteLine("Введите координаты каждой точки триугольника: ");
                    shapesList.Add(new TGon(new []{fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine())}));
                }
                if (shape == "QGon")
                {
                    Console.WriteLine("Введите координаты каждой точки четёрыхугольника: ");
                    shapesList.Add(new QGon(new []{fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine())}));
                }
                if (shape == "Rectangle")
                {
                    Console.WriteLine("Введите координаты каждой точки прямоугольника: ");
                    shapesList.Add(new Rectangle(new []{fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine())}));
                }
                if (shape == "Trapeze")
                {
                    Console.WriteLine("Введите координаты каждой точки трапеции: ");
                    shapesList.Add(new Trapeze(new []{fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine())}));
                }
                if (shape == "Circle")
                {
                    Console.WriteLine("Введите координаты центра и радиус окружности: ");
                    shapesList.Add( new Circle(fromStrToPoint2D(Console.ReadLine()), Convert.ToDouble(Console.ReadLine())));
                }
            }
            
            double allSquare = 0;
            double allLenght = 0;
            for (int i = 0; i < countShapes; i++)
            {
                //Console.WriteLine("Площадь " + shapesList[i].ToString() + ": " + shapesList[i].square());
                //Console.WriteLine("Длина " + shapesList[i].ToString() + ": " + shapesList[i].length());
                allSquare += shapesList[i].square();
                allLenght += shapesList[i].length();
            }
            double AverageSquare = allSquare/countShapes;
            Console.WriteLine("Суммарная площадь введенных фигур: " + allSquare);
            Console.WriteLine("Суммарная длина введенных фигур: " + allLenght);
            Console.WriteLine("Средняя площадь введенных фигур: " + AverageSquare);
        
            Console.WriteLine("\n===================\n");
            List<IShape> shapesList2 = new List<IShape>(countShapes);
            for (int i = 0; i < countShapes; i++)
            {
                var shape = shapesList[i];
                if (shape.GetType() == typeof(Segment))
                {
                    Console.WriteLine("Введите координаты начала и конца отрезка: ");
                    shapesList2.Add(new Segment(fromStrToPoint2D(Console.ReadLine()),fromStrToPoint2D(Console.ReadLine())));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));
                }
                if (shape.GetType() == typeof(Polyline))
                { 
                    Console.WriteLine("Введите количество точек кривой: ");
                    int countPoint = Convert.ToInt32(Console.ReadLine());
                    Point2D[] point2Ds = new Point2D[countPoint];
                    Console.WriteLine("Введите координаты каждой точки кривой: ");
                    for (int j = 0; j < countPoint; j++)
                    {
                        point2Ds[j] = fromStrToPoint2D(Console.ReadLine());
                    }
                    shapesList2.Add(new Polyline(point2Ds));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                
                if (shape.GetType() == typeof(TGon))
                {
                    Console.WriteLine("Введите координаты каждой точки триугольника: ");
                    shapesList2.Add(new TGon(new []{fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine())}));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                else if (shape.GetType() == typeof(QGon))
                {
                    Console.WriteLine("Введите координаты каждой точки четёрыхугольника: ");
                    shapesList2.Add(new QGon(new []{fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine()),
                                                         fromStrToPoint2D(Console.ReadLine())}));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                if (shape.GetType() == typeof(Rectangle))
                {
                    Console.WriteLine("Введите координаты каждой точки прямоугольника: ");
                    shapesList2.Add(new Rectangle(new []{fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine()),
                                                              fromStrToPoint2D(Console.ReadLine())}));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                else if (shape.GetType() == typeof(Trapeze))
                {
                    Console.WriteLine("Введите координаты каждой точки трапеции: ");
                    shapesList2.Add(new Trapeze(new []{fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine()),
                                                            fromStrToPoint2D(Console.ReadLine())}));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                else if (shape.GetType() == typeof(Circle))
                {
                    Console.WriteLine("Введите координаты центра и радиус окружности: ");
                    shapesList2.Add( new Circle(fromStrToPoint2D(Console.ReadLine()), Convert.ToDouble(Console.ReadLine())));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));

                }
                else if (shape.GetType() == typeof(NGon))
                { 
                    Console.WriteLine("Введите количество точек н-угольника: ");
                    int countPoint = Convert.ToInt32(Console.ReadLine());
                    Point2D[] point2Ds = new Point2D[countPoint];
                    Console.WriteLine("Введите координаты каждой точки н-угольника: ");
                    for (int j = 0; j < countPoint; j++)
                    {
                        point2Ds[j] = fromStrToPoint2D(Console.ReadLine()); 
                    }
                    shapesList2.Add(new NGon(point2Ds));
                    Console.WriteLine(CrossOrNOT(shapesList[i], shapesList2[i]));
                    var movedShape = MoveShape(shapesList2[i]);
                    Console.WriteLine(CrossOrNOT(shapesList[i], movedShape));
                 
                } 
            }
            
        }
        static public Point2D fromStrToPoint2D(string a)
        {
            string[] str = a.Split(' ');
            double[] coord = { Convert.ToDouble(str[0]), Convert.ToDouble(str[1]) };
            return new Point2D(coord);
        }
        static public string CrossOrNOT(IShape first, IShape second)
        {
            bool temp = first.cross(second);
            if (temp) return "Данные фигуры пересекаются!\n";
            return "Данные фигуры НЕ пересекаются!\n";
        }
        static public IShape MoveShape(IShape i)
        {
            Console.WriteLine("Введите тип движения фигуры: ");
            var move = Console.ReadLine();
            IShape tempShape = i;
            if (move == "Shift")
            {
                Console.WriteLine("Введите вектор сдвига: ");
                Point2D vector = fromStrToPoint2D(Console.ReadLine());
                tempShape = i.shift(vector);
            }
            if (move == "Rotate")
            {
                Console.WriteLine("Введите угол поворота: ");
                double angle = Convert.ToDouble(Console.ReadLine());
                tempShape = i.rot(angle);
            }
            if (move == "Symmetry")
            {
                Console.WriteLine("Введите ось для симметрии: ");
                int axis = Convert.ToInt32(Console.ReadLine());
                tempShape = i.symAxis(axis);
            }
            return tempShape;
        }
    }
}