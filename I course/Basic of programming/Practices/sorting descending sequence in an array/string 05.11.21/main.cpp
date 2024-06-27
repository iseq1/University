#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "rus");


//реализовать подсчет количества символов в строке.
    int n=0, numbers=0, space=0;
    char str[]="What a wonderful world 1234567890";
    cout<<"\""<<str<<"\""<<" имеет "<<sizeof(str)<<" символа!"<<endl;
    for (int i=0; i<sizeof(str); i++) {
        n++;
    }
    for (int i = 0; i<sizeof(str); i++){
        if ( (int)str[i] >= 48  && (int)str[i] <= 57)
            numbers++;
    }
    for (int i=0; i<sizeof(str); i++) {
        if( (int)str[i] == 32 ) {
            space++;
        }
    }
    cout<<"В строке \""<<str<<"\" "<<n-numbers-space<<" букв, "<<numbers<<" цифр "<<space<<" пробела!"<<endl;


//реализовать подсчет количества цифр в строке.
    cout<<endl;
    char text[] = "Hello world";
    char dest[50];
    strcpy_s(dest, text);
    cout << dest << endl;


// реалиовать сравнение двух строк.
    cout<<endl;
    int k=0;
    char str1[]="What a wonderful world";
    char str2[]="What a beautiful world";
    cout<<"Сравним "<<str1<<" и "<<str2<<endl;
    if (sizeof(str1) == sizeof(str2)) {
        cout<<"Обе строки имееют "<<sizeof(str1)<<" символов"<<endl;
        for (int i=0; i<sizeof(str1); i++) {
            if (str1[i]==str2[i]) {
                k++;
            }
        }
        cout<<"Строки \""<<str1<<"\" и \""<<str2<<"\" имеют "<<k<<" одинаковых символов";
    }
}
