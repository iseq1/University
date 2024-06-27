/*
5. ������������� ��� ������� �� 0 � 1 ����� n, � �������
���������� 0 ������ ��� ���������� 1. ����� n ��������.
�������� ������:
3
���������:
000
001
010
100
*/

#include <iostream>
using namespace std;

void sdvig(int max, int mask, int n) {
    for(int i = 0; i < max; i++){
        char *num = new char[n+1]; num[n] = '\0';
        int counter_ones = 0;//���������� ������
        for(int j = 0; j < n; j++){
            int calls = ((i & (mask >> j)) >> n-1-j);
            num[j] = '0' + calls;
            counter_ones += calls;
        }
        if(n - counter_ones > counter_ones) {
            cout << num << endl;
        }
    }
}

int main() {
    int n; cin >> n;
    int max = pow(2, n);
    int mask = pow(2, n-1);
    sdvig(max,mask,n);
}