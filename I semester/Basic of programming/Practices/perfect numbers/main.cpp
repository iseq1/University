#include <iostream>
using namespace std;
//Соверше́нное число́ — натуральное число, равное сумме всех своих
// собственных делителей (то есть всех положительных делителей,
// отличных от самого́ числа).
int main() {
    int a,b,z,x,c,q,w,e,r,t,y;
    cout<<"Enter the beginning of the range of numbers: ";
    cin>>a;
    cout<<"Enter the end of the range of numbers: ";
    cin>>b;
    for (a; a<b; a++) {
        q=0;
        for (int t=1; t<a; t++) {
            if (a%t==0) {
                q+=t;
            }
        }
        if (q==a) {
            cout<<q<<endl;
        }
    }
    return 0;
}