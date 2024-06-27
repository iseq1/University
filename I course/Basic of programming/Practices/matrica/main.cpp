#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "Russian");


   // ѕеремножение двух произвольных матриц!

   //создание двумерного динамичексого массива   !A!

   double rows, cols, a;
   cout<<"¬ведите количество строк и столбцов матрицы \"A\": ";
   cin>>rows>>cols ;
   double** mas=new double* [rows];
   for (int i=0; i<rows; i++) {
       mas[i]=new double[cols];
   }

   //заполнение двумерного динамического массива !A!

   cout<<"¬ведите элементы матрицы \"A\": ";
   for (int i=0; i<rows; i++) {
       for (int j=-0; j<cols; j++) {
           cin>>a;
           mas[i][j] = {a};
       }
   }

   //¬ывод двумерного динамического массива !A!

   cout<<"ѕолученаа€ матрица \"A\": "<<endl;
   for (int i=0; i<rows; i++) {
       for (int j=-0; j<cols; j++) {
           cout<<mas[i][j]<<" ";
       }
       cout<<endl;
   }
   cout<<endl;
   //создание двумерного динамичексого массива !B!

   double rowss, colss, aa;
   cout<<"¬ведите количество строк и столбцов матрицы \"B\": ";
   cin>>rowss>>colss ;
   double** mass=new double* [rowss];
   for (int i=0; i<rowss; i++) {
       mass[i]=new double[colss];
   }

   //заполнение двумерного динамического массива !B!

   cout<<"¬ведите элемент матрицы \"B\": ";
   for (int i=0; i<rowss; i++) {
       for (int j=-0; j<colss; j++) {
           cin>>aa;
           mass[i][j] = {aa};
       }
   }

   //¬ывод двумерного динамического массива !B!

   cout<<"ѕолученаа€ матрица \"B\": "<<endl;
   for (int i=0; i<rowss; i++) {
       for (int j=-0; j<colss; j++) {
           cout<<mass[i][j]<<" ";
       }
       cout<<endl;
   }
   cout<<endl;
   // —оздание матрицы, равной перемножунию матриц ј и ¬

   double**c=new double*[rows];
   for (int i=0; i<rows; i++) {
       c[i]=new double[colss];
       for (int j=0; j<colss; j++) {
           c[i][j]=0;
           for (int k=0; k<cols; k++) {
               c[i][j] += mas[i][k] * mass[k][j];
           }
       }
   }

   //  ¬ывод матрицы-произведени€

   cout<<"ѕроизведение матриц \"A\" и \"B\": "<<endl;
   for (int i=0; i<rows; i++) {
       for (int j=0; j <colss; j++) {
           cout<<c[i][j]<<" ";
       }
       cout<<endl;
   }





   //удаление динамической пам€ти в двумерном динамическом массиве !A!

   for (int i=0; i<rows; i++) {
       delete[]mas[i];
   }
   delete[]mas;

   //удаление динамической пам€ти в двумерном динамическом массиве !B!

   for (int i=0; i<rowss; i++) {
       delete[]mass[i];
   }
   delete[]mass;

   //удаление динамической пам€ти в двумерном динамическом массиве !C!

   for (int i=0; i<rowss; i++) {
       delete[]c[i];
   }
   delete[]c;
   }

    /*

    //¬озведение матрицы в квадрат ( UPD: любую степень )

    //создание двумерного динамичексого массива   !A!

    double rows, cols, a;
    cout << "¬ведите количество строк и столбцов матрицы \"A\": ";
    cin >> rows >> cols;
    double **mas = new double *[rows];
    for (int i = 0; i < rows; i++) {
        mas[i] = new double[cols];
    }

//заполнение двумерного динамического массива !A!

    cout << "¬ведите элементы матрицы \"A\": ";
    for (int i = 0; i < rows; i++) {
        for (int j = -0; j < cols; j++) {
            cin >> a;
            mas[i][j] = {a};
        }
    }

//¬ывод двумерного динамического массива !A!

    cout << "ѕолученаа€ матрица \"A\": " << endl;
    for (int i = 0; i < rows; i++) {
        for (int j = -0; j < cols; j++) {
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;

    int n,k;
    cout<<"¬ведите значение числа \"n\" (степень): ";
    cin>>n;
    k=1;
    while (k<n) {
        // —оздание матрицы, равной перемножунию матриц ј и ¬

        double**c=new double*[rows];
        for (int i=0; i<rows; i++) {
            c[i]=new double[cols];
            for (int j=0; j<cols; j++) {
                c[i][j]=0;
                for (int k=0; k<cols; k++) {
                    c[i][j] += mas[i][k] * mas[k][j];
                }
            }
        }

        //  ¬ывод матрицы-произведени€

        cout<<"ћатрица \"A\" в степени "<<k+1<<" равна: "<<endl;
        for (int i=0; i<rows; i++) {
            for (int j=0; j <cols; j++) {
                cout<<c[i][j]<<" ";
            }
            cout<<endl;
        }

        //удаление динамической пам€ти в двумерном динамическом массиве !C!

        for (int i=0; i<rows; i++) {
            delete[]c[i];
        }
        delete[]c;

        k=k+1;
    }

    //удаление динамической пам€ти в двумерном динамическом массиве !A!

    for (int i=0; i<rows; i++) {
        delete[]mas[i];
    }
    delete[]mas;
*/