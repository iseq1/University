using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.OleDb;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Excel = Microsoft.Office.Interop.Excel;
using System.Windows.Forms.DataVisualization.Charting;

namespace minipr1
{
    public partial class Form1 : Form
    {
        static Random rnd = new Random();
        static int D = 4;
        static int M = rnd.Next(250, 500);
        int[,] mas = new int[D, M];

        List<double> Height = new List<double>();
        List<double> Weight = new List<double>();
        List<double> Attitude = new List<double>();
        List<double> Glucose = new List<double>();
        List<int> Diabetes = new List<int>();
        double glucoseThreshold = 5.5;

        public Form1()
        {
            InitializeComponent();
            FirtsDG();
            SecondDG();
            //ThirdDG();
        }

        private void FirtsDG()
        {
            dataGridView1.RowCount = D;
            dataGridView1.ColumnCount = M;
         
            dataGridView1.Rows[0].HeaderCell.Value = "Height";
            dataGridView1.Rows[1].HeaderCell.Value = "Weight";
            dataGridView1.Rows[2].HeaderCell.Value = "Glucose";
            dataGridView1.Rows[3].HeaderCell.Value = "Diabetes";
            for (int i = 0; i < M; i++)
                dataGridView1.Columns[i].HeaderCell.Value = (i + 1).ToString();
        }

        private void SecondDG()
        {
            
            dataGridView2.RowCount = D;
            dataGridView2.ColumnCount = M;
            dataGridView2.Rows[0].HeaderCell.Value = "Height";
            dataGridView2.Rows[1].HeaderCell.Value = "Weight";
            dataGridView2.Rows[2].HeaderCell.Value = "Glucose";
            dataGridView2.Rows[3].HeaderCell.Value = "Diabetes";
            for (int i = 0; i < M; i++)
                dataGridView2.Columns[i].HeaderCell.Value = (i + 1).ToString();
        }

        private void ThirdDG()
        {
            dataGridView3.RowCount = D;
            dataGridView3.ColumnCount = Attitude.Count;
           
            dataGridView3.Rows[0].HeaderCell.Value = "Height";
            dataGridView3.Rows[1].HeaderCell.Value = "Weight";
            dataGridView3.Rows[2].HeaderCell.Value = "Glucose";
            dataGridView3.Rows[3].HeaderCell.Value = "Diabetes";
            for (int i = 0; i < Attitude.Count; i++)
                dataGridView3.Columns[i].HeaderCell.Value = (i + 1).ToString();
        }

        private void FourthDG()
        {
            dataGridView4.RowCount = D;
            dataGridView4.ColumnCount = Height.Count;

            dataGridView4.Rows[0].HeaderCell.Value = "Height";
            dataGridView4.Rows[1].HeaderCell.Value = "Weight";
            dataGridView4.Rows[2].HeaderCell.Value = "Glucose";
            dataGridView4.Rows[3].HeaderCell.Value = "Diabetes";
            for (int i = 0; i < Height.Count; i++)
                dataGridView4.Columns[i].HeaderCell.Value = (i + 1).ToString();
        }

        private void FivethhDG()
        {
            dataGridView5.RowCount = D;
            dataGridView5.ColumnCount = M;

            dataGridView5.Rows[0].HeaderCell.Value = "Height";
            dataGridView5.Rows[1].HeaderCell.Value = "Weight";
            dataGridView5.Rows[2].HeaderCell.Value = "Glucose";
            dataGridView5.Rows[3].HeaderCell.Value = "Diabetes";
            for (int i = 0; i < M; i++)
                dataGridView5.Columns[i].HeaderCell.Value = (i + 1).ToString();
        }

        private int BMI(int height, int weight)
        {
            double newHeight = height / 100;
            double BMI = weight / (newHeight * newHeight);
            if (BMI > 16 && BMI < 40)
            {
                Height.Add(height);
                Weight.Add(weight);
                return 1;
            }
            else
                return 0;
        }

        private void startButtn_Click(object sender, EventArgs e)
        {
            
            for (int i = 0; i < D; i++)
            {
                for (int j = 0; j < M; j++)
                {
                    mas[i, j] = 0;
                    dataGridView1.Rows[i].Cells[j].Value = mas[i, j].ToString();
                }
            }
           
        }

        private void WnHButtn_Click(object sender, EventArgs e)
        {
            for (int j = 0; j < M; j++)
            {
                mas[0, j] = rnd.Next(100,165);
                dataGridView2.Rows[0].Cells[j].Value = mas[0, j].ToString();
            }
            for (int j = 0; j < M; j++)
            {
                mas[1, j] = rnd.Next(25,62);
                dataGridView2.Rows[1].Cells[j].Value = mas[1, j].ToString();
            }
            for (int i = 2; i < D; i++)
            {
                for (int j = 0; j < M; j++)
                {
                    mas[i, j] = 0;
                    dataGridView2.Rows[i].Cells[j].Value = mas[i, j].ToString();
                }
            }
            FivethhDG();
        }

