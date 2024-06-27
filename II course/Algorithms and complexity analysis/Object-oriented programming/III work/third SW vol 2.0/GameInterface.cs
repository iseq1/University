using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;

namespace third_SW_vol_2._0
{
    public class GameInterface
    {
        GameData gm = new GameData();
        public System.Windows.Forms.Label record = new System.Windows.Forms.Label(); 
        public System.Windows.Forms.Label score = new System.Windows.Forms.Label();
        public System.Windows.Forms.Label gold = new System.Windows.Forms.Label();

        public void CreateRecordLabel(System.Windows.Forms.Label record)
        {
            record.BringToFront();
            this.record.Font = new System.Drawing.Font("", 24F, System.Drawing.FontStyle.Bold);
            this.record.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.record.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            record.Location = new Point(1050, 410);
            record.Size = new Size(150, 70);
            record.Text = Convert.ToString(gm.score);
        }

        public void CreateGoldLabel(System.Windows.Forms.Label gold)
        {
            gold.BringToFront();
            this.gold.Font = new System.Drawing.Font("", 24F, System.Drawing.FontStyle.Bold);
            this.gold.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.gold.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            gold.Location = new Point(1050, 620);
            gold.Size = new Size(150, 70);
            gold.Text = Convert.ToString(gm.cash);
        }

        public void CreateScoreLabel(System.Windows.Forms.Label score)
        {
            score.BringToFront();
            this.score.Font = new System.Drawing.Font("", 24F, System.Drawing.FontStyle.Bold);
            this.score.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.score.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            score.Location = new Point(1050, 510);
            score.Size = new Size(150, 70);
            score.Text = Convert.ToString(PlatformController.score);
        }

        public void UpdateLabels(System.Windows.Forms.Label record, System.Windows.Forms.Label gold, System.Windows.Forms.Label score)
        {
            gm.InpuScoretData();
            gm.InputCashData();
            record.Text = Convert.ToString(gm.score);
            gold.Text = Convert.ToString(gm.cash);
            score.Text = Convert.ToString(PlatformController.score);
        }
    }
}