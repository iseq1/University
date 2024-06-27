#include <iostream>
using namespace std;
int main() {
    int a,b,c,l;
    cout<<"Kol-vo v massive: ";
    cin>>a;
    int* mas=new int[a];
    int* sam=new int[a];
    for (int x=0; x<a; x++) {
        cin>>b;
        mas[x] = { b };
        sam[x] = { b };
    }
    for (int x=0; x<a; x++) {
        cout<<mas[x]<<" ";
    }
    cout<<endl<<"Sdvig massiva na dliny l: ";
    cin>>l;
    c=a-l;
    for (c; c<a; ++c) {
        cout<<mas[c]<<" ";
    }
    c=a-l;
    for (int y=0; y<c; y++) {
        cout<<sam[y]<<" ";
    }
    delete []mas;
    delete []sam;
    return 0;
}