#include <iostream>
using namespace std;
int main() {
    setlocale(LC_ALL, "rus");


//����������� ������� ���������� �������� � ������.
    int n=0, numbers=0, space=0;
    char str[]="What a wonderful world 1234567890";
    cout<<"\""<<str<<"\""<<" ����� "<<sizeof(str)<<" �������!"<<endl;
    for (int i=0; i<sizeof(str); i++) {
        n++;
    }
    for (int i = 0; i<sizeof(str); i++){
        if ( (int)str[i] >= 48  && (int)str[i] <= 57)
            numbers++;
    }
    for (int i=0; i<sizeof(str); i++) {
        if( (int)str[i] == 32 ) {
            space++;
        }
    }
    cout<<"� ������ \""<<str<<"\" "<<n-numbers-space<<" ����, "<<numbers<<" ���� "<<space<<" �������!"<<endl;


//����������� ������� ���������� ���� � ������.
    cout<<endl;
    char text[] = "Hello world";
    char dest[50];
    strcpy_s(dest, text);
    cout << dest << endl;


// ���������� ��������� ���� �����.
    cout<<endl;
    int k=0;
    char str1[]="What a wonderful world";
    char str2[]="What a beautiful world";
    cout<<"������� "<<str1<<" � "<<str2<<endl;
    if (sizeof(str1) == sizeof(str2)) {
        cout<<"��� ������ ������ "<<sizeof(str1)<<" ��������"<<endl;
        for (int i=0; i<sizeof(str1); i++) {
            if (str1[i]==str2[i]) {
                k++;
            }
        }
        cout<<"������ \""<<str1<<"\" � \""<<str2<<"\" ����� "<<k<<" ���������� ��������";
    }
}
