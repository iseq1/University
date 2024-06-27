#include <iostream>
using namespace std;
int main() {
    int a,b,e;
    cout<<"Kol-vo v massive: ";
    cin>>a;
    int* mas=new int[a];
    for (int x=0; x<a; x++) {
        cout<<"Element massiva: ";
        cin>>b;
        mas[x] = { b };
    }
    for (int c=0; c<a; c++) {
        cout << mas[c] << " ";
    }
    cout<<endl;
    for (int z=1; z<a; z++) {
        e=0;
        if (mas[z-1]>mas[z]) {
            e=mas[z];
            mas[z]=mas[z-1];
            mas[z-1]=e;
        }
    }
    for (int c=0; c<a; c++) {
        cout<<mas[c]<<" ";
    }
    delete[]mas;
    return 0;
}
