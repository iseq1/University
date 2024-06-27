#include <iostream>
using namespace std;
int main() {
    int z,x,e,p;
    cin>>p;
    int* mas=new int[p];
    for (x=0; x<p; x++) {
        cin>>z;
        mas[x] = { z };
    }
    e=0;
    for (int q=0; q<p; q++) {
        for ( int w=0; w<p; w++) {
            if (mas[q]<mas[w]) {
                e=mas[q];
                mas[q]=mas[w];
                mas[w]=e;
            }
        }
    }
    for (int l=0; l<p; l++) {
        cout<<mas[l]<<" ";
    }
    delete[]mas;
    return 0;
}
