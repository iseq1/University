#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "Russian");


   // ������������ ���� ������������ ������!

   //�������� ���������� ������������� �������   !A!

   double rows, cols, a;
   cout<<"������� ���������� ����� � �������� ������� \"A\": ";
   cin>>rows>>cols ;
   double** mas=new double* [rows];
   for (int i=0; i<rows; i++) {
       mas[i]=new double[cols];
   }

   //���������� ���������� ������������� ������� !A!

   cout<<"������� �������� ������� \"A\": ";
   for (int i=0; i<rows; i++) {
       for (int j=-0; j<cols; j++) {
           cin>>a;
           mas[i][j] = {a};
       }
   }

   //����� ���������� ������������� ������� !A!

   cout<<"���������� ������� \"A\": "<<endl;
   for (int i=0; i<rows; i++) {
       for (int j=-0; j<cols; j++) {
           cout<<mas[i][j]<<" ";
       }
       cout<<endl;
   }
   cout<<endl;
   //�������� ���������� ������������� ������� !B!

   double rowss, colss, aa;
   cout<<"������� ���������� ����� � �������� ������� \"B\": ";
   cin>>rowss>>colss ;
   double** mass=new double* [rowss];
   for (int i=0; i<rowss; i++) {
       mass[i]=new double[colss];
   }

   //���������� ���������� ������������� ������� !B!

   cout<<"������� ������� ������� \"B\": ";
   for (int i=0; i<rowss; i++) {
       for (int j=-0; j<colss; j++) {
           cin>>aa;
           mass[i][j] = {aa};
       }
   }

   //����� ���������� ������������� ������� !B!

   cout<<"���������� ������� \"B\": "<<endl;
   for (int i=0; i<rowss; i++) {
       for (int j=-0; j<colss; j++) {
           cout<<mass[i][j]<<" ";
       }
       cout<<endl;
   }
   cout<<endl;
   // �������� �������, ������ ������������ ������ � � �

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

   //  ����� �������-������������

   cout<<"������������ ������ \"A\" � \"B\": "<<endl;
   for (int i=0; i<rows; i++) {
       for (int j=0; j <colss; j++) {
           cout<<c[i][j]<<" ";
       }
       cout<<endl;
   }





   //�������� ������������ ������ � ��������� ������������ ������� !A!

   for (int i=0; i<rows; i++) {
       delete[]mas[i];
   }
   delete[]mas;

   //�������� ������������ ������ � ��������� ������������ ������� !B!

   for (int i=0; i<rowss; i++) {
       delete[]mass[i];
   }
   delete[]mass;

   //�������� ������������ ������ � ��������� ������������ ������� !C!

   for (int i=0; i<rowss; i++) {
       delete[]c[i];
   }
   delete[]c;
   }

    /*

    //���������� ������� � ������� ( UPD: ����� ������� )

    //�������� ���������� ������������� �������   !A!

    double rows, cols, a;
    cout << "������� ���������� ����� � �������� ������� \"A\": ";
    cin >> rows >> cols;
    double **mas = new double *[rows];
    for (int i = 0; i < rows; i++) {
        mas[i] = new double[cols];
    }

//���������� ���������� ������������� ������� !A!

    cout << "������� �������� ������� \"A\": ";
    for (int i = 0; i < rows; i++) {
        for (int j = -0; j < cols; j++) {
            cin >> a;
            mas[i][j] = {a};
        }
    }

//����� ���������� ������������� ������� !A!

    cout << "���������� ������� \"A\": " << endl;
    for (int i = 0; i < rows; i++) {
        for (int j = -0; j < cols; j++) {
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;

    int n,k;
    cout<<"������� �������� ����� \"n\" (�������): ";
    cin>>n;
    k=1;
    while (k<n) {
        // �������� �������, ������ ������������ ������ � � �

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

        //  ����� �������-������������

        cout<<"������� \"A\" � ������� "<<k+1<<" �����: "<<endl;
        for (int i=0; i<rows; i++) {
            for (int j=0; j <cols; j++) {
                cout<<c[i][j]<<" ";
            }
            cout<<endl;
        }

        //�������� ������������ ������ � ��������� ������������ ������� !C!

        for (int i=0; i<rows; i++) {
            delete[]c[i];
        }
        delete[]c;

        k=k+1;
    }

    //�������� ������������ ������ � ��������� ������������ ������� !A!

    for (int i=0; i<rows; i++) {
        delete[]mas[i];
    }
    delete[]mas;
*/