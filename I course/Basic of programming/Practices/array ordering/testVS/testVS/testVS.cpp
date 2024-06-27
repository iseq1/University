#include <iostream>
using namespace std;
int main() {
    int z, x, q, w, e, a;
    cin >> a;
    int* mas=new int[a];
    for (x = 0; x < a; x++) {
        cin >> z;
        mas[x] = { z };
    }
    e = 0;
    for (int q = 0; q < a; q++) {
        for (int w = 0; w < a; w++) {
            if (mas[q] < mas[w]) {
                e = mas[q];
                mas[q] = mas[w];
                mas[w] = e;
            }
        }
    }
    for (int l = 0; l < a; l++) {
        cout << mas[l] << " ";
    }
    delete[]mas;
    return 0;
}
