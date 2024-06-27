using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace SWpart2
{
    public partial class Form1 : Form
    {
    //Пикселей в одном делении оси
    const int PIX_IN_ONE = 15;
    //Длина стрелки
    const int ARR_LEN = 10;
    //Список всех фигур
    private List<IShape> Shapes = new List<IShape>();
    //Список фигур, проверяемых на пересечение
    private List<IShape> CrossShapes = new List<IShape>();
    public Form1()
    {
        InitializeComponent();
        CanvasPictureBox.Paint += PictureBox1_PaintAxis;
    }
    private void PictureBox1_PaintAxis(object sender, PaintEventArgs e)
    {
        int w = CanvasPictureBox.ClientSize.Width / 2;
        int h = CanvasPictureBox.ClientSize.Height / 2;
        //Смещение начала координат в центр PictureBox
        e.Graphics.TranslateTransform(w, h);
        DrawXAxis(new Point2D(new double[]{-w, 0}), new Point2D(new double[]{w, 0}), e.Graphics);
        DrawYAxis(new Point2D(new double[]{0, h}), new Point2D(new double[]{0, -h}), e.Graphics);
        //Центр координат
        e.Graphics.FillEllipse(Brushes.Red, -2, -2, 4, 4);
        
    }
    //Рисование оси X
    private void DrawXAxis(Point2D start, Point2D end, Graphics g)
    {
        //Деления в положительном направлении оси
        for (int i = PIX_IN_ONE; i < end.x[0] - ARR_LEN; i += PIX_IN_ONE)
        {
            g.DrawLine(Pens.Black, i, -5, i, 5);
            DrawText(new Point2D(new double[]{i, 5}), (i / PIX_IN_ONE).ToString(), g);
        }
        //Деления в отрицательном направлении оси
        for (int i = -PIX_IN_ONE; i > start.x[0]; i -= PIX_IN_ONE)
        {
            g.DrawLine(Pens.Black, i, -5, i, 5);
            DrawText(new Point2D(new double[]{i, 5}), (i / PIX_IN_ONE).ToString(), g);
        }
        //Ось
        g.DrawLine(Pens.Black, new System.Drawing.Point((int)start.x[0], (int)start.x[1]), new System.Drawing.Point((int)end.x[0], (int)end.x[1]));
        //Стрелка
        g.DrawLines(Pens.Black, GetArrow(start.x[0], start.x[1], end.x[0], end.x[1], ARR_LEN));
    }
    //Рисование оси Y
    private void DrawYAxis(Point2D start, Point2D end, Graphics g)
    {
        //Деления в отрицательном направлении оси
        for (int i = PIX_IN_ONE; i < start.x[1]; i += PIX_IN_ONE)
        {
            g.DrawLine(Pens.Black, -5, i, 5, i);
            DrawText(new Point2D(new double[]{5, i}), (-i / PIX_IN_ONE).ToString(), g, true);
        }
        //Деления в положительном направлении оси
        for (int i = -PIX_IN_ONE; i > end.x[1] + ARR_LEN; i -= PIX_IN_ONE)
        {
            g.DrawLine(Pens.Black, -5, i, 5, i);
            DrawText(new Point2D(new double[]{5, i}), (-i / PIX_IN_ONE).ToString(), g, true);
        }
        //Ось
        g.DrawLine(Pens.Black, new System.Drawing.Point((int)start.x[0], (int)start.x[1]), new System.Drawing.Point((int)end.x[0], (int)end.x[1]));
        //Стрелка
        g.DrawLines(Pens.Black, GetArrow(start.x[0], start.x[1], end.x[0], end.x[1], ARR_LEN));
    }
    //Рисование текста
    private void DrawText(Point2D point, string text, Graphics g, bool isYAxis = false)
    {
        var f = new Font(Font.FontFamily, 6);
        var size = g.MeasureString(text, f);
        var pt = isYAxis
            ? new PointF((float)(point.x[0] + 1), (float)(point.x[1] - size.Height / 2))
            : new PointF((float)(point.x[0] - size.Width / 2), (float)(point.x[1] + 1));
        var rect = new RectangleF(pt, size);
        g.DrawString(text, f, Brushes.Black, rect);
    }
    //Вычисление стрелки оси
    private static PointF[] GetArrow(double x1, double y1, double x2, double y2, float len = 10, float width = 4)
    {
        PointF[] result = new PointF[3];
        //направляющий вектор отрезка
        var n = new PointF((float)(x2 - x1), (float)(y2 - y1));
        //Длина отрезка
        var l = (float)Math.Sqrt(n.X * n.X + n.Y * n.Y);
        //Единичный вектор
        var v1 = new PointF(n.X / l, n.Y / l);
        //Длина стрелки
        n.X = (float)(x2 - v1.X * len);
        n.Y = (float)(y2 - v1.Y * len);
        result[0] = new PointF(n.X + v1.Y * width, n.Y - v1.X * width);
        result[1] = new PointF((float)x2, (float)y2);
        result[2] = new PointF(n.X - v1.Y * width, n.Y + v1.X * width);
        return result;
    }
    //Отрисовка всех фигур из List<IShape> Shapes
    private void CanvasPictureBox_Paint(object sender, PaintEventArgs e)
    {
        // Рисуем все фигуры, сохраненные в списке
        foreach (IShape shape in Shapes)
        {
            if (shape is Segment segment) 
            {
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)(segment.getStart().x[0] *
                    PIX_IN_ONE), (int)(segment.getStart().x[1] * PIX_IN_ONE * -1)), new System.Drawing.Point((int)
                    (segment.getFinish().x[0] * PIX_IN_ONE), (int)(segment.getFinish().x[1] * PIX_IN_ONE * -1)));
            }
            else if (shape is Polyline polyline)
            {
                for (int i = 0; i < polyline.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)polyline.getP(i).x[0]*PIX_IN_ONE, (int)polyline.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)polyline.getP(i+1).x[0]*PIX_IN_ONE, (int)polyline.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
            }
            else if (shape is Circle circle)
            {
                //circle
                e.Graphics.DrawEllipse(new Pen(Brushes.Black, 2), (float)(circle.getP().x[0]*PIX_IN_ONE - circle.getR()*PIX_IN_ONE), (float)
                    (circle.getP().x[1]*PIX_IN_ONE*-1 - circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE));
                //center
                e.Graphics.FillEllipse(Brushes.Black, (float)(circle.getP().x[0] * PIX_IN_ONE) - 2,
                    (float)(circle.getP().x[1] * PIX_IN_ONE * -1 - 2), 4, 4);
            }
            else if (shape is NGon nGon)
            {
                for (int i = 0; i < nGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)nGon.getP(i).x[0]*PIX_IN_ONE, (int)nGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(i+1).x[0]*PIX_IN_ONE, (int)nGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)nGon.getP(nGon.getN()-1).x[0]*PIX_IN_ONE, (int)nGon.getP(nGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(0).x[0]*PIX_IN_ONE, (int)nGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(TGon))
            {
                TGon tGon = (TGon)shape;
                for (int i = 0; i < tGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)tGon.getP(i).x[0]*PIX_IN_ONE, (int)tGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(i+1).x[0]*PIX_IN_ONE, (int)tGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)tGon.getP(tGon.getN()-1).x[0]*PIX_IN_ONE, (int)tGon.getP(tGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(0).x[0]*PIX_IN_ONE, (int)tGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(QGon))
            {
                QGon qGon = (QGon)shape;
                for (int i = 0; i < qGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)qGon.getP(i).x[0]*PIX_IN_ONE, (int)qGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(i+1).x[0]*PIX_IN_ONE, (int)qGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)qGon.getP(qGon.getN()-1).x[0]*PIX_IN_ONE, (int)qGon.getP(qGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(0).x[0]*PIX_IN_ONE, (int)qGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Rectangle))
            {
                Rectangle rectangle = (Rectangle)shape;
                for (int i = 0; i < rectangle.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)rectangle.getP(i).x[0]*PIX_IN_ONE, (int)rectangle.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(i+1).x[0]*PIX_IN_ONE, (int)rectangle.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)rectangle.getP(rectangle.getN()-1).x[0]*PIX_IN_ONE, (int)rectangle.getP(rectangle.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(0).x[0]*PIX_IN_ONE, (int)rectangle.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Trapeze))
            {
                Trapeze trapeze = (Trapeze)shape;
                for (int i = 0; i < trapeze.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)trapeze.getP(i).x[0]*PIX_IN_ONE, (int)trapeze.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(i+1).x[0]*PIX_IN_ONE, (int)trapeze.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Black, 2), new System.Drawing.Point((int)trapeze.getP(trapeze.getN()-1).x[0]*PIX_IN_ONE, (int)trapeze.getP(trapeze.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(0).x[0]*PIX_IN_ONE, (int)trapeze.getP(0).x[1]*PIX_IN_ONE*-1));
            }
        }
    }
    //Переход на MainForm
    private void GoToMainPage()
    {
        //переход на mainform
        TabPage myTabPage = tabControl1.TabPages["tabPageMainForm"];
        tabControl1.SelectedTab = myTabPage;
        
    }
    //Очистка tabPage
    private void tabPage_Enter(object sender, EventArgs e)
    {
        //tabPageAdd
            //textBox
        RadiusTextBox.Clear();
        for (int i = 0; i < 18; i++)
        {
            string px = "Point" + (i + 1) + "XtextBox";
            string py = "Point" + (i + 1) + "YtextBox";
            TextBox tbx = tabPageAddShape.Controls.Find(px, true).FirstOrDefault() as TextBox;
            TextBox tby = tabPageAddShape.Controls.Find(py, true).FirstOrDefault() as TextBox;
            if (tbx != null && tby != null)
            {
                tbx.Clear();
                tby.Clear();
            }
        }
            //ComboBox
        if (ShapeSelectionComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            ShapeSelectionComboBox.SelectedIndex = -1;
        else
            ShapeSelectionComboBox.Items.Clear();
            //NumericUpDown
        CountPointsNumericUpDown.Value = CountPointsNumericUpDown.Minimum;
        
        //tabPageMove
            //textBox
        AngleRotateTextBox.Clear();
        ShiftXTextBox.Clear();
        ShiftYTextBox.Clear();
            //ComboBox
        if (MoveComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            MoveComboBox.SelectedIndex = -1;
        else
            MoveComboBox.Items.Clear();
        if (ShapesComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            ShapesComboBox.SelectedIndex = -1;
        else
            ShapesComboBox.Items.Clear();
            //NumericUpDown
        AxisSymDomainUpDown.SelectedIndex = -1;

        //tabPageDelete
        if (DeleteShapeComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            DeleteShapeComboBox.SelectedIndex = -1;
        else
            DeleteShapeComboBox.Items.Clear();
        
        //tabPageCross
        if (FirstShapeIntersectionComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            FirstShapeIntersectionComboBox.SelectedIndex = -1;
        else
            FirstShapeIntersectionComboBox.Items.Clear();
        if (SecondShapeIntersectionComboBox.DropDownStyle != ComboBoxStyle.DropDownList)
            SecondShapeIntersectionComboBox.SelectedIndex = -1;
        else
            SecondShapeIntersectionComboBox.Items.Clear();
        
    }
    //При выборе Move автоматом закрываем остальные окошки
    private void MoveComboBox_SelectedIndexChanged(object sender, EventArgs e)
    {
        if (MoveComboBox.SelectedIndex == -1)
        {
            ShiftXTextBox.Enabled = true;
            ShiftYTextBox.Enabled = true;

            AngleRotateTextBox.Enabled = true;

            AxisSymDomainUpDown.Enabled = true;
        }
        if (MoveComboBox.SelectedIndex == 0)
        {
            ShiftXTextBox.Enabled = true;
            ShiftYTextBox.Enabled = true;

            AngleRotateTextBox.Enabled = false;

            AxisSymDomainUpDown.Enabled = false;
        }
        if (MoveComboBox.SelectedIndex == 1)
        {
            ShiftXTextBox.Enabled = false;
            ShiftYTextBox.Enabled = false;

            AngleRotateTextBox.Enabled = true;

            AxisSymDomainUpDown.Enabled = false;
        }
        if (MoveComboBox.SelectedIndex == 2)
        {
            ShiftXTextBox.Enabled = false;
            ShiftYTextBox.Enabled = false;

            AngleRotateTextBox.Enabled = false;

            AxisSymDomainUpDown.Enabled = true;
        }
    }
    //При выборе фигуры автоматически задаём верное кол-во точек
    private void ShapeSelectionComboBox_SelectedIndexChanged(object sender, EventArgs e)
    {
        if (ShapeSelectionComboBox.SelectedIndex == -1)
        {
            CountPointsNumericUpDown.Value = CountPointsNumericUpDown.Minimum;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 0)
        {
            CountPointsNumericUpDown.Value = 2;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 1)
        {
            CountPointsNumericUpDown.Value = 2;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 2)
        {
            CountPointsNumericUpDown.Value = 1;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 3)
        {
            CountPointsNumericUpDown.Value = 3;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 4)
        {
            CountPointsNumericUpDown.Value = 3;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 5)
        {
            CountPointsNumericUpDown.Value = 4;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 6)
        {
            CountPointsNumericUpDown.Value = 4;
        }
        if (ShapeSelectionComboBox.SelectedIndex == 7)
        {
            CountPointsNumericUpDown.Value = 4;
        }
    }
    //Обработка нажатия на "Add Shape" - добавление в список фигур, добавление в комбобоксы, отрисовка фигуры и возвращение на MainForm 
    private void AddShapeButton_Click(object sender, EventArgs e)
    {
        try
        {
            if (ShapeSelectionComboBox.SelectedIndex == -1) 
            {
                throw new Exception("You didn't choose a shape!");
            }
            
            if (ShapeSelectionComboBox.SelectedIndex == 0)
            {
                if (CountPointsNumericUpDown.Value == 2)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the segment!");
                        }
                        
                    }
                    //segment
                    Shapes.Add(new Segment(new Point2D(new[] { Convert.ToDouble(Point1XtextBox.Text), Convert.ToDouble(Point1YtextBox.Text) }), new Point2D(new[] { Convert.ToDouble(Point2XtextBox.Text), Convert.ToDouble(Point2YtextBox.Text) })));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Invalid number of points for segment!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 1)
            {
                if(CountPointsNumericUpDown.Value > 1)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the polyline!");
                        }
                    }
                    //polyline
                    int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] polyline = new Point2D[pointsCount];
                    for (int i = 0; i < pointsCount; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        polyline[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new Polyline(polyline));

                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for polyline!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 2)
            {
                if(CountPointsNumericUpDown.Value == 1)
                {
                    if (string.IsNullOrEmpty(RadiusTextBox.Text))
                    {
                        throw new Exception("You did not enter or entered the wrong radius of the circle!");
                    }
                    if(string.IsNullOrEmpty(Point1XtextBox.Text) ||  string.IsNullOrEmpty(Point1YtextBox.Text))
                    {
                        throw new Exception("You did not enter or entered incorrect coordinates of the center of the circle!");
                    }
                    //circle
                    Shapes.Add(new Circle(new Point2D(new[] { Convert.ToDouble(Point1XtextBox.Text), Convert.ToDouble(Point1YtextBox.Text) }),Convert.ToDouble(RadiusTextBox.Text)));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]); 
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint; 
                    GoToMainPage(); 
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for circle!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 3)
            {
                if (CountPointsNumericUpDown.Value > 1)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the polygon!");
                        }
                        
                    }
                    //ngon
                    int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] ngon = new Point2D[pointsCount];
                    for (int i = 0; i < pointsCount; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        ngon[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new NGon(ngon));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for polygon!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 4)
            {
                if (CountPointsNumericUpDown.Value == 3)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the triangle!");
                        }
                        
                    }
                    //tgon
                    //int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] tgon = new Point2D[3];
                    for (int i = 0; i < 3; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        tgon[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new TGon(tgon));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for triangle!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 5)
            {
                if (CountPointsNumericUpDown.Value == 4)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the quadrangle!");
                        }
                        
                    }
                    //qgon
                    //int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] qgon = new Point2D[4];
                    for (int i = 0; i < 4; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        qgon[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new QGon(qgon));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for quadrangle!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 6)
            {
                if (CountPointsNumericUpDown.Value == 4)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the rectangle!");
                        }
                        
                    }
                    //rectangle
                    //int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] rectangle = new Point2D[4];
                    for (int i = 0; i < 4; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        rectangle[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new Rectangle(rectangle));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for rectangle!");
                }
            }

            else if (ShapeSelectionComboBox.SelectedIndex == 7)
            {
                if (CountPointsNumericUpDown.Value == 4)
                {
                    for (int i = 0; i < CountPointsNumericUpDown.Value; i++)
                    {
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        if(string.IsNullOrEmpty(tabPageAddShape.Controls[px].Text) || string.IsNullOrEmpty(tabPageAddShape.Controls[py].Text))
                        {
                            throw new Exception("You have not entered or entered incorrect coordinates of the points of the trapeze!");
                        }
                        
                    }
                    //trepeze
                    //int pointsCount = Convert.ToInt32(CountPointsNumericUpDown.Value);
                    Point2D[] trapeze = new Point2D[4];
                    for (int i = 0; i < 4; i++)
                    {
                        // Считываем данные из текущего TextBox и сохраняем их в массив строк
                        string px = "Point" + (i + 1) + "XtextBox";
                        string py = "Point" + (i + 1) + "YtextBox";
                        trapeze[i] = new Point2D(new[]
                        {
                            Convert.ToDouble(tabPageAddShape.Controls[px].Text),
                            Convert.ToDouble(tabPageAddShape.Controls[py].Text)
                        });
                    }

                    Shapes.Add(new Trapeze(trapeze));
                    AddToComboBoxs(Shapes[Shapes.Count - 1]);
                    CanvasPictureBox.Paint += CanvasPictureBox_Paint;
                    GoToMainPage();
                    MessageBox.Show("Created a new shape!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    throw new Exception("Wrong number of points for trapeze!");
                }
            }
        }
        catch(Exception ex)
        {
            // Вывод сообщения об ошибке
            MessageBox.Show("Error adding shape: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

    }
    //Добавление фигуры во все комбобоксы
    private void AddToComboBoxs(IShape shape)
    {
        ShapesComboBox.Items.Add(shape.ToString());
        DeleteShapeComboBox.Items.Add(shape.ToString());;
        FirstShapeIntersectionComboBox.Items.Add(shape.ToString());;
        SecondShapeIntersectionComboBox.Items.Add(shape.ToString());;
    }
    //Удаление фигуры из всез комбобоксов
    private void DeleteFromComboBox(string shapeString)
    {
        ShapesComboBox.Items.Remove(shapeString); 
        DeleteShapeComboBox.Items.Remove(shapeString);;
        FirstShapeIntersectionComboBox.Items.Remove(shapeString);;
        SecondShapeIntersectionComboBox.Items.Remove(shapeString);;
    }
    //Обработка нажатия на "Perimeter" - показываю периметр фигур
    private void PerimeterButton_Click(object sender, EventArgs e)
    {
        try
        {
            IsCrossLabel.Hide();
            SquareLabel.Hide();
            PerimeterLabel.Show();

            if (string.IsNullOrEmpty(PerimeterSquareTextBox.Text))
            {
                double perimeter = 0;
                foreach (IShape shapes in Shapes)
                {
                    perimeter += shapes.length();
                }

                PerimeterSquareTextBox.Text = Convert.ToString(perimeter);
            }
            else
            {
                double perimeter = 0;
                foreach (IShape shapes in Shapes)
                {
                    perimeter += shapes.length();
                }

                PerimeterSquareTextBox.Text = Convert.ToString(perimeter);
            }

            MessageBox.Show("Calculate the perimeter!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Error in calculating perimeter: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    //Обработка нажатия на "Square" - показываю площадь фигур
    private void SquareButton_Click(object sender, EventArgs e)
    {
        try
        {
            IsCrossLabel.Hide();
            PerimeterLabel.Hide();
            SquareLabel.Show();


            if (string.IsNullOrEmpty(PerimeterSquareTextBox.Text))
            {
                double square = 0;
                foreach (IShape shapes in Shapes)
                {
                    square += shapes.square();
                }

                PerimeterSquareTextBox.Text = Convert.ToString(square);
            }
            else
            {
                double square = 0;
                foreach (IShape shapes in Shapes)
                {
                    square += shapes.square();
                }

                PerimeterSquareTextBox.Text = Convert.ToString(square);
            }

            MessageBox.Show("Calculate the square!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Error in calculating square: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    //Удаление с полотна всех фигур из списка 
    private void CanvasPictureBox_Wipe(object sender, PaintEventArgs e)
    {
        IEnumerable<IShape> Combined = Shapes.Concat(CrossShapes);
        foreach (IShape shape in Combined)
        {
             if (shape is Segment segment) 
            {
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)segment.getStart().x[0]*PIX_IN_ONE, (int)segment.getStart().x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)segment.getFinish().x[0]*PIX_IN_ONE, (int)segment.getFinish().x[1]*PIX_IN_ONE*-1));
            }
            else if (shape is Polyline polyline)
            {
                for (int i = 0; i < polyline.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)polyline.getP(i).x[0]*PIX_IN_ONE, (int)polyline.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)polyline.getP(i+1).x[0]*PIX_IN_ONE, (int)polyline.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
            }
            else if (shape is Circle circle)
            {
                //circle
                e.Graphics.DrawEllipse(new Pen(Brushes.White, 2), (float)(circle.getP().x[0]*PIX_IN_ONE - circle.getR()*PIX_IN_ONE), (float)
                    (circle.getP().x[1]*PIX_IN_ONE*-1 - circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE));
                //center
                e.Graphics.FillEllipse(Brushes.White, (float)(circle.getP().x[0] * PIX_IN_ONE) - 2,
                    (float)(circle.getP().x[1] * PIX_IN_ONE * -1 - 2), 4, 4);
            }
            else if (shape is NGon nGon)
            {
                for (int i = 0; i < nGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)nGon.getP(i).x[0]*PIX_IN_ONE, (int)nGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(i+1).x[0]*PIX_IN_ONE, (int)nGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)nGon.getP(nGon.getN()-1).x[0]*PIX_IN_ONE, (int)nGon.getP(nGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(0).x[0]*PIX_IN_ONE, (int)nGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(TGon))
            {
                TGon tGon = (TGon)shape;
                for (int i = 0; i < tGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)tGon.getP(i).x[0]*PIX_IN_ONE, (int)tGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(i+1).x[0]*PIX_IN_ONE, (int)tGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)tGon.getP(tGon.getN()-1).x[0]*PIX_IN_ONE, (int)tGon.getP(tGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(0).x[0]*PIX_IN_ONE, (int)tGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(QGon))
            {
                QGon qGon = (QGon)shape;
                for (int i = 0; i < qGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)qGon.getP(i).x[0]*PIX_IN_ONE, (int)qGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(i+1).x[0]*PIX_IN_ONE, (int)qGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)qGon.getP(qGon.getN()-1).x[0]*PIX_IN_ONE, (int)qGon.getP(qGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(0).x[0]*PIX_IN_ONE, (int)qGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Rectangle))
            {
                Rectangle rectangle = (Rectangle)shape;
                for (int i = 0; i < rectangle.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)rectangle.getP(i).x[0]*PIX_IN_ONE, (int)rectangle.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(i+1).x[0]*PIX_IN_ONE, (int)rectangle.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)rectangle.getP(rectangle.getN()-1).x[0]*PIX_IN_ONE, (int)rectangle.getP(rectangle.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(0).x[0]*PIX_IN_ONE, (int)rectangle.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Trapeze))
            {
                Trapeze trapeze = (Trapeze)shape;
                for (int i = 0; i < trapeze.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)trapeze.getP(i).x[0]*PIX_IN_ONE, (int)trapeze.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(i+1).x[0]*PIX_IN_ONE, (int)trapeze.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.White, 2), new System.Drawing.Point((int)trapeze.getP(trapeze.getN()-1).x[0]*PIX_IN_ONE, (int)trapeze.getP(trapeze.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(0).x[0]*PIX_IN_ONE, (int)trapeze.getP(0).x[1]*PIX_IN_ONE*-1));
            }
        }
        

        int w = CanvasPictureBox.ClientSize.Width / 2;
        int h = CanvasPictureBox.ClientSize.Height / 2;
        DrawXAxis(new Point2D(new double[]{-w, 0}), new Point2D(new double[]{w, 0}), e.Graphics);
        DrawYAxis(new Point2D(new double[]{0, h}), new Point2D(new double[]{0, -h}), e.Graphics);
        e.Graphics.FillEllipse(Brushes.Red, -2, -2, 4, 4);
    }
    //Выделение фигур из списка для пересечения 
    private void CanvasPictureBox_Highlight(object sender, PaintEventArgs e)
    {
        foreach (IShape shape in CrossShapes)
        {
             if (shape is Segment segment) 
            {
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)segment.getStart().x[0]*PIX_IN_ONE, (int)segment.getStart().x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)segment.getFinish().x[0]*PIX_IN_ONE, (int)segment.getFinish().x[1]*PIX_IN_ONE*-1));
            }
            else if (shape is Polyline polyline)
            {
                for (int i = 0; i < polyline.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)polyline.getP(i).x[0]*PIX_IN_ONE, (int)polyline.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)polyline.getP(i+1).x[0]*PIX_IN_ONE, (int)polyline.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
            }
            else if (shape is Circle circle)
            {
                //circle
                e.Graphics.DrawEllipse(new Pen(Brushes.Red, 2), (float)(circle.getP().x[0]*PIX_IN_ONE - circle.getR()*PIX_IN_ONE), (float)
                    (circle.getP().x[1]*PIX_IN_ONE*-1 - circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE), (float)(2 * circle.getR()*PIX_IN_ONE));
                //center
                e.Graphics.FillEllipse(Brushes.Red, (float)(circle.getP().x[0] * PIX_IN_ONE) - 2,
                    (float)(circle.getP().x[1] * PIX_IN_ONE * -1 - 2), 4, 4);
            }
            else if (shape is NGon nGon)
            {
                for (int i = 0; i < nGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)nGon.getP(i).x[0]*PIX_IN_ONE, (int)nGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(i+1).x[0]*PIX_IN_ONE, (int)nGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)nGon.getP(nGon.getN()-1).x[0]*PIX_IN_ONE, (int)nGon.getP(nGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)nGon.getP(0).x[0]*PIX_IN_ONE, (int)nGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(TGon))
            {
                TGon tGon = (TGon)shape;
                for (int i = 0; i < tGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)tGon.getP(i).x[0]*PIX_IN_ONE, (int)tGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(i+1).x[0]*PIX_IN_ONE, (int)tGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)tGon.getP(tGon.getN()-1).x[0]*PIX_IN_ONE, (int)tGon.getP(tGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)tGon.getP(0).x[0]*PIX_IN_ONE, (int)tGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(QGon))
            {
                QGon qGon = (QGon)shape;
                for (int i = 0; i < qGon.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)qGon.getP(i).x[0]*PIX_IN_ONE, (int)qGon.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(i+1).x[0]*PIX_IN_ONE, (int)qGon.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)qGon.getP(qGon.getN()-1).x[0]*PIX_IN_ONE, (int)qGon.getP(qGon.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)qGon.getP(0).x[0]*PIX_IN_ONE, (int)qGon.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Rectangle))
            {
                Rectangle rectangle = (Rectangle)shape;
                for (int i = 0; i < rectangle.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)rectangle.getP(i).x[0]*PIX_IN_ONE, (int)rectangle.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(i+1).x[0]*PIX_IN_ONE, (int)rectangle.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)rectangle.getP(rectangle.getN()-1).x[0]*PIX_IN_ONE, (int)rectangle.getP(rectangle.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)rectangle.getP(0).x[0]*PIX_IN_ONE, (int)rectangle.getP(0).x[1]*PIX_IN_ONE*-1));
            }
            else if (shape.GetType() == typeof(Trapeze))
            {
                Trapeze trapeze = (Trapeze)shape;
                for (int i = 0; i < trapeze.getN()-1; i++)
                {
                    e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)trapeze.getP(i).x[0]*PIX_IN_ONE, (int)trapeze.getP(i).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(i+1).x[0]*PIX_IN_ONE, (int)trapeze.getP(i+1).x[1]*PIX_IN_ONE*-1));
                }
                e.Graphics.DrawLine(new Pen(Brushes.Red, 2), new System.Drawing.Point((int)trapeze.getP(trapeze.getN()-1).x[0]*PIX_IN_ONE, (int)trapeze.getP(trapeze.getN()-1).x[1]*PIX_IN_ONE* -1), new System.Drawing.Point((int)trapeze.getP(0).x[0]*PIX_IN_ONE, (int)trapeze.getP(0).x[1]*PIX_IN_ONE*-1));
            }
        }

        int w = CanvasPictureBox.ClientSize.Width / 2;
        int h = CanvasPictureBox.ClientSize.Height / 2;
        DrawXAxis(new Point2D(new double[]{-w, 0}), new Point2D(new double[]{w, 0}), e.Graphics);
        DrawYAxis(new Point2D(new double[]{0, h}), new Point2D(new double[]{0, -h}), e.Graphics);
        e.Graphics.FillEllipse(Brushes.Red, -2, -2, 4, 4);
    }
    ////Обработка нажатия на "Clean" - убираю периметр/площадь, удаляю с полотна фигуры, отчищаю комбобоксы, чищу список фигур
    private void CleanButton_Click(object sender, EventArgs e)
    {
        try
        {
            PerimeterSquareTextBox.Clear();
            PerimeterLabel.Hide();
            SquareLabel.Hide();
            IsCrossLabel.Hide();
            foreach (IShape shape in Shapes)
            {
                DeleteFromComboBox(shape.ToString());
            }

            CanvasPictureBox.Paint += CanvasPictureBox_Wipe;
            Shapes.Clear();
            CanvasPictureBox.Invalidate();
            MessageBox.Show("The canvas was successfully cleaned!", "Success", MessageBoxButtons.OK,
                MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show("Сleaning error: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    //Обработка нажатия на "Delete shape" - Удаление определенной фигуры из списка, комбобоксов, полотна
    private void DeleteShapeButton_Click(object sender, EventArgs e)
    {
        try
        {
            if (DeleteShapeComboBox.SelectedItem == null)
            {
                throw new Exception("You haven't chosen shapes yet!");
            }
            CanvasPictureBox.Paint += CanvasPictureBox_Wipe;
            string shape = DeleteShapeComboBox.SelectedItem.ToString();
            DeleteFromComboBox(shape);
            foreach (IShape shapes in Shapes)
            {
                if (shapes.ToString() == shape)
                {
                    Shapes.Remove(shapes);
                    break;
                }
            }

            CanvasPictureBox.Paint += CanvasPictureBox_Paint;
            GoToMainPage();
            MessageBox.Show("Shape deleted successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch(Exception ex)
        {
            // Вывод сообщения об ошибке
            MessageBox.Show("Error deleting shape: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    //Обработка нажатия на "Move shape" - двигаем фигуры, попутно обновляя полотно, списки и комбобоксы
    private void MoveShapeButton_Click(object sender, EventArgs e)
    {
        try
        {
            if (MoveComboBox.SelectedItem == null || ShapesComboBox.SelectedItem == null)
            {
                throw new Exception("You haven't selected a shape or move type yet!");
            }
            IShape newShape;
            if (MoveComboBox.SelectedIndex == 0)
            {
                if (string.IsNullOrEmpty(ShiftXTextBox.Text) || string.IsNullOrEmpty(ShiftYTextBox.Text))
                {
                    throw new Exception("You have not entered or entered incorrect coordinates of the shift vector");
                }
                //shift
                double shiftX = Convert.ToDouble(ShiftXTextBox.Text);
                double shiftY = Convert.ToDouble(ShiftYTextBox.Text);
                foreach (IShape shape in Shapes)
                {
                    if (shape.ToString() == ShapesComboBox.SelectedItem.ToString())
                    {
                        newShape = shape.shift(new Point2D(new[] { shiftX, shiftY }));
                        Shapes.Add(newShape);
                        DeleteFromComboBox(shape.ToString());
                        AddToComboBoxs(newShape);
                        Shapes.Remove(shape);
                        break;
                    }
                }
            }
            else if (MoveComboBox.SelectedIndex == 1)
            {
                if (string.IsNullOrEmpty(AngleRotateTextBox.Text))
                {
                    throw new Exception("You did not enter or entered an incorrect angle of rotation of the shape");
                }
                //rotation
                double angleRot = Convert.ToDouble(AngleRotateTextBox.Text);
                foreach (IShape shape in Shapes)
                {
                    if (shape.ToString() == ShapesComboBox.SelectedItem.ToString())
                    {
                        newShape = shape.rot(angleRot);
                        Shapes.Add(newShape);
                        DeleteFromComboBox(shape.ToString());
                        AddToComboBoxs(newShape);
                        Shapes.Remove(shape);
                        break;
                    }
                }
            }
            else if (MoveComboBox.SelectedIndex == 2)
            {
                if (AxisSymDomainUpDown.SelectedItem == null)
                {
                    throw new Exception("You did not enter or entered an incorrect axis of symmetry");
                }
                //symmetry
                int AxisSym;
                if (AxisSymDomainUpDown.SelectedItem.ToString() == "X")
                    AxisSym = 0;
                else
                    AxisSym = 1;

                foreach (IShape shape in Shapes)
                {
                    if (shape.ToString() == ShapesComboBox.SelectedItem.ToString())
                    {
                        newShape = shape.symAxis(AxisSym);
                        Shapes.Add(newShape);
                        DeleteFromComboBox(shape.ToString());
                        AddToComboBoxs(newShape);
                        Shapes.Remove(shape);
                        break;
                    }
                }
            }

            CanvasPictureBox.Paint += CanvasPictureBox_Wipe;
            CanvasPictureBox.Paint += CanvasPictureBox_Paint;
            GoToMainPage();
            MessageBox.Show("Shape position changed successfully!", "Success", MessageBoxButtons.OK,
                MessageBoxIcon.Information);
        }
        catch(Exception ex)
        {
            // Вывод сообщения об ошибке
            MessageBox.Show("Error when repositioning a shape: \n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    //Обработка нажатия на "Cross shapes" - 
    private void CrossingShapesButton_Click(object sender, EventArgs e)
    {
        try
        {
            if (CrossShapes.Count > 0)
                CrossShapes.Clear();
            if (FirstShapeIntersectionComboBox.SelectedItem == null || SecondShapeIntersectionComboBox.SelectedItem == null)
            {
                throw new Exception("You haven't chosen shapes yet!");
            }
            string firstShape = FirstShapeIntersectionComboBox.SelectedItem.ToString();
            string secondShape = SecondShapeIntersectionComboBox.SelectedItem.ToString();
            if (firstShape == secondShape)
            {
                throw new Exception("You can't check crossover on the same shape!");
            }
            PerimeterLabel.Hide();
            SquareLabel.Hide();
            IsCrossLabel.Show();

            foreach (IShape shape in Shapes)
            {
                if (shape.ToString() == firstShape)
                {
                    CrossShapes.Add(shape);
                }
                else if (shape.ToString() == secondShape)
                {
                    CrossShapes.Add(shape);
                }
            }

            if (CrossShapes[0].cross(CrossShapes[1]))
                PerimeterSquareTextBox.Text = "Yes";
            else
                PerimeterSquareTextBox.Text = "No";


            CanvasPictureBox.Paint += CanvasPictureBox_Wipe;
            CanvasPictureBox.Paint += CanvasPictureBox_Paint;
            CanvasPictureBox.Paint += CanvasPictureBox_Highlight;
            GoToMainPage();
            MessageBox.Show("Selected shapes checked for intersection!", "Success", MessageBoxButtons.OK,
                MessageBoxIcon.Information);
        }
        catch(Exception ex)
        {
            // Вывод сообщения об ошибке
            MessageBox.Show("Error while checking shape crossing: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
    }
}