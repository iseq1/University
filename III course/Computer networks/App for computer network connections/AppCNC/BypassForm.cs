using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AppCNC
{
    public partial class BypassForm : Form
    {
        public BypassForm(List<SwitchingNode> SwitchingNodeList, double[,] matrix, int uzel)
        {
            InitializeComponent();
            FillDataGrid(SwitchingNodeList, matrix, uzel);
        }

        private void FillDataGrid(List<SwitchingNode> SwitchingNodeList, double[,] matrix, int uzel)
        {
            int n = SwitchingNodeList.Count;
            dataGridView1.RowCount = 1;
            dataGridView1.ColumnCount = n;
            DijkstraAlgorithm dij = new DijkstraAlgorithm(n);
            double[] dijmas = dij.Dijkstra(matrix, uzel);
            dataGridView1.Rows[0].HeaderCell.Value = SwitchingNodeList[uzel].getName();
            for (int i = 0; i < n; i++)
            {
                dataGridView1.Columns[i].HeaderCell.Value = SwitchingNodeList[i].getName();
                dataGridView1.Rows[0].Cells[i].Value = dijmas[i];
            }
        }
    }
}
