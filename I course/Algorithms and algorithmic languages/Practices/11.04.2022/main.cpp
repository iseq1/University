#include <iostream>
#include <fstream>
#include <queue>
#include <vector>


























































































using namespace std;
const int N=11111;

ifstream fin ("D:\\project under development\\C++ proj\\algorithms and algorithmic languages 2021-2022\\11.04.2022\\Input.txt");
ofstream fout("D:\\project under development\\C++ proj\\algorithms and algorithmic languages 2021-2022\\11.04.2022\\Output.txt");


int a[N], b[N];     //кол-во подчиненных, начальников
int p[N];          // Номер начальников
queue <int> q;
bool mark[N];

int main(){
    int n, k;
    fin>>n>>k;
    vector <vector <int> > e(n);
    for(int i=0;i<n;i++){
        int a,b;
        fin>>a>>b;
        a--; b--;
        e [a].emplace_back (b);
        e [b].emplace_back (a);
    }
    q.push(k); mark[k]=true; p[k] = -1;
    while(!q.empty()){
        int v = q.front(); q.pop();
        for (int j=0; j<e[v].size(); j++){
            if (!mark[e[v][j]]){
                mark[e[v][j]]=true;
                q.push(e[v][j]);
                p[e[v][j]]=v;
            }
        }
    }
    for(int i=0;i<n;i++){
        fout<<i+1<<" :"<< p[i]<<" =";
        for(int j=0;i<e [i].size();i++){
            fout<<" "<< e[i][j]+1;
        }
        fout<<endl;
    }
    fout.close();
    return 0;
}