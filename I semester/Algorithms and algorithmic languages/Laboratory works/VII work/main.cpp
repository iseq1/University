/*
7. Определить максимальную глубину вложения круглых скобок в некоторой формуле с правильной расстановкой скобок.
Исходные данные:
((()(())())())
Результат:
4
*/

#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "ru");
    int k=0, kmax=0;
    char*str=new char[250];
    cin.getline(str,250);
    for(int i=0; str[i]!='\0';i++) {
        if (str[i]=='(') {
            k++;
            if (k>kmax) {
                kmax=k;
            }
        }
        if (str[i]==')') {
            k--;
        }
    }

    if (k!=0){
        cout<<"Неверный ввод!"; //количессвто "(" != количеству ")"
    }
    else cout<<kmax;
}