        private void DrawChart(List<double> xData, List<double> yData)
        {
            // Очистите график перед отрисовкой новых данных
            chart1.Series.Clear();

            // Создайте новый объект серии данных и задайте тип графика
            Series series = new Series("Height");
            series.ChartType = SeriesChartType.Line;
            Series series1 = new Series("Weight");
            series1.ChartType = SeriesChartType.Line;

            // Заполните серию данных значениями из списков xData и yData
            for (int i = 0; i < xData.Count; i++)
            {
                series1.Points.AddXY(i+1, yData[i]);
                series.Points.AddXY(i + 1, xData[i]);
            }
            series.BorderWidth = 2;
            series1.BorderWidth = 2;
            // Добавьте серию данных на график
            chart1.Series.Add(series);
            chart1.Series.Add(series1);

            // Подпишите ось X
            chart1.ChartAreas[0].AxisX.Title = "Count of people";
            chart1.ChartAreas[0].AxisX.TitleFont = new Font("Arial", 12, FontStyle.Bold);
            
            // Подпишите ось Y
            chart1.ChartAreas[0].AxisY.Title = "Height and weight indicators";
            chart1.ChartAreas[0].AxisY.TitleFont = new Font("Arial", 12, FontStyle.Bold);

        }

        private void SortingButtn_Click(object sender, EventArgs e)
        {
            chart1.Visible = true;
            DrawChart(Height, Weight);
        }

        private void MakeAttitude(List<double> height, List<double> weight)
        {
            for (int i = 0; i < height.Count; i++)
            {
                Attitude.Add(height[i] / weight[i]);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            
            MakeAttitude(Height, Weight);
            // Очистите график перед отрисовкой новых данных
            chart2.Series.Clear();

            // Создайте новый объект серии данных и задайте тип графика
            Series histogram = new Series();
            histogram.ChartType = SeriesChartType.Column;
            histogram.Name = "Weight-to-Height Ratio Histogram";

            // Настройка интервалов и подсчет частот
            int numIntervals = (int)(1 + Math.Log(Attitude.Count, 2));
            double minValue = Attitude.Min();
            double maxValue = Attitude.Max();
            double intervalSize = (maxValue - minValue) / numIntervals;
           
            int[] frequencies = new int[numIntervals];
            foreach (double ratio in Attitude)
            {
                int intervalIndex = (int)((ratio - minValue) / intervalSize);
                if (intervalIndex == numIntervals) // Проверка на выход за границы массива
                {
                    intervalIndex--; // Уменьшаем intervalIndex на 1, чтобы он находился в допустимых границах массива
                }
                frequencies[intervalIndex]++;
            }
            /*
            for (int i = 0; i < numIntervals; i++)
            {
                double intervalStart = minValue + (i * intervalSize);
                double intervalEnd = intervalStart + intervalSize;
                string intervalLabel = string.Format("{0:F1}-{1:F1}", intervalStart, intervalEnd);
                histogram.Points.AddXY(intervalLabel, frequencies[i]);
            }
            */

            for (int i = 0; i < numIntervals; i++)
            {
                double intervalStart = minValue + (i * intervalSize);
                double intervalEnd = intervalStart + intervalSize;
                double intervalAverage = (intervalStart + intervalEnd) / 2; // Вычисляем среднее значение интервала
                string intervalLabel = intervalAverage.ToString("F2"); // Форматируем среднее значение в нужном формате
                histogram.Points.AddXY(intervalLabel, frequencies[i]);
            }

            // Добавьте серию данных на график
            chart2.Series.Add(histogram);
            

            // Подпишите ось X
            chart2.ChartAreas[0].AxisY.Title = "Count of people";
            chart2.ChartAreas[0].AxisX.TitleFont = new Font("Arial", 12, FontStyle.Bold);

            // Подпишите ось Y
            chart2.ChartAreas[0].AxisX.Title = "Height and weight indicators";
            chart2.ChartAreas[0].AxisY.TitleFont = new Font("Arial", 12, FontStyle.Bold);

            ThirdDG();
        }

        private void Calculate_Glucose()
        {
            // Задайте стандартное отклонение шума (параметр σ)
            double sigma = 0.01;
            Random random = new Random();
            for (int i = 0; i < Attitude.Count; i++)
            {
                double glucoseLevel = Attitude[i] + GetRandomNoise(sigma);
                   if (glucoseLevel < 0)
                {
                    MessageBox.Show(glucoseLevel + " " + Attitude[i] + " " + (glucoseLevel- Attitude[i]));
                }
                // Добавьте зашумленное значение в список
                Glucose.Add(Math.Round(glucoseLevel, 3));
            }
        }
        static Random random = new Random();
        static double GetRandomNoise(double sigma)
        {
            double u1 = 1.0 - random.NextDouble(); // Обратим равномерно распределенную случайную переменную в интервале (0, 1] в равномерно распределенную случайную переменную в интервале [0, 1)
            double u2 = 1.0 - random.NextDouble();
            double z = Math.Sqrt(-2.0 * Math.Log(u1)) * Math.Sin(2.0 * Math.PI * u2); // cenтральная предельная теорема

            return sigma * z;
        }

        private void Calculate_diabet()
        {
            for (int i = 0; i < Glucose.Count; i++)
            {
                int label = (Glucose[i] < glucoseThreshold) ? 0 : 1;
                Diabetes.Add(label);
            }
        }


        private void button2_Click(object sender, EventArgs e)
        {
            double[,] newmas = new double[D, Attitude.Count];
            Calculate_Glucose();
            Calculate_diabet();
            for (int i=0;i<Attitude.Count; i++)
            {
                newmas[0, i] = Height[i]; dataGridView3.Rows[0].Cells[i].Value = newmas[0, i].ToString();
                newmas[1, i] = Weight[i]; dataGridView3.Rows[1].Cells[i].Value = newmas[1, i].ToString();
                newmas[2, i] = Glucose[i]; dataGridView3.Rows[2].Cells[i].Value = newmas[2, i].ToString(); 
                newmas[3, i] = Diabetes[i]; dataGridView3.Rows[3].Cells[i].Value = newmas[3, i].ToString();
            }
            // Очистите график перед отрисовкой новых данных
            chart3.Series.Clear();

            // Создайте новый объект серии данных и задайте тип графика
            Series series = new Series("Glucose value");
            series.ChartType = SeriesChartType.Line;
            Series series1 = new Series("Threshold");
            series1.ChartType = SeriesChartType.Line;
            List<double> newGL = new List<double>();
            Glucose.Sort();
            // Заполните серию данных значениями из списков xData и yData
            for (int i = 0; i < Attitude.Count; i++)
            {
                //MessageBox.Show("" + (i + 1) + (newmas[2, i]));
                series1.Points.AddXY(i + 1, glucoseThreshold);
                series.Points.AddXY(i + 1, Glucose[i]);
            }
            series.BorderWidth = 2;
            series1.BorderWidth = 2;
            // Добавьте серию данных на график
            chart3.Series.Add(series);
            chart3.Series.Add(series1);

            // Подпишите ось X
            chart3.ChartAreas[0].AxisX.Title = "Count of people";
            chart3.ChartAreas[0].AxisX.TitleFont = new Font("Arial", 12, FontStyle.Bold);

            // Подпишите ось Y
            chart3.ChartAreas[0].AxisY.Title = "Glucose value";
            chart3.ChartAreas[0].AxisY.TitleFont = new Font("Arial", 12, FontStyle.Bold);
        }

        private void button3_Click(object sender, EventArgs e)
        {
           
            FourthDG();
            double[,] newmas = new double[D, Height.Count];
           
            for (int i = 0; i < Height.Count; i++)
            {
                newmas[0, i] = Height[i]; dataGridView4.Rows[0].Cells[i].Value = newmas[0, i].ToString();
                newmas[1, i] = Weight[i]; dataGridView4.Rows[1].Cells[i].Value = newmas[1, i].ToString();
                newmas[2, i] = 0; dataGridView4.Rows[2].Cells[i].Value = newmas[2, i].ToString();
                newmas[3, i] = 0; dataGridView4.Rows[3].Cells[i].Value = newmas[3, i].ToString();
            }

           
        }

        private void button5_Click(object sender, EventArgs e)
        {
            
            for (int j = 0; j < M; j++)
            {
                
                dataGridView5.Rows[0].Cells[j].Value = mas[0, j].ToString();
            }
            for (int j = 0; j < M; j++)
            {
              
                dataGridView5.Rows[1].Cells[j].Value = mas[1, j].ToString();
            }
            for (int i = 2; i < D; i++)
            {
                for (int j = 0; j < M; j++)
                {
                    mas[i, j] = 0;
                    dataGridView5.Rows[i].Cells[j].Value = mas[i, j].ToString();
                }
            }
            for (int i = 0; i < M; i++)
            {
                int temp = BMI(mas[0, i], mas[1, i]);
                if(temp == 0) 
                {
                    dataGridView5.Rows[0].Cells[i].Value = "x";
                    dataGridView5.Rows[1].Cells[i].Value = "x";
                }

            }
            
        }

        private void button4_Click(object sender, EventArgs e)
        {
            
        }

        private void Form1_Load(object sender, EventArgs e)
        {
 
        }
    }
}
