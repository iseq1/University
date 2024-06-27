using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Linq;
using System.Media;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class Sound
    {
        
        public void BackgroundSound()
        {
            SoundPlayer backgroundsound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\backgroundsound.wav");
            backgroundsound.Play();
        }
        
        public void ShootingSound()
        {
            SoundPlayer shootingSound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\shootingsound.wav");
            shootingSound.Play();
            
            //прерывается при любом другом воспроизведении, нужно спросить как запускать звуки синхроно/паралеллтно друг другу
        }

        public void JumpSound()
        {
            SoundPlayer jumpsound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\jumpsound.wav");
            jumpsound.Play();
        }

        public void CollisionPnESound() //столкновение игрока с врагом
        {
        }
        
        public void CollisionBnESound() //столкновение пули с вргаом
        {
        }

        public void SpringSound()
        {
            SoundPlayer springsound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\springsound.wav");
            springsound.Play();  
        }

        public void JetpackSound()
        {
            SoundPlayer jetpacksound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\jetpacksound.wav");
            jetpacksound.Play();  
        }

        public void EmergenceEnemiesSound()
        {
        }

        public void EmergenceBonusSound()
        {
        }

        public void Losing()
        { 
            //надо ли, грубо говоря, столкновение с врагом -> проигрыш -> старт в одно мгновенье происходят, нужно ли перезагружать этот момент звуками? 
            SoundPlayer startsound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\startsound.wav");
            startsound.Play();
        }

        public void CoinSound()
        {
            SoundPlayer coinsound =
                new SoundPlayer(
                    @"D:\project under development\C# proj\OOP\third SW vol 2.0\third SW vol 2.0\bin\Debug\coinsound.wav");
            coinsound.Play();
        }
    }
}