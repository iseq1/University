/*
2. ��������������� ��� ����� �� 1 �� n.
�������� ���������, ������� �������� � ���������� ����� ����������
���� ��������� �������� ���� �� ���� ���� ������, ������ ������.
*/

#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL,"Russian");
    int n, sum=0;
    cout<<"������� ����� \"n\": ";
    cin>>n;
    cout<<"���������� ��� ������� ������ �����: "<<endl;
    for (int i=1; i <=n; i++) {
        int x=i;
        while (x>0) {
            if (x%10==1 || x%10==9 || x%100==25 || x%100==49 || x%100==81) {
                sum++;
                cout<<i<<endl;
                break;
            }
            x/=10;
        }
    }
    cout<<"����� ����� ����� �������: "<<sum;
    return 0;

}

// ������� 02.11.2021 15:55