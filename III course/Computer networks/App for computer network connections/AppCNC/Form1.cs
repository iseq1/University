using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using ZedGraph;

namespace AppCNC
{
    public partial class Form1 : Form
    {
        private bool isNodeSelected = false;
        private SwitchingNode selectedNode;
        private PointPair selectedNodeOriginalPosition; 
        List<SwitchingNode> SwitchingNodeList = new List<SwitchingNode>();
        PointPairList SwitchingNodeListDraw = new PointPairList();
        PointPairList LinkList = new PointPairList();

        public Form1()
        {
            InitializeComponent();
            CreateGraph();
            numericChangeDelete.ValueChanged += NumericChangeDelete_ValueChanged;
            //DataGridAddPage();
        }

      

        private void CreateGraph()
        {
            GraphPane graphPane = zedGraphControl1.GraphPane;
            // Добавляем точки на график
            LineItem nodeCurve = graphPane.AddCurve("Узел", SwitchingNodeListDraw, Color.Blue, SymbolType.Circle);
            graphPane.Title.Text = "Связь узлов";
            graphPane.AddCurve("Связь", LinkList, Color.Red, SymbolType.None);
            Legend myLegend = new Legend();
            myLegend.IsVisible = true;
            myLegend.Position = LegendPos.InsideTopRight; // Положение легенды на графике
            
            graphPane.Legend.IsVisible = true;
            graphPane.Legend.Position = LegendPos.InsideTopRight;
            graphPane.Legend.FontSpec.Size = 12;

                

            // Добавляем созданную легенду на график
            zedGraphControl1.MasterPane[0].Margin.Top = (int)(graphPane.Legend.FontSpec.Size * 1.5);
            zedGraphControl1.IsShowPointValues = true;
            zedGraphControl1.IsSynchronizeXAxes = true;
            zedGraphControl1.IsSynchronizeYAxes = true;

            

            // Обновляем график
            graphPane.XAxis.Scale.Max = 100;
            graphPane.YAxis.Scale.Max = 100;
            zedGraphControl1.AxisChange();
            zedGraphControl1.Invalidate();
        }
      
        private void NodeUpDown_ValueChanged(object sender, EventArgs e)
        {
            
            try
            {
                

                
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при изменении узла: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            
        }

        private void Fill_NodeUpDown()
        {
            NodeUpDown.Items.Clear();
            foreach (var item in SwitchingNodeList)
            {
                NodeUpDown.Items.Add(item.ToString());
            }
        }

        private void NumericChangeDelete_ValueChanged(object sender, EventArgs e)
        {
            try
            {
                if (Convert.ToInt32(numericChangeDelete.Value - 1)>=SwitchingNodeList.Count)
                {
                    numericChangeDelete.Value = SwitchingNodeList.Count;
                    throw new Exception("Вы не можете выбрать для изменения не существующий узел!");
                }
                if (Convert.ToInt32(numericChangeDelete.Value - 1) < 0)
                {
                    numericChangeDelete.Value = 1;
                    throw new Exception("Вы не можете выбрать для изменения не существующий узел!");
                }
             
                NewNameNode.Text = SwitchingNodeList[Convert.ToInt32(numericChangeDelete.Value - 1)].getName();
                NewX.Text = Convert.ToString(SwitchingNodeList[Convert.ToInt32(numericChangeDelete.Value - 1)].getCoords().X);
                NewY.Text = Convert.ToString(SwitchingNodeList[Convert.ToInt32(numericChangeDelete.Value - 1)].getCoords().Y);
                NewWeight.Text = Convert.ToString(SwitchingNodeList[Convert.ToInt32(numericChangeDelete.Value - 1)].getWeight());
                bandwidthCBCHANGE.Text = Convert.ToString(SwitchingNodeList[Convert.ToInt32(numericChangeDelete.Value - 1)].getBandwidth());
                speedCBCHANGE.Text = "Мбит/с";
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при изменении узла: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void AddNode_Click(object sender, EventArgs e)
        {
            try
            {
               
                string pattern = @"^\d+$";
               
                if (AddX.Text.Length < 1 || AddY.Text.Length < 1 || AddName.Text.Length < 1 ||
                    !Regex.IsMatch(AddX.Text, pattern) || !Regex.IsMatch(AddY.Text, pattern) /*|| !Regex.IsMatch(AddName.Text, pattern2)*/)
                {
                    throw new Exception("Данные узла заданы некорректно!");
                }

                zedGraphControl1.GraphPane.XAxis.Scale.MinAuto = false;
                zedGraphControl1.GraphPane.XAxis.Scale.MaxAuto = false;
                zedGraphControl1.GraphPane.YAxis.Scale.MinAuto = false;
                zedGraphControl1.GraphPane.YAxis.Scale.MaxAuto = false;
                zedGraphControl1.GraphPane.AxisChange();

                double speed = 1;
                if (SpeedCB.Text == "Кбит/с")
                {
                    speed = speed / 1024;
                }
                if (SpeedCB.Text == "Гбит/с")
                {
                    speed = speed * 1024;
                }


                SwitchingNode Node = new SwitchingNode(new PointPair(Convert.ToDouble(AddX.Text), Convert.ToDouble(AddY.Text)), AddName.Text, Convert.ToDouble(AddWeight.Text), Math.Round(Convert.ToDouble(bandwidthCB.Text)*speed,2));
                SwitchingNodeList.Add(Node);
                AddToComboBoxs(Node);
                //matrGruz = CreateNagruzkiyMatrix();
                MessageBox.Show("Узел успешно добавлен!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch(Exception ex)
            {
                MessageBox.Show("Ошибка при добавлении узла: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void UpdateCanvasBttn_Click(object sender, EventArgs e)
        {
            SwitchingNodeListDraw.Clear();
            LinkList.Clear();
            foreach (var item in SwitchingNodeList)
            {
                SwitchingNodeListDraw.Add(item.getCoords());
                SwitchingNodeListDraw.Add(Double.NaN, Double.NaN);
                for(int i = 0; i < item.getLinklist().Count; i++)
                {
                    LinkList.Add(item.getCoords());
                    LinkList.Add(item.getLinklist(i).getCoords());
                    LinkList.Add(new PointPair(Double.NaN, Double.NaN));
                }
            }
            zedGraphControl1.AxisChange();
            zedGraphControl1.Invalidate();
            //CreateAdjacencyMatrix();
            Fill_NodeUpDown();
            FillDataGrid();
            MessageBox.Show("Полотно успешно обновленно!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void DeleteNodeBttn_Click(object sender, EventArgs e)
        {
            try
            {
                if (NewNameNode.Text == string.Empty || NewX.Text == string.Empty || NewY.Text == string.Empty)
                {
                    throw new Exception("Некорректно веденная информация");
                }
                var selectedValue = numericChangeDelete.Value;
                DeleteFromComboBox(SwitchingNodeList[Convert.ToInt32(selectedValue - 1)]);
                foreach (var item in SwitchingNodeList)
                {
                    if (item.getLinklist().Contains(SwitchingNodeList[Convert.ToInt32(selectedValue - 1)]))
                    {
                        item.getLinklist().Remove(SwitchingNodeList[Convert.ToInt32(selectedValue - 1)]);
                    }
                }
                SwitchingNodeList.RemoveAt(Convert.ToInt32(selectedValue - 1));
                UpdateComboBox();
                UpdateCanvasBttn_Click(sender, e);
                MessageBox.Show("Узел успешно удалён!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch(Exception ex)
            {
                MessageBox.Show("Ошибка при удалении узла: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ChangeNodeBttn_Click(object sender, EventArgs e)
        {
            decimal selectedValue = numericChangeDelete.Value;
            SwitchingNodeList[Convert.ToInt32(selectedValue - 1)].setName(NewNameNode.Text);
            SwitchingNodeList[Convert.ToInt32(selectedValue - 1)].setCoords(new PointPair(Convert.ToDouble(NewX.Text), Convert.ToDouble(NewY.Text)));
            SwitchingNodeList[Convert.ToInt32(selectedValue - 1)].setWeight(Convert.ToDouble(NewWeight.Text));
            double speed = 1;
            if (speedCBCHANGE.Text == "Кбит/с")
            {
                speed /= 1024;
            }
            if (speedCBCHANGE.Text == "Гбит/с")
            {
                speed = 1024;
            }
            SwitchingNodeList[Convert.ToInt32(selectedValue - 1)].setBandwidth(Math.Round(Convert.ToDouble(bandwidthCBCHANGE.Text) * speed, 2));
            UpdateComboBox();
            UpdateCanvasBttn_Click(sender, e);
            MessageBox.Show("Узел успешно изменён!", "Успех", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void AddToComboBoxs(SwitchingNode Node)
        {
            FirstMakeLinkComboBox.Items.Add(Node.ToString());
            SecondMakeLinkComboBox.Items.Add(Node.ToString());
            FirstDeleteLinkcomboBox.Items.Add(Node.ToString());
            FirstMatrGruzCB.Items.Add(Node.ToString());
            SecondMatrGruzCB.Items.Add(Node.ToString());
            //SecondDeleteLinkComboBox.Items.Add(Node.ToString());

        }

        private void UpdateComboBox()
        {
            FirstMakeLinkComboBox.Items.Clear();
            SecondMakeLinkComboBox.Items.Clear();
            FirstDeleteLinkcomboBox.Items.Clear();
            FirstMatrGruzCB.Items.Clear();
            foreach (var item in SwitchingNodeList)
            {
                FirstMakeLinkComboBox.Items.Add(item.ToString());
                SecondMakeLinkComboBox.Items.Add(item.ToString());
                FirstDeleteLinkcomboBox.Items.Add(item.ToString());
                FirstMatrGruzCB.Items.Add(item.ToString());
            }
        }
        
        private void DeleteFromComboBox(SwitchingNode Node)
        {
            FirstMakeLinkComboBox.Items.Remove(Node.ToString());
            SecondMakeLinkComboBox.Items.Remove(Node.ToString());
            FirstDeleteLinkcomboBox.Items.Remove(Node.ToString());
            //SecondDeleteLinkComboBox.Items.Remove(Node.ToString());
        }
        private void FirstDeleteLinkcomboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            SecondDeleteLinkComboBox.Items.Clear();
            var unit = FirstDeleteLinkcomboBox.SelectedItem;
            try
            {
              
                foreach(var item in SwitchingNodeList)
                {
                    if (unit.ToString() == item.ToString())
                    {
                        if (item.getLinklist().Count == 0)
                        {
                            throw new Exception("У данного узла нет связей!");
                        }

                        for (int i = 0; i < item.getLinklist().Count; i++)
                        {
                            SecondDeleteLinkComboBox.Items.Add(item.getLinklist(i).ToString());
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при удалении связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void MakeLinkBttn_Click(object sender, EventArgs e)
        {
            try
            {
                if (FirstMakeLinkComboBox.SelectedIndex == -1 || SecondMakeLinkComboBox.SelectedIndex == -1)
                {
                    throw new Exception("Вам необходимо корректно выбрать узлы для связи!");
                }
                if (FirstMakeLinkComboBox.SelectedItem.ToString() == SecondMakeLinkComboBox.SelectedItem.ToString())
                {
                    throw new Exception("Вы не можете установить связь между одним и тем же узлом!");
                }

                double firstSpeed = 1;
                if (FirstSpeedCB.Text == "Кбит/с")
                {
                    firstSpeed /= 1024;
                }
                if (FirstSpeedCB.Text == "Гбит/с")
                {
                    firstSpeed = 1024;
                }

                double secondSpeed = 1;
                if (SecondSpeedCB.Text == "Кбит/с")
                {
                    secondSpeed /= 1024;
                }
                if (SecondSpeedCB.Text == "Гбит/с")
                {
                    secondSpeed = 1024;
                }

                foreach (var item in SwitchingNodeList)
                {
                    if (item.ToString() == FirstMakeLinkComboBox.SelectedItem.ToString())
                    {
                        foreach (var item2 in SwitchingNodeList)
                        {
                            if (item2.ToString() == SecondMakeLinkComboBox.SelectedItem.ToString())
                            {
                                if (item.getLinklist().Contains(item2))
                                {
                                    throw new Exception("Между данными узлами связь уже установлена!");
                                }
                                item.setLinklist(item2);
                                item.setDataFlowlist(new DataFlow(Convert.ToDouble(firstDataFlowCB.Text)*firstSpeed));
                                //MessageBox.Show("" + item.getDataFlowlist(0));
                                item2.setLinklist(item);
                                item2.setDataFlowlist(new DataFlow(Convert.ToDouble(SecondDataFlowCB.Text) * secondSpeed));
                                //MessageBox.Show("" + item2.getDataFlowlist(0));
                                
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при установке связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void DeleteLinkBttn_Click(object sender, EventArgs e)
        {
            try
            {
                if (FirstDeleteLinkcomboBox.SelectedIndex == -1 || SecondDeleteLinkComboBox.SelectedIndex == -1)
                {
                    throw new Exception("Вам необходимо корректно выбрать узлы для удаления связи!");
                }
                int i = -1;
                int j = -1;
                foreach (var item in SwitchingNodeList)
                {
                    i++;
                    if (item.ToString() == FirstDeleteLinkcomboBox.SelectedItem.ToString())
                    {
                        foreach (var item2 in SwitchingNodeList)
                        {
                            j++;
                            if (item2.ToString() == SecondDeleteLinkComboBox.SelectedItem.ToString())
                            {
                                if (!item.getLinklist().Contains(item2))
                                {
                                    throw new Exception("Между данными узлами связь уже удалена!");
                                }
                                
                                item.getLinklist().Remove(item2);
                                item.getDataFlowlist().Remove(item.getDataFlowlist(j));
                                item2.getLinklist().Remove(item);
                                item2.getDataFlowlist().Remove(item2.getDataFlowlist(i));
                                
                            }
                        }
                    }
                }
                UpdateComboBox();
                UpdateCanvasBttn_Click(sender, e);
            }

            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при удалении связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        
        private void ZedGraphControl1_MouseClick(object sender, MouseEventArgs e)
        {
        
            GraphPane graphPane = zedGraphControl1.GraphPane;
            if (e.Button == MouseButtons.Left)
            {
                double x, y;
                graphPane.ReverseTransform(new PointF(e.X, e.Y), out x, out y);
                SwitchingNode Node = FindNodeAtCoordinates(x, y);
                if (Node==null && !isNodeSelected)
                {
                    //добавляем узел
                    SwitchingNode newNode = new SwitchingNode(new PointPair(Math.Round(x, 2), Math.Round(y, 2)), "Безымянный " + (SwitchingNodeList.Count+1), 1, 1);
                    SwitchingNodeList.Add(newNode);
                    AddToComboBoxs(newNode);
                }
                else if (Node!=null && !isNodeSelected)
                { 
                    //выбранный узел готовим для перемещения
                    selectedNode = Node;
                    selectedNodeOriginalPosition = new PointPair(Node.getCoords().X, Node.getCoords().Y);
                    isNodeSelected = true;
                }
                else if (Node==null && isNodeSelected)
                {
                    //принимаем новые координаты и перемещаем узел
                    double dx = x - selectedNodeOriginalPosition.X;
                    double dy = y - selectedNodeOriginalPosition.Y;
                    foreach (var item in SwitchingNodeList)
                    {
                        if (item == selectedNode)
                            item.setCoords(new PointPair(selectedNodeOriginalPosition.X + dx, selectedNodeOriginalPosition.Y + dy));
                    }
                    isNodeSelected = false;
                }
                else if (Node!=null && isNodeSelected)
                {
                   
                    //устанавливаем связь между двумя узлами
                    SwitchingNode secondNode = Node;
                    foreach (SwitchingNode item in SwitchingNodeList)
                    {
                        if (item == selectedNode)
                        {
                            foreach (SwitchingNode item2 in SwitchingNodeList)
                            {
                                if (item2 == secondNode)
                                {
                                    try
                                    {
                                        if(item == item2)
                                        {
                                            throw new Exception("Нельзя установить связь между одним узлом!");
                                        }
                                        // надо добавить обработчик события установления связи
                                        item.setLinklist(item2);
                                        item.setDataFlowlist(new DataFlow(1));
                                        //MessageBox.Show("" + item.getDataFlowlist(0));
                                        item2.setLinklist(item);
                                        item2.setDataFlowlist(new DataFlow(1));
                                        UpdateComboBox();
                                        UpdateCanvasBttn_Click(sender, e);
                                        break;
                                    }
                                    catch(Exception ex)
                                    {
                                        MessageBox.Show("Ошибка при создании связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                                    }
                                }
                            }
                        }
                    }
                    UpdateComboBox();
                    isNodeSelected = false;
                }
            }

            // Пересчитываем только ось X
            zedGraphControl1.GraphPane.XAxis.Scale.MinAuto = false;
            zedGraphControl1.GraphPane.XAxis.Scale.MaxAuto = false;
            zedGraphControl1.GraphPane.YAxis.Scale.MinAuto = false;
            zedGraphControl1.GraphPane.YAxis.Scale.MaxAuto = false;
            zedGraphControl1.GraphPane.AxisChange();
            UpdateCanvasBttn_Click(sender, e);
        }
        
        private SwitchingNode FindNodeAtCoordinates(double x, double y)
        {
            foreach (SwitchingNode item in SwitchingNodeList)
            {
                
                double minx = x - x * 0.05;
                double maxx = x + x * 0.05;
                double miny = y - y * 0.05;
                double maxy = y + y * 0.05;
                if ((minx <= item.getCoords().X  && item.getCoords().X <= maxx) && 
                    (miny <= item.getCoords().Y && item.getCoords().Y <= maxy))
                {
                    MessageBox.Show("Узел найден!");
                    return item;
                }
           
            }
            return null;
        }

        private double[,] CreateAdjacencyMatrix(bool weight)
        {
            
            if (weight)
            {
                int n = SwitchingNodeList.Count;
                double[,] mas = new double[n, n];
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        mas[i, j] = 0;
                    }
                    List<SwitchingNode> temp = SwitchingNodeList[i].getLinklist();
                    foreach (SwitchingNode item in temp)
                    {
                        int index = SwitchingNodeList.FindIndex(node => node == item);
                        mas[i, index] = 1;
                    }
                }
                
                return mas;
            }
            else
            {
                int n = SwitchingNodeList.Count;
                double[,] mas = new double[n, n];
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        mas[i, j] = 0;
                    }
                    List<SwitchingNode> temp = SwitchingNodeList[i].getLinklist();
                    foreach (SwitchingNode item in temp)
                    {
                        int index = SwitchingNodeList.FindIndex(node => node == item);
                        mas[i, index] = 1;
                    }
                    
                }
                
                return mas;
            }

            
        }

        private void GoToMainPage()
        {
            //переход на mainform
            TabPage myTabPage = tabControl1.TabPages["tabPage1"];
            tabControl1.SelectedTab = myTabPage;

        }

        private void FillDataGrid()
        {
            
            int n = SwitchingNodeList.Count;
            if (n > 0)
            {
                double[,] mas = CreateAdjacencyMatrix(true);

                dataGridView1.RowCount = n;
                dataGridView1.ColumnCount = n;

                dataGridView2.RowCount = n;
                dataGridView2.ColumnCount = n;

                dataGridView3.RowCount = n;
                dataGridView3.ColumnCount = n;
                for (int i = 0; i < n; i++)
                {
                    dataGridView1.Rows[i].HeaderCell.Value = SwitchingNodeList[i].getName();
                    dataGridView1.Columns[i].HeaderCell.Value = SwitchingNodeList[i].getName();

                    dataGridView2.Rows[i].HeaderCell.Value = SwitchingNodeList[i].getName();
                    dataGridView2.Columns[i].HeaderCell.Value = SwitchingNodeList[i].getName();

                    dataGridView3.Rows[i].HeaderCell.Value = SwitchingNodeList[i].getName();
                    dataGridView3.Columns[i].HeaderCell.Value = SwitchingNodeList[i].getName();

                    for (int j = 0; j < n; j++)
                    {
                        dataGridView1.Rows[i].Cells[j].Value = mas[i, j];
                        dataGridView2.Rows[i].Cells[j].Value = mas[i, j];
                        
                    }
                }
            }
        }



        private void DijkstraBttn_Click(object sender, EventArgs e)
        {
            try 
            {
                int n = SwitchingNodeList.Count();
                double[,] matrGruz = new double[n, n];
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        matrGruz[i, j] = Convert.ToDouble(dataGridView3.Rows[i].Cells[j].Value);
                    }
                }
                
                Form BypassForm = new BypassForm(SwitchingNodeList, matrGruz, NodeUpDown.SelectedIndex);
                BypassForm.Show();
            }
            catch(Exception ex)
            {
                MessageBox.Show("Ошибка при поиске путей: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private double[,] CreateNagruzkiyMatrix()
        {
            int n = SwitchingNodeList.Count;
            double[,] mas = new double[n, n];
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    mas[i, j] = 0;
                }
                List<SwitchingNode> temp = SwitchingNodeList[i].getLinklist();
                foreach (SwitchingNode item in temp)
                {
                    int index = SwitchingNodeList.FindIndex(node => node == item);
                    mas[i, index] = 1;
                }
            }
            return mas;
        }


        private void FirstMatrGruzCB_SelectedIndexChanged(object sender, EventArgs e)
        {
            SecondMatrGruzCB.Items.Clear();
            var unit = FirstMatrGruzCB.SelectedItem;
            try
            {
                foreach (var item in SwitchingNodeList)
                {
                    if (unit.ToString() == item.ToString())
                    {
                        if (item.getLinklist().Count == 0)
                        {
                            throw new Exception("У данного узла нет связей!");
                        }

                        for (int i = 0; i < item.getLinklist().Count; i++)
                        {
                            SecondMatrGruzCB.Items.Add(item.getLinklist(i).ToString());
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при удалении связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        Dictionary<List<int>, double> dictGruz = new Dictionary<List<int>, double>();

        private void TopologyWeightBttn_Click(object sender, EventArgs e)
        {
            try
            {
                if (FirstMatrGruzCB.SelectedIndex == -1 || SecondMatrGruzCB.SelectedIndex == -1)
                {
                    throw new Exception("Вам необходимо корректно выбрать узлы!");
                }
                if (FirstMatrGruzCB.SelectedItem.ToString() == SecondMatrGruzCB.SelectedItem.ToString())
                {
                    throw new Exception("Вы не можете выбрать один и тот же узел!");
                }

                int i = -1;
                int j = -1;
                foreach (var item in SwitchingNodeList)
                {
                    i++;
                    if (item.ToString() == FirstMatrGruzCB.SelectedItem.ToString())
                    {
                        foreach (var item2 in SwitchingNodeList)
                        {
                            j++;
                            if (item2.ToString() == SecondMatrGruzCB.SelectedItem.ToString())
                            {
                                if (!item.getLinklist().Contains(item2))
                                {
                                    throw new Exception("Между данными узлами связь уже удалена!");
                                }
                                dictGruz.Add(new List<int> {i,j}, Convert.ToDouble(TopologyWeight.Text));
                                //dictGruz.Add(new List<int> { j, i }, Convert.ToDouble(TopologyWeight.Text));
                            }
                        }
                    }
                }
                
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при установке связи между узлами: \n" + ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        

        private void UpdateMetrGruzBttn_Click(object sender, EventArgs e)
        {
            int n = SwitchingNodeList.Count();
            double[,] matrGruz = new double[n, n];
            for(int i = 0; i < n; i++)
            {
                for(int j = 0; j < n; j++)
                {
                    matrGruz[i, j] = 0;
                }
            }
            if (dictGruz.Count > 0)
            {
                foreach (var kvp in dictGruz)
                {
                    int row = kvp.Key[0];
                    int column = kvp.Key[1];
                    matrGruz[row, column] = kvp.Value;
                    matrGruz[column, row] = kvp.Value;
                }
                for (int i = 0; i < SwitchingNodeList.Count; i++)
                {
                    for (int j = 0; j < SwitchingNodeList.Count; j++)
                    {
                        dataGridView3.Rows[i].Cells[j].Value = matrGruz[i, j];
                    }
                }
            }
        }

        private void ClearMatrGruzBttn_Click(object sender, EventArgs e)
        {
            dictGruz.Clear();
            UpdateMetrGruzBttn_Click(sender, e);
        }

        private void UpdateItog_Click(object sender, EventArgs e)
        {
            dataGridView4.ColumnCount = 6;
            dataGridView4.Columns[0].Name = "V1";
            dataGridView4.Columns[1].Name = "V2";
            dataGridView4.Columns[2].Name = "Топология";
            dataGridView4.Columns[3].Name = "П/С";
            dataGridView4.Columns[4].Name = "Задержка";
            dataGridView4.Columns[5].Name = "Стоимость";

            int n = SwitchingNodeList.Count();
            double[,] matrGruz = new double[n, n];
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    matrGruz[i, j] = 0;
                }
            }
            if (dictGruz.Count > 0)
            {
                foreach (var kvp in dictGruz)
                {
                    int row = kvp.Key[0];
                    int column = kvp.Key[1];
                    matrGruz[row, column] = kvp.Value;
                    matrGruz[column, row] = kvp.Value;
                }
            }
            dataGridView4.RowCount = 1;
            int previos = 0;    
            int number = 0;
            foreach (var item in SwitchingNodeList)
            {
                dataGridView4.RowCount += item.getLinklist().Count;
                
                DijkstraAlgorithm dij = new DijkstraAlgorithm(SwitchingNodeList.Count);
                MessageBox.Show(" " + number + " " + item.getLinklist().Count);
                double[] dijmas = dij.Dijkstra(matrGruz, number);
                for (int i = previos; i< previos + item.getLinklist().Count; i++)
                {
                    dataGridView4.Rows[i].Cells[0].Value = item.getName();
                    dataGridView4.Rows[i].Cells[1].Value = item.getLinklist(i-previos).getName();
                    dataGridView4.Rows[i].Cells[2].Value = dijmas[i-previos+1];
                    
                    /*dataGridView4.Rows[i].Cells[3].Value = item.getLinklist(i).getName();
                    dataGridView4.Rows[i].Cells[4].Value = item.getLinklist(i).getName();
                    dataGridView4.Rows[i].Cells[5].Value = item.getLinklist(i).getName();*/
                    
                }
                number++;
                previos += item.getLinklist().Count;
            }
        }
    }
}
