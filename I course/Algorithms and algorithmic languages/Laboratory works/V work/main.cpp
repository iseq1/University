/*
5. В квадратной матрице размера n распечатать в виде матриц все миноры (n-1)-го порядка.
В первой строке задаётся размер матрицы n, а в последующих – сама матрица.
Поиск миноров реализовать через отдельную функцию.
Исходные данные:
2
1 2
3 4
Результат:
1 2 3 4
*/

#include <iostream>
using namespace std;

int minor(int n, double**mas) {
    //для любой квадратной матрицы NxN существует n^2 миноров (n-1) порядка
  int k; //порядковый номер минора
  k=1;
  for (int i=0; i<n; i++) {
      for (int j=0; j<n; j++) {
          cout<<endl<<k<<". ";
          for (int r=0; r<n; r++) {
              cout<<endl;
              for (int c=0; c<n;c++) {
                  if ((r!=i) && (c!=j)) {
                      cout<<mas[r][c]<<" ";
                  }
              }
          }
          cout<<endl;
          k++;
      }
  }
  return 0;
}

int main() {
    setlocale(LC_ALL, "ru");
    int n;
    cout<<"Введите количество строк и столбцов квадратной матрицы \"A\": ";
    cin>>n;
    double** mas=new double* [n];
    for (int i=0; i<n; i++) {
        mas[i]=new double[n];
    }
    cout<<"Введите элементы матрицы \"A\": ";
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            cin>>mas[i][j];
        }
    }
    cout<<"Полученаая матрица \"A\": "<<endl;
    for (int i=0; i<n; i++) {
        for (int j=0; j<n; j++) {
            cout<<mas[i][j]<<" ";
        }
        cout<<endl;
    }
    cout<<endl;
    cout<<"Миноры матррицы \"A\": "<<endl;
    minor(n,mas);

    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
    return 0;
}



/*

#include <iostream>
using namespace std;
void WriteMinor(int **a, int n, int i0, int j0);
void SearchMinors(int **a, int n);
int main() {
    srand(time(0));
    int n; cin >> n;
    int **a = new int*[n];
    for(int i = 0; i < n; i++){
        a[i] = new int[n];
        for(int j = 0; j < n; j++){
            a[i][j] = rand() % 10;
            cout << a[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;

    SearchMinors(a, n);
}
void WriteMinor(int **a, int n, int i0, int j0){
    for(int i = 0; i < n; i++){
        if(i0 == i) continue;
        for(int j = 0; j < n; j++){
            if(j0 == j) continue;
            cout << a[i][j] << " ";
        }
        cout << endl;
    }
}

void SearchMinors(int **a, int n){
    for(int i = n-1; i >= 0; i--){
        for(int j = n-1; j >= 0; j--){
            WriteMinor(a, n, i, j);
            cout << endl;
        }
    }
}

*/