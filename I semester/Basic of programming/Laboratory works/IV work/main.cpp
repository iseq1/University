/*
4. ������������� ��� ������ ��� ��������� n � ������������
������������������ ���������� ������������ ������ �� ������������
�� �������, ��� n. ����� n ��������.
�������� ������:
5
���������:
1/5 1/4 1/3 2/5 1/2 3/5 2/3 3/4 4/5
*/

#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "Russian");
    cout<<"������� ����� n: ";
    int n,a=0,b=1,c=1,d,p,q;
    cin>>n;
    d=n;
    //������������������ ����� n-�� ������� ������������ ����� ������������ ��� ���� �������������
    // ������������ ���������� ������, ����������� ������� ������ ��� ����� n;
    //������������������ ����� F(n) ���������� � 0/1 (a/b), 1/n (c/n) ... � ������������� (n-1)/n, 1/1;
    cout<<a<<"/"<<b<<" "<<c<<"/"<<n<<" ";
    while (c<=n && d!=1) {
        p = ((n + b) / d) * c - a;
        q = ((n + b) / d) * d - b;
        cout << p << "/" << q << " ";
        a=c, b=d, c=p, d=q;
    }
}