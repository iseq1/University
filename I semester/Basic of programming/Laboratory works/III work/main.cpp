/*
3. � ������������������ �� n ����� ����� ����� ����������
������� � ���������� �������� ���������� ������� ������������
��� ��������� ���������. � ������ ������ ������� ���������� �����
� ������������������, � �� ������ � ���� �����.
�������� ������:

���������:
6
*/

#include <iostream>
using namespace std;
int main() {9
    2 5 1 2 3 7 3 2 2
    setlocale(LC_ALL, "Rus");
    int n;
    cout<<"������� ����� ��������� � �������, � ����� � ��� ����� �����: "<<endl;
    cin>>n;
    int* mas=new int [n];
    for (int i=0; i<n; i++) {
        cin>>mas[i];
    }

    // ���������� �������� � ������� ������������ ���������
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

    // ���������� �������� � ������� ��������� ���������
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

    //���������� ��� ��������� � ������� �������
    int max_drop = max(max_drop_up, max_drop_down);
    cout<<endl<<"���������� ������� � ������ �������� �����: "<<max_drop;
    delete[]mas;
}