#include <iostream>
using namespace std;
int main(){
    setlocale(LC_ALL, "");
    const int SIZE = 100; int k;
    char str[SIZE];
    cout << "���������� ������� ������:\n";
    cin.get(str, SIZE);
    cout<<"������� ����: ";
    cin>>k;
    for(int i=0; i<strlen(str); i++) {
        if ((int(str[i]) >= 65 && int(str[i]) <= 90) || (int(str[i]) >= 97 && int(str[i]) <= 122)) {
            str[i] = char(int(str[i]) + k);
        }
    }
    cout<<str;
}