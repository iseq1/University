using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AppCNC
{
    class DijkstraAlgorithm
    {
        private int V;

        public DijkstraAlgorithm(int v)
        {
            V = v;
        }

        // Функция для поиска узла с минимальным расстоянием
        private int MinDistance(double[] dist, bool[] sptSet)
        {
            double min = double.MaxValue;
            int minIndex = -1;

            for (int v = 0; v < V; v++)
            {
                if (sptSet[v] == false && dist[v] <= min)
                {
                    min = dist[v];
                    minIndex = v;
                }
            }

            return minIndex;
        }
        // Функция для вычисления кратчайших путей от заданной вершины
        public double[] Dijkstra(double[,] graph, int src)
        {
            double[] dist = new double[V];
            bool[] sptSet = new bool[V];

            for (int i = 0; i < V; i++)
            {
                dist[i] = double.MaxValue;
                sptSet[i] = false;
            }

            dist[src] = 0;

            for (int count = 0; count < V - 1; count++)
            {
                int u = MinDistance(dist, sptSet);
                sptSet[u] = true;

                for (int v = 0; v < V; v++)
                {
                    if (!sptSet[v] && graph[u, v] != 0 && dist[u] != int.MaxValue && dist[u] + graph[u, v] < dist[v])
                    {
                        dist[v] = dist[u] + graph[u, v];
                    }
                }
            }

            return dist;
        }

       
    }
}
