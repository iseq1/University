#include <iostream>
#include <fstream>
#include <queue>
#include <stack>
using namespace std;

int main()
{
    ifstream fin("input.txt");
    int n;
    fin >> n;
    int **mas = new int*[n];
    for (int i = 0; i < n; i++) {
        mas[i] = new int[n];
        for (int j = 0; j < n; j++) {
            fin >> mas[i][j];
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (mas[i][j] == 1) {
                for (int k = 0; k < n; k++) {
                    if (mas[k][i] == 1) {
                        mas[k][j] = 1;
                    }
                }
            }
        }
    }
    int maxWays = 0;
    int *tops = new int[n];
    for (int j = 0; j < n; j++) {
        tops[j] = 0;
        for (int i = 0; i < n; i++) {
            tops[j] += mas[i][j];
        }
        maxWays = max(maxWays, tops[j]);
    }

    for (int i = 0; i < n; i++) {
        if (tops[i] == maxWays) { cout << i + 1 << " " << endl; }
    }


}

