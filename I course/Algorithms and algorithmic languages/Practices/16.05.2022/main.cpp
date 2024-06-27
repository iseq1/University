#include <iostream>
#include <fstream>
#include <queue>

using namespace std;

ifstream fin("Input.txt");
ofstream fout("Output.txt");

int n, m, number;
bool **POP;
int U, V;

void Tree(int);

int main()
{
    fin >> n >> m;
    //Формат ввода:  кол-во вершин, кол-во рёбер, рёбра, число откуда начинаем
    POP = new bool*[n];
    for (int i = 0; i < n; i++) {
        POP[i] = new bool[n];
        for (int j = 0; j < n; j++) {
            POP[i][j] = 0;
        }
    }
    for (int i = 0; i < m; i++) {

        fin >> U >> V;
        U--; V--;
        POP[U][V] = POP[V][U] = true;
    }
    fin >> number;
    Tree(number);

    fout.close();
    return 0;
}

void Tree(int u) {
    vector <pair<int, int>> div;
    bool *chk = new bool[n];
    for (int i = 0; i < n; i++) {
        chk[i] = 0;
    }
    chk[u] = 1;
    queue<int> q;
    q.push(u);
    while (!q.empty()) {
        u = q.front(); q.pop();
        for (int i = 0; i < n; i++) {
            if (POP[u][i] && !chk[i]) {
                chk[i] = 1;
                div.push_back(make_pair(u, i));
                q.push(i);
            }
        }
    }

    for (int i = 0; i < div.size(); i++) {
        fout << div[i].first + 1 << " " << div[i].second + 1 << endl;
    }

    fout << endl;
    return;
}