#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL,"Russian");
    int a,b;
    cout<<"¬ведите размер массива: ";
    cin>>a;
    int* mas=new int[a];
    for (int z=0; z<a; z++) {
        cout<<"¬ведите элемент массива: ";
        cin>>b;
        mas[z] = { b };
    }
    for (int z=0; z<a; z++) {
        cout<<mas[z]<<" ";
    }
    cout<<endl;
    for (int m=0; m<a; m++) {
        int e=0;
        if (mas[m]<mas[m-1]) {
            e=mas[m];
            mas[m]=mas[m-1];
            mas[m-1]=e;
        }
    }
    for (int z=0; z<a; z++) {
        cout<<mas[z]<<" ";
    }






    delete[]mas;
    return 0;
}
