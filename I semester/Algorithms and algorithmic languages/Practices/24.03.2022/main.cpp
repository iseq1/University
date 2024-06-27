// Зачем данную задачу реализовывать через класс, если проще её сделать просто через вспомогательные функции внутри main ?


#include <iostream>
#include <fstream>
using namespace std;
/*
class Map {
    char mapp[4][4];
    char PrintMap(char mapp[4][4]);


public:
    void ReadTextFile(char *file, int n, int m);

};

void Map::ReadTextFile(char *file, int n, int m) {
    ifstream fin(file);
    if (!fin.is_open()) return;
    while (!fin.eof()) {
        char a;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                fin >> a;
                mapp[i][j]=a;
            }
        }
    }
    cout << endl;
    fin.close();
}
char Map::PrintMap(char mapp[4][4]) {
    for(int i=0; i<4;i++){
        for(int j=0; j<4; j++){
            cout<<mapp[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}

*/


void ReadTextFile(char *file, int n, int m, char map[m][n]) {
    ifstream fin(file);
    if (!fin.is_open()) return;
    while (!fin.eof()) {
        char a;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                fin >> a;
                map[i][j]=a;
            }
        }
    }
    cout << endl;
    fin.close();
}





int main() {
    setlocale(LC_ALL, "ru");
    cout<<"Введите размерномть карты: "; int m,n; cin>>m>>n;
    /*Map map;
    map.ReadTextFile("D://project under development/C++ proj/algorithms and algorithmic languages 2021-2022/24.03.2022/1.txt", m, n);
    */
    char map[m][n];
    ReadTextFile("D://project under development/C++ proj/algorithms and algorithmic languages 2021-2022/24.03.2022/1.txt", m, n, char map[m][n]);



}
