using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Emgu;
using Emgu.CV;
using Emgu.CV.Util;
using Emgu.CV.Structure;
using Emgu.Util;
using DirectShowLib;
using Timer = System.Threading.Timer;


namespace WebCamera
{
    public partial class Form1 : Form
    {
        private VideoCapture capture = null;
        private DsDevice[] webCams = null;
        private int selectedCameraID = 0;
        

        public Form1()
        {
            InitializeComponent();
        }

        //загрузка формы
        private void Form1_Load(object sender, EventArgs e)
        {
            webCams = DsDevice.GetDevicesOfCat(FilterCategory.VideoInputDevice);
            for (int i = 0; i < webCams.Length; i++)
            {
                toolStripComboBox1.Items.Add(webCams[i].Name);
            }
        }

        //выбор камеры
        private void toolStripComboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            selectedCameraID = toolStripComboBox1.SelectedIndex;
        }

        //смотреть
        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            try
            {
                if (webCams.Length == 0)
                {
                    throw new Exception("Нет доступных камер!");
                }
                else if (toolStripComboBox1.SelectedItem == null)
                {
                    throw new Exception("Необходимо выбрать камеру!");
                }
                else if (capture != null)
                {
                    capture.Start();
                }
                else
                {
                    capture = new VideoCapture(selectedCameraID);
                    capture.ImageGrabbed += Capture_ImageGrabbed;
                    capture.Start();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void Capture_ImageGrabbed(object sender, EventArgs e)
        {
            try
            {
                Mat m = new Mat();
                capture.Retrieve(m);
                pictureBox1.Image = m.ToImage<Bgr, byte>().Flip(Emgu.CV.CvEnum.FlipType.Horizontal).Bitmap;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        //пауза
        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            try
            {
                if (capture != null)
                {
                    capture.Pause();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }


        //стоп
        private void toolStripButton3_Click(object sender, EventArgs e)
        {
            try
            {
                if (capture != null)
                {
                    capture.Pause();
                    capture.Dispose();
                    capture = null;
                    pictureBox1.Image.Dispose();
                    pictureBox1.Image = null;
                    selectedCameraID = 0;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        //кнопка выход
        private void выходToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        //сделать скриншот
        private void toolStripButton4_Click(object sender, EventArgs e)
        {
            try
            {
                Mat m = new Mat();
                capture.Retrieve(m);
                MakeScreenShotForm screenShotForm = new MakeScreenShotForm(m.ToImage<Bgr, byte>().Flip(Emgu.CV.CvEnum.FlipType.Horizontal));
                screenShotForm.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        //серия скриншотов
        
        private void toolStripButton5_Click(object sender, EventArgs e)
        {
            Init();
        }
        
        public void Init()
        {
            
            int num = 0; 
            // устанавливаем метод обратного вызова
            TimerCallback tm = new TimerCallback(MakeScreen);
            // создаем таймер
            Timer timer = new Timer(tm, num, 0, 5000);
        }

        private void MakeScreen(object state)
        {
            try
            {
                Mat m = new Mat();
                capture.Retrieve(m);
                MakeScreenShotForm screenShotForm = new MakeScreenShotForm(m.ToImage<Bgr, byte>().Flip(Emgu.CV.CvEnum.FlipType.Horizontal));
                screenShotForm.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка!", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        
    }
}
