/*
имеется  ряд плиток - чёрных и белых, входные данные - цвет плитки
необходимо сделать эту цепочку чередующейчя - ч б ч б ч б
можно перекрашивать плитки в угоду цели
За какое наименьшее число перекрашиваний можно получить черед.последовательность?
*/
/*
#include <iostream>
using namespace std;




const int num=10;

int main() {
    char str[num];
    cin.getline(str, num);
    int kB=0, kW=0;
    // BLACK
    if (str[0]=='B'){
        for(int i=0; i<num;i+2){
            if (str[i]!='B' && str[i+1]=='W'){
                kB++;
            }
            if (str[i]=='B' && str[i+1]!='W'){
                kB++;
            }
            if (str[i]!='B' && str[i+1]!='W'){
                kB=kB+2;
            }
        }
        cout<<kB;
    }

    // WIGHT
    if (str[0]=='W'){
        for(int i=0; i<num;i+2){
            if (str[i]!='W' && str[i+1]=='B'){
                kW++;
            }
            if (str[i]=='W' && str[i+1]!='B'){
                kW++;
            }
            if (str[i]!='W' && str[i+1]!='B'){
                kW=kW+2;
            }
        }
        cout<<kW;
    }

    return 0;
}


*/


#include <queue>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

#define fi first
#define se second

const int INF=2000000000;

typedef pair <int, int> Pair;

class GraphW{
    int n;
    vector <Pair>*e;
    int* c;

public:
    GraphW(const char*);
    void Print();
    int MinPath(int,int);
    bool Cycle();
    bool DFS(int,int);
};

int u,v;

int main(){
    GraphW g ("Graph3.TXT");
    g.Print();
    cout<<g.MinPath(u,v)<<endl;
}


bool GraphW::Cycle(){
    for(int i=0;i<n;i++){
        c[i]=0;
    }

    for(int i=0;i<n;i++){
        if (c[i]==0){
            if (DFS(i, -1)){
                return true;
            }
        }
    }

    return false;
}

bool GraphW::DFS(int u, int p){
    for (int i=0; i<e[u].size(); i++){
        if (e[u][i].fi!=p && c[e[u][i].fi]!=2){
            if (c[e[u][i].fi]==1){
                return true;
            }
            else if (DFS(e[u][i].fi,u))
                return true;
        }
    }
    c[u]=2;
    return false;
}



GraphW::GraphW(const char* fname) {
    ifstream fin(fname);
    int m;
    fin>>n>>m;
    e=new vector <Pair> [n];

    for(int i=0;i<m;i++){
        int u,v,w;
        fin>>u>>v>>w;
        u--; v--;
        Pair p;
        p.fi = v, p.se=w;
        e[u].emplace_back(p);
        p.fi = u;
        e[v].emplace_back(p);
    }
    fin.close();

}

void GraphW::Print(){
    cout<<n<<endl;
    for(int i=0; i<n;i++){
        cout<<i+1<<" :";
        for (int j=0;j<e[i].size(); j++){
            cout<<" "<<e[i][j].fi+1<<"["<<e[i][j].se<<"]";
        }
    }
}

int GraphW::MinPath(int, int) {
    int* d = new int [n];
    for (int i=0; i<n; i++){
        d[i]=INF;
    }
    d[u]=0;
    queue <int> q;
    q.push(u);

    while(!q.empty()){
        u=q.front(); q.pop();
        for (int j=0; j<e[u].size(); j++){
            if (d[u]+e[u][j].se < d[e[u][j].fi]){
                d[e[u][j].fi]=d[u]+e[u][j].se;
                q.push(e[u][j].fi);
            }
        }
    }

    for(int i=0;i<n;i++){
        cout<<i+1<<"("<<d[i]<<")";
    }

    return d[v];
}