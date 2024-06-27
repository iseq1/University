/*
3. В последовательности из n целых чисел найти наибольший
перепад – наибольшую разность элементовв цепочке возрастающих
или убывающих элементов. В первой строке задаётся количество чисел
в последовательности, а во второй – сами числа.
Исходные данные:

Результат:
6
*/

#include <iostream>
using namespace std;
int main() {9
    2 5 1 2 3 7 3 2 2
    setlocale(LC_ALL, "Rus");
    int n;
    cout<<"Введите число элементов в массиве, а затем и сам масив чисел: "<<endl;
    cin>>n;
    int* mas=new int [n];
    for (int i=0; i<n; i++) {
        cin>>mas[i];
    }

    // наибольшая разность в цепочке возрастающих элементов
    int first_number_up, drop_up, max_drop_up=0;
    for (int i=0; i<n; i++) {
        first_number_up=0;
        if (mas[i]<mas[i+1]) {
            first_number_up=mas[i];
            for (int j=i+1; j<n; j++) {
                drop_up=mas[j]-first_number_up;
                if (drop_up>max_drop_up) {
                    max_drop_up=drop_up;
                }
                if (mas[j]>mas[j+1] || mas[j] == mas[j+1]) {
                    break;
                }
            }
        }
    }

    // наибольшая разность в цепочке убывающих элементов
    int first_number_down, drop_down, max_drop_down=0;
    for (int i=0; i<n; i++) {
        first_number_down=0;
        if (mas[i]>mas[i+1]) {
            first_number_down=mas[i];
            for (int j=i+1; j<n; j++) {
                drop_down=first_number_down-mas[j];
                if (drop_down>max_drop_down) {
                    max_drop_down=drop_down;
                }
                if (mas[j]<mas[j+1] || mas[j] == mas[j+1]) {
                    break;
                }
            }
        }
    }

    //сравниваем два максимума и выводим больший
    int max_drop = max(max_drop_up, max_drop_down);
    cout<<endl<<"Наибольшей перепад в данной цепечоке чисел: "<<max_drop;
    delete[]mas;
}