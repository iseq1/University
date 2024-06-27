/*
6. Проверить, что в матрице 9 на 9 числа расставлены по правилам судоку:
в каждой строке, каждом столбце и в каждом фрагменте 3 на 3 встречаются все
цифры от 1 до 9. Если числа расставлены правильно, то напечатать «ДА», в противном
случае напечатать «НЕТ».
Исходные данные:
6 7 9 8 4 2 5 3 1
8 3 5 1 6 7 4 2 9
2 1 4 9 3 5 7 6 8
7 6 8 5 1 3 9 4 2
3 4 2 6 8 9 1 5 7
5 9 1 7 2 4 3 8 6
9 8 6 3 5 1 2 7 4
1 2 3 4 7 8 6 9 5
4 5 7 2 9 6 8 1 3
*/

#include <iostream>
using namespace std;

int minor(double** mas, int i, int j ) {
    int k1,k2,k3,k4,k5,k6,k7,k8,k9;
    k1=k2=k3=k4=k5=k6=k7=k8=k9=0;
    for(int a=i; a<i+3; a++){
        for (int b=j; b<j+3; b++) {
            if (mas[a][b] == 1) {
                k1 += 1;
            }
            if (mas[a][b] == 2) {
                k2 += 1;
            }
            if (mas[a][b] == 3) {
                k3 += 1;
            }
            if (mas[a][b] == 4) {
                k4 += 1;
            }
            if (mas[a][b] == 5) {
                k5 += 1;
            }
            if (mas[a][b] == 6) {
                k6 += 1;
            }
            if (mas[a][b] == 7) {
                k7 += 1;
            }
            if (mas[a][b] == 8) {
                k8 += 1;
            }
            if (mas[a][b] == 9) {
                k9 += 1;
            }
        }
    }
    if(k1==k2 && k2==k3 && k3==k4 && k4==k5 && k5==k6 && k6==k7 && k7==k8 && k8==k9 && k9==1) {
        return 1;
    }
    else return 0;
}

int stroka(int n, double**mas) {
    int k1,k2,k3,k4,k5,k6,k7,k8,k9,k=0;
    k1=k2=k3=k4=k5=k6=k7=k8=k9=0;
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            if (mas[i][j] == 1) {
                k1 += 1;
            }
            if (mas[i][j] == 2) {
                k2 += 1;
            }
            if (mas[i][j] == 3) {
                k3 += 1;
            }
            if (mas[i][j] == 4) {
                k4 += 1;
            }
            if (mas[i][j] == 5) {
                k5 += 1;
            }
            if (mas[i][j] == 6) {
                k6 += 1;
            }
            if (mas[i][j] == 7) {
                k7 += 1;
            }
            if (mas[i][j] == 8) {
                k8 += 1;
            }
            if (mas[i][j] == 9) {
                k9 += 1;
            }
        }
        if(k1==k2 && k2==k3 && k3==k4 && k4==k5 && k5==k6 && k6==k7 && k7==k8 && k8==k9 && k9==(i+1)) {
            k++;
        }
    }
    if(k==9) {
        return 1;
    }
    else return 0;
}

int stolbec(int n, double**mas) {
    int k1,k2,k3,k4,k5,k6,k7,k8,k9, k=0;
    k1=k2=k3=k4=k5=k6=k7=k8=k9=0;
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            if (mas[j][i] == 1) {
                k1 += 1;
            }
            if (mas[j][i] == 2) {
                k2 += 1;
            }
            if (mas[j][i] == 3) {
                k3 += 1;
            }
            if (mas[j][i] == 4) {
                k4 += 1;
            }
            if (mas[j][i] == 5) {
                k5 += 1;
            }
            if (mas[j][i] == 6) {
                k6 += 1;
            }
            if (mas[j][i] == 7) {
                k7 += 1;
            }
            if (mas[j][i] == 8) {
                k8 += 1;
            }
            if (mas[j][i] == 9) {
                k9 += 1;
            }
        }
        if(k1==k2 && k2==k3 && k3==k4 && k4==k5 && k5==k6 && k6==k7 && k7==k8 && k8==k9 && k9==(i+1)) {
            k++;
        }
    }
    if(k==9) {
        return 1;
    }
    else return 0;
}

int minors3_3(int n, double**mas){

    int rows=0, cols=0, k=0;
    for(int i=rows; i<n;i+=3) {
        for (int j = cols; j <n; j+=3) {
            k+=minor(mas, i, j);
        }
    }
    if (k==9) {
        return 1;
    }
    else return 0;
}

int main() {
    setlocale(LC_ALL, "ru");
    //создание двумерного динамичексого массива   !A!
    int n;
    cout<<"Введите количество строк и столбцов матрицы \"A\": ";
    cin>>n;
    double** mas=new double* [n];
    for (int i=0; i<n; i++) {
        mas[i]=new double[n];
    }
    //заполнение двумерного динамического массива !A!
    cout<<"Введите элементы матрицы \"A\": ";
    for (int i=0; i<n; i++) {
        for (int j=-0; j<n; j++) {
            cin>>mas[i][j];
        }
    }
    //Вывод двумерного динамического массива !A!
    cout<<"Полученаая матрица \"A\": "<<endl;
    for (int i=0; i<n; i++) {
        for (int j=-0; j<n; j++) {
            cout<<mas[i][j]<<" ";
        }
        cout<<endl;
    }
    cout<<endl;
   if (stroka(n,mas)*stolbec(n,mas)*minors3_3(n, mas)==1){
        cout<<"ДА";
   }
   else cout<<"НЕТ";
   return 0;
}


