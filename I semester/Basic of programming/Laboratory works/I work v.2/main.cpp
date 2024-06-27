#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "Russian");
    //a<=b
    long int a,b,factK, factN, factNK, nk, pov;
    cout<<"Введите первое натуральное число: ";
    cin>>a;
    cout<<"Введите второе натуральное число: ";
    cin>>b;
    for (int z=0; z<1; z++) {
        if (a > b) {
            cout <<endl<< "Неверно введены числа!"<<endl<<"Первое число должно быть меньше или равно второму!";
            break;
        }
    }
// а=1 в=10, сначала берёт (1;1), (1;2) и т.д.; (z;x), если k^2 + n^2 = n!/k!*(n-k)! причём k<=n;
    for (int k=a; k<=b; k++) {
        for (int n=k; n<=b; n++){
            factK=1;
            for (int q=1; q<=k; q++) {
                factK*=q;
            }
            factN=1;
            for (int w=0; w<n; w++) {
                factN*=(n-w);
            }
            nk=n-k;
            factNK=1;
            for (int e=1; e<=nk; e++) {
                factNK*=e;
            }
            pov =0;
            if ( (k*k) + (n*n) == (factN/(factK*factNK)) ) {
                cout<<"Есть такие числа: "<<k<<" "<<n;
                pov+=1;
            }
            else {
                pov+=0;
            }

        }
    }
    if (pov==0) {
        cout<<"Таких чисел не нашлось!";
    }

}
//ПРИНЯЛИ 12.10.21 в 10:00 по мск;