using System;
using System.Collections.Generic;
using ZedGraph;

namespace AppCNC
{
    public class SwitchingNode
    {
        private string name;
        private PointPair coordinates;
        private double weight;
        private List<SwitchingNode> linklist;
        private List<DataFlow> dataFlows;
        private double bandwidth;


        public SwitchingNode(PointPair coordinates)
        {
            this.coordinates = new PointPair(Math.Round(coordinates.X, 2), Math.Round(coordinates.Y, 2));
            name = "Безымянный";
            weight = 1;
            linklist = new List<SwitchingNode>();
            dataFlows = new List<DataFlow>();
            bandwidth = 1;
        }

        public SwitchingNode(PointPair coordinates, string name)
        {
            this.coordinates = new PointPair(Math.Round(coordinates.X, 2), Math.Round(coordinates.Y, 2));
            this.name = name;
            weight = 1;
            linklist = new List<SwitchingNode>();
            dataFlows = new List<DataFlow>();
            bandwidth = 1;
        }

        public SwitchingNode(PointPair coordinates, string name, double weight)
        {
            this.coordinates = new PointPair(Math.Round(coordinates.X, 2), Math.Round(coordinates.Y, 2));
            this.name = name;
            this.weight = weight;
            linklist = new List<SwitchingNode>();
            dataFlows = new List<DataFlow>();
            bandwidth = 1;
        }

        public SwitchingNode(PointPair coordinates, string name, double weight, double bandwidth)
        {
            this.coordinates = new PointPair(Math.Round(coordinates.X, 2), Math.Round(coordinates.Y, 2));
            this.name = name;
            this.weight = weight;
            linklist = new List<SwitchingNode>();
            dataFlows = new List<DataFlow>();
            this.bandwidth = bandwidth;
        }

        public PointPair getCoords()
        {
            return coordinates;
        }

        public string getName()
        {
            return name;
        }
        public double getWeight()
        {
            return weight;
        }

        public void setCoords(PointPair coord)
        {
            coordinates = new PointPair(Math.Round(coord.X, 2), Math.Round(coord.Y, 2));
        }
        public void setName(string name)
        {
            this.name = name;
        }

        public void setWeight(double weight)
        {
            this.weight = weight;
        }
        public double getBandwidth()
        {
            return bandwidth;
        }
        public void setBandwidth(double bandwidth)
        {
            this.bandwidth = bandwidth;
        }

        public List<SwitchingNode> getLinklist()
        {
            return linklist;
        }

        public SwitchingNode getLinklist(int i)
        {
            return linklist[i];
        }
        public void setLinklist(List<SwitchingNode> array)
        {
            linklist = array;
        }
        public void setLinklist(SwitchingNode node)
        {
            linklist.Add(node);
        }

        public void setLinklist(SwitchingNode node, int i)
        {
            linklist[i] = node;
        }

        public List<DataFlow> getDataFlowlist()
        {
            return dataFlows;
        }

        public DataFlow getDataFlowlist(int i)
        {
            return dataFlows[i];
        }

        public void setDataFlowlist(List<DataFlow> array)
        {
            dataFlows = array;
        }
        public void setDataFlowlist(DataFlow node)
        {
            dataFlows.Add(node);
        }

        public void setDataFlowlist(DataFlow node, int i)
        {
            dataFlows[i] = node;
        }

        public override string ToString()
        {
            return string.Format("\"{0}\" Node: [{1}; {2}]", name, Math.Round(coordinates.X,2).ToString(), Math.Round(coordinates.Y, 2).ToString());
        }
    }
}
