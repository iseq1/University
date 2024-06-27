using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Media;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace third_SW_vol_2._0
{
    //Основная форма с игрой
    
    // для формы с шопом можно завести матрицу (индекс скина, одеть/снять, открыт/закрыт) и передавать инфу сюда
    // для монет и рекордов можно класс с сериализацией в хмл 
    
    //осталось сделать кнопку выхода, магазинчик(нинаю нинаю) и полный выход
    public partial class GameForm : Form
    {
        Player player;
        Timer timer1;
        Timer timer2;
        Sound sound = new Sound();
        GameData gd = new GameData();
        GameInterface gi = new GameInterface();
        Shop shop = new Shop();
        
        public GameForm()
        {
            this.DoubleBuffered = true;
            InitializeComponent();
            Init();
            timer1 = new Timer();
            timer1.Interval = 15;
            timer1.Tick += new EventHandler(Update);
            timer1.Start();
            this.KeyDown += new KeyEventHandler(OnKeyboardPressed);
            this.KeyUp += new KeyEventHandler(OnKeyboardUp);
            this.BackgroundImage = Image.FromFile("back.jpg");
            this.Height = 600;
            this.Width = 330;
            this.Paint += new PaintEventHandler(OnRepaint);
            GoFullscreen(true);
            Interface();
            Controls.Add(gi.gold); Controls.Add(gi.record); Controls.Add(gi.score);
            gi.CreateGoldLabel(gi.gold);
            gi.CreateRecordLabel(gi.record);
            gi.CreateScoreLabel(gi.score);
            timer2 = new Timer();
            timer2.Interval = 15;
            timer2.Tick += new EventHandler(Update2);
            timer2.Start();
            
            //sound.BackgroundSound();
        }

        private void Update2(object sender,EventArgs e)
        {
            gi.UpdateLabels(gi.record,gi.gold,gi.score);
        }

        private void Interface()
        {
            PictureBox bp = new PictureBox();
            bp.Image = Image.FromFile("Interface.png");
            bp.SizeMode = PictureBoxSizeMode.StretchImage;
            bp.Size = new Size(700,900);
            bp.Location = new Point(750, 0);
            Controls.Add(bp);
        }

        

        private void GoFullscreen(bool fullscreen)
        {
            if (fullscreen)
            {
                this.WindowState = FormWindowState.Normal;
                this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
                this.Bounds = Screen.PrimaryScreen.Bounds;
            }
            else
            {
                this.WindowState = FormWindowState.Maximized;
                this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Sizable;
            }
        }
        
        public void Init()
        {
            PlatformController.platforms = new System.Collections.Generic.List<Platform>();
            PlatformController.AddPlatform(new System.Drawing.PointF(100, 400));
            PlatformController.startPlatformPosY = 400;
            PlatformController.score = 0;
            PlatformController.GenerateStartSequence();
            PlatformController.bullets.Clear();
            PlatformController.bonuses.Clear();
            PlatformController.enemies.Clear();
            PlatformController.coins.Clear();
            player = new Player();
            gd.InpuScoretData();
            gd.InputCashData();
        }

        private void OnKeyboardUp(object sender,KeyEventArgs e)
        {
            player.physics.dx = 0;
            player.sprite = Image.FromFile("player1.png");
            shop.InputTypeSprite();
            int typeSprite = Convert.ToInt32(shop.typesprite);
            switch (typeSprite)
            {
                case 1:
                    player.sprite = Image.FromFile("player1.png");
                    break;
                case 2:
                    player.sprite = Image.FromFile("player2.png");
                    break;
                case 3:
                    player.sprite = Image.FromFile("player3.png");
                    break;
                case 4:
                    player.sprite = Image.FromFile("player4.png");
                    break;
                case 5:
                    player.sprite = Image.FromFile("player5.png");
                    break;
                case 6:
                    player.sprite = Image.FromFile("player6.png");
                    break;
                case 7:
                    player.sprite = Image.FromFile("player7.png");
                    break;
                case 8:
                    player.sprite = Image.FromFile("player8.png");
                    break;
            }
            switch (e.KeyCode.ToString())
            {
                case "Space":
                    sound.ShootingSound();
                    PlatformController.CreateBullet(new PointF(player.physics.transform.position.X + player.physics.transform.size.Width / 2, player.physics.transform.position.Y));
                    break;
            }
        }
        
        private void OnKeyboardPressed(object sender,KeyEventArgs e)
        {
            switch (e.KeyCode.ToString())
            {
                case "Right":
                    player.physics.dx = 6;
                    break;
                case "Left":
                    player.physics.dx = -6;
                    break;
                case "Space":
                    player.sprite = Image.FromFile("shooting.png");
                    //PlatformController.CreateBullet(new PointF(player.physics.transform.position.X + player.physics.transform.size.Width/2,player.physics.transform.position.Y));
                    break;
                case "Escape":
                    Application.Exit();
                    break;
            }
        }


        private void Update(object sender,EventArgs e)
        {
            gd.InpuScoretData();
            gd.InputCashData();
            gd.OutputScoreData();
            if ( (player.physics.transform.position.Y >= PlatformController.platforms[0].transform.position.Y + 200) || (player.physics.StandartCollidePlayerWithObjects(true,false, false))  )
                Init();

            if (PlatformController.coins.Count > 0 && player.physics.StandartCollidePlayerWithObjects(false, false, true))
            {
                for (int i = 0; i < PlatformController.coins.Count; i++)
                {
                    PlatformController.RemoveCoin(i);
                    gd.OutputCashData();
                    break;
                }
            }

            player.physics.StandartCollidePlayerWithObjects(false, true, false);
            
            if (PlatformController.bullets.Count > 0)
            {
                for (int i = 0; i < PlatformController.bullets.Count; i++)
                {
                    if (Math.Abs(PlatformController.bullets[i].physics.transform.position.Y - player.physics.transform.position.Y) > 500)
                    {
                        PlatformController.RemoveBullet(i); 
                        continue;
                    }
                    PlatformController.bullets[i].MoveUp();
                }
            }
            if (PlatformController.enemies.Count > 0)
            {
                for (int i = 0; i < PlatformController.enemies.Count; i++)
                {
                    if (PlatformController.enemies[i].physics.StandartCollide())
                    {
                        PlatformController.RemoveEnemy(i);
                        break;
                    }
                }
            }
            
            
            
            player.physics.ApplyPhysics();
            FollowPlayer();
            Invalidate();
        }

        public void FollowPlayer()
        {
            int offset = 400 - (int)player.physics.transform.position.Y;
            player.physics.transform.position.Y += offset;
            for(int i = 0; i < PlatformController.platforms.Count; i++)
            {
                var platform = PlatformController.platforms[i];
                platform.transform.position.Y += offset;
            }
            for (int i = 0; i < PlatformController.bullets.Count; i++)
            {
                var bullet = PlatformController.bullets[i];
                bullet.physics.transform.position.Y += offset;
            }
            for (int i = 0; i < PlatformController.enemies.Count; i++)
            {
                var enemy = PlatformController.enemies[i];
                enemy.physics.transform.position.Y += offset;
            }
            for (int i = 0; i < PlatformController.bonuses.Count; i++)
            {
                var bonus = PlatformController.bonuses[i];
                bonus.physics.transform.position.Y += offset;
            }

            for (int i = 0; i < PlatformController.coins.Count; i++)
            {
                var coin = PlatformController.coins[i];
                coin.physics.transform.position.Y += offset;
            }
        }

        private void OnRepaint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            if (PlatformController.platforms.Count > 0)
            {
                for (int i = 0; i < PlatformController.platforms.Count; i++)
                    PlatformController.platforms[i].DrawSprite(g);
            }
            if (PlatformController.bullets.Count > 0)
            {
                for (int i = 0; i < PlatformController.bullets.Count; i++)
                    PlatformController.bullets[i].DrawSprite(g);
            }
            if (PlatformController.enemies.Count > 0)
            {
                for (int i = 0; i < PlatformController.enemies.Count; i++)
                    PlatformController.enemies[i].DrawSprite(g);
            }
            if (PlatformController.bonuses.Count > 0)
            {
                for (int i = 0; i < PlatformController.bonuses.Count; i++)
                    PlatformController.bonuses[i].DrawSprite(g);
            }
            if (PlatformController.coins.Count > 0)
            {
                for (int i = 0; i < PlatformController.coins.Count; i++)
                    PlatformController.coins[i].DrawSprite(g);
            }
            
            player.DrawSprite(g);
        }
    }
}