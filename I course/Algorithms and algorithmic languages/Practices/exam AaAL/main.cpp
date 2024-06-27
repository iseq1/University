#include <iostream>
#include <ctime> // � ��� ������� time
using namespace std; // ��������� ����� ���������� ������� ������������� ������!!!

// 1.��������� ������ � ���� ��������� �������
void massiv() {
    int size; cin>>size;
    double* mas=new double[size];
    for(int i=0; i<size; i++) {
        cin>>mas[i];
    }
    for (int i=0; i<size; i++) {
        cout<<mas[i]<<" ";
    }
    delete[]mas;
}

// 2+3.��������� ������ � ���� ��������� ������������� ������� + ����� ������������� �������
void matrica() {
    int cols,rows; cin>>cols>>rows;
    double**matr=new double*[rows];
    for(int i=0; i<rows; i++) {
        matr[i]=new double[cols];
    }
    for(int i=0; i<rows; i++) {
        for(int j=0; j<cols; j++) {
            cin>>matr[i][j];
        }
    }
    for (int i=0; i<rows; i++) {
        for (int j=0; j <cols; j++) {
            cout<<matr[i][j]<<" ";
        }
        cout<<endl;
    }
    for(int i=0;i<rows;i++){
        delete[]matr[i];
    }
    delete[]matr;
}

// 4. ��������� ����� ��������� ������ �����
void sum_of_divisors() {
    int num; cin>>num; int sum=1;
    cout<<"1";
    for(int i=2;i<=num;i++){
        if (num%i==0) {
            sum+=i; cout<<"+"<<i;
        }
    }
    cout<<"="<<sum;
}

// 5. ��������� ����������� ������ �������� ���� ����� �����
void NOD() {
    int num1,num2,k1,k2; cin>>num1>>num2;
    for (int i=num1; i>0; i--) {
        if (num1%i==0 && num2%i==0) {
            cout << "nod = " << i;
            break;
        }
    }
}

// 6. ��������� ��������� �� ������ ����� ���������
int fibonacci(int num) {
    if (num == 0)
        return 0;
    if (num == 1)
        return 1;
    return fibonacci(num - 1) + fibonacci(num - 2);
}

// 7. ���������� n!
int fact(int num) {
    if (num == 0) return 1;
    if (num == 1) return 1;
    if (num > 1) return num * fact(num - 1);
}

// 8. ���������� x^n
void degree() {
    int x,n,itog=1; cin>>x>>n;
    for(int i=0; i<n; i++) {
        itog*=x;
    }
    cout<<itog;
}

// 9. �������� ������ ����� �� ��������
void simple_integer() {
    int num,k=0; cin>>num;
    for (int i=1; i<=num; i++) {
        if (num%i==0){
            k++;
        }
    }
    if (k==2) {
        cout<<num<<" ������� �����!";
    }
    else cout<<num<<" �� ������� �����!";
}

// 10. �������� ����, ��� � ������ ������ ����� ���� �������� �����.
void digit(){
    int num,digit,k=0,number; cin>>num>>digit; number=num;
    while (num>0){
        if (num%10==digit) k++;
        num/=10;
    }
    if (k>0) cout<<"����� "<<digit<<" ����������� � ����� "<<number<<" "<<k<<" ���(�)";
    else cout<<"����� "<<digit<<" �� ����������� � ����� "<<number;
}

// 11. ��������� ����� ��������� �������� ������������������ (��� ���������� � �������).
void sum_range(){
    int sum=0,n,elem; cout<<"������� ���������� ���������, ���� �������� ������������������: "; cin>>n;
    for (int i=0; i<n;i++) {
        cin>>elem; sum+=elem;
    }
    cout<<sum;
}

// 12. ��������� ������������ ��������� �������� ������������������ (��� ���������� � �������).
void product_range() {
    int prod=1,n,elem; cout<<"������� ���������� ���������, ���� �������� ������������������: "; cin>>n;
    for (int i=0; i<n;i++) {
        cin>>elem; prod*=elem;
    }
    cout<<prod;
}

// 13. ��������� ������������� �� ��������� �������� ������������������ (��� ���������� � �������).
void max_range() {
    int k=0,n,elem; cout<<"������� ���������� ���������, ���� �������� ������������������: "; cin>>n;
    for(int i=0;i<n;i++){
        cin>>elem; if (elem>k) k=elem;
    }
    cout<<k;
}

// 14. ��������� ���������� ������������ ��������� � �������.
void max_elems_in_masiv(){
    int n; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    } int maxelem=0;
    for(int i=0;i<n;i++){
        if(mas[i]>maxelem) maxelem=mas[i];
    } int counter_maxelem=0;
    cout<<"� ������������������: ";
    for(int i=0;i<n;i++){
        cout<<mas[i]<<" ";
        if(mas[i]==maxelem) counter_maxelem++;
    }
    cout<<" - ������ "<<counter_maxelem<<" ���(�) ������������ �������("<<maxelem<<")";
    delete[]mas;
}

// 15. ��������� ���� ������������ ��������� �������
void two_max_elems_in_masiv() {
    int n; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    }
    int maxelem=0;
    for(int i=0;i<n;i++){
        if(mas[i]>maxelem) maxelem=mas[i];
    }
    int second_maxelem=0; cout<<"� ������������������: ";
    for(int i=0;i<n;i++){ cout<<mas[i]<<" ";
        if(mas[i]<maxelem && mas[i]>second_maxelem) second_maxelem=mas[i];
    }
    cout<<" - ������� ��� ������������ ��������: "<<second_maxelem<<" "<<maxelem;
    delete[]mas;
}

// 16. ��������� ������������� �������� ������� �� ���������, ��������������� ������� (������?)
void max_elem_condition() {
    int n; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    } int maxelem=0;
    for(int i=0;i<n;i++){
        if(mas[i]>maxelem) {
            maxelem = mas[i];
        }
    }
    delete[]mas;
}

// 17. �������� ����, ��� �������� ������� �������� ������������ ������������������.
void increasing_sequence(){
    int n,k=0; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    }
    for(int i=0; i<n;i++)
        if(mas[i]<mas[i+1]) k++;
    if(k==n-1)
        cout<<"ok"<<endl;
    else
        cout<<"no"<<endl;
    delete[]mas;
}

// 18. �������� ����, ��� �������� ������� �������� ������������ ������������������.
void symmetric_sequence(){
    int n,k=0; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    } int range=n/2, j=n-1;
    for (int i=0; i<range; i++){
        if (mas[i]==mas[j]) {
            k++;
        } j--;
    }
    if (k==range) {
        cout<<"ok";
    }
    else cout<<"no";
    delete[]mas;
}

// 19.���������� �������. (������������ ����?) (����� ����� ������������ ������������������)
void sortirovka_masiva() { int n; cin>>n;
    double*mas=new double[n];
    for (int i = 0; i < n; i++) {
        cin >> mas[i];
    }
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (mas[j] > mas[j + 1]) {
                temp = mas[j];
                mas[j] = mas[j + 1];
                mas[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < n; i++) {
        cout << mas[i] << " ";
    }
    delete[]mas;
}

// 20. �������� ��������� ������ ��������������� ��������� �������� � �������.
void binary_search() {int n; cin>>n;
    double*mas=new double[n];
    for (int i = 0; i < n; i++) {
        cin >> mas[i];
    }
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (mas[j] > mas[j + 1]) {
                temp = mas[j];
                mas[j] = mas[j + 1];
                mas[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < n; i++) {
        cout<<mas[i]<<" ";
    }
    cout<<endl;
    //����� ��������������� ������, ��� ��� �������� ����� � ������������ �������,
    //������ ���� ����������� � ���������� ��������� ������
    cout<<"������� �������, ������� ���������� �����: "; int key; cin>>key;
    bool flag = false;
    int left = 0, right = n-1, mid; // ����� �������, ������ �������, ��������
    while ((left <= right) && (flag != true)) {
        mid = (left + right) / 2; // ��������� ��������� ������ ������� [left,right]
        if (mas[mid] == key) flag = true; //��������� ���� �� ���������� ���������
        if (mas[mid] > key) right = mid - 1; // ���������, ����� ����� ����� ���������
        else left = mid + 1;
    }
    if (flag) cout << "������ �������� " << key << " � ������� �����: " << mid;
    else cout << "��������, �� ������ �������� � ������� ���";
    delete[]mas;
}

// 21. �������� ������� ���� ��������������� ��������
void merging_two_arrays() { cout<<"������� ���-�� ��������� ������� ������� � ��� ������: ";
    int n, m; cin>>n;
    double*a=new double[n];
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    cout<<"������� ���-�� ��������� ������� ������� � ��� ������: "; cin>>m;
    double*b=new double[m];
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < m - 1; i++) {
        for (int j = 0; j < m - i - 1; j++) {
            if (b[j] > b[j + 1]) {
                temp = b[j];
                b[j] = b[j + 1];
                b[j + 1] = temp;
            }
        }
    }
    cout<<"������ \"A\": ";
    for (int i = 0; i < n; i++) {
        cout<<a[i]<<" ";
    } cout<<endl;
    cout<<"������ \"B\": ";
    for (int i = 0; i < m; i++) {
        cout<<b[i]<<" ";
    } cout<<endl;

    double*mas=new double[n+m];
    for(int i=0; i<n; i++){
        mas[i] = a[i];
    } int k=0;
    for(int i=n; i<n+m; i++){
        mas[i] = b[k]; k++;
    }
    cout<<"������� ���� ��������: ";
    for (int i = 0; i < m+n; i++) {
        cout<<mas[i]<<" ";
    } cout<<endl;

    delete[]a; delete[]b; delete[]mas;
}

// 22. �������� ��������� ���� ��������, �������� � ������� ��������.
void equal_sets() { cout<<"������� ���-�� ��������� 1-�� ���������, � ����� ���� ���������: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"������� ���-�� ��������� 2-�� ���������, � ����� ���� ���������: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int k=0;
    if (n!=m){
        cout<<"��� �������� ��������� �������!";
    }
    else {
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if (a[i]==b[j]) {
                    k++;
                }
            }
        }
        if (k==n) {
            cout<<"��� �������� ��������� �����!";
        }
        else {cout<<"��� �������� ��������� �������!";}
    }
    delete[]a, delete[]b;
}

// 23. �������� ��������� ������ ��������� � ������. ��������� ������ � ������� ��������.
void occurrence_of_the_set() { cout<<"������� ���-�� ��������� 1-�� ���������, � ����� ���� ���������: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"������� ���-�� ��������� 2-�� ���������, � ����� ���� ���������: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    } int k=0;
    for(int i=0;i<m;i++){
        for(int j=0;j<n;j++){
            if (b[i]==a[j]){
                k++;
            }
        }
    }
    if (k==m) {cout<<"������ ��������� ��������� ������ � ������ ���������!";}
    if (k<m && k!=0) {cout<<"������ ��������� �������� ������ � ������ ���������!";} //����� �� ������������ ������ �������?
    if (k==0) {cout<<"������ ��������� �� ������ � ������ ���������!";}
    delete[]a, delete[]b;
}

// 24. ���������� ����������� ���� ��������. ��������� ������ � ������� ��������.
void combining_two_sets() {cout<<"������� ���-�� ��������� 1-�� ���������, � ����� ���� ���������: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"������� ���-�� ��������� 2-�� ���������, � ����� ���� ���������: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    } int k=0;
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            if (a[i]==b[j]){
                k++;
            }
        }
    }
    int size=n+m-k;
    int*c=new int[size]; // �������� ������� - ����������� ���� ��������
    for(int i=0;i<size;i++){
        c[i]={0};
    }
    if (n>m) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (i < n && a[i] != c[i] && a[i] != c[j]) {
                    c[i] = a[i];
                }
                if (i >= n && b[i - n] != c[i] && b[i - n] != c[j]) {
                    c[i] = b[i - n];
                }
            }
        }
    }
    if (n<m) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (i < m && b[i] != c[i] && b[i] != c[j]) {
                    c[i] = b[i];
                }
                if (i >= m && a[i - m] != c[i] && a[i - m] != c[j]) {
                    c[i] = a[i - m];
                }
            }
        }
    }
    cout<<endl<<"��������� ��������� �� ����������� ������ ���� ��������: ";
    for(int i=0;i<size;i++){
        cout<<c[i]<<" ";
    }
    delete[]a,delete[]b,delete[]c;
}

// 25. ���������� ����������� ���� ��������. ��������� ������ � ������� ��������.
void intersection_of_two_sets() {cout<<"������� ���-�� ��������� 1-�� ���������, � ����� ���� ���������: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"������� ���-�� ��������� 2-�� ���������, � ����� ���� ���������: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int size=0; //����� ������� �����������
    int len=m*n; //����� �������, ��� ����� ��������� ���� � ��������, ������� ���� ��� � 1 ��., ��� � �� 2!
    int*masinter=new int[len]; //������, ��� ����� ��������� ���� � ��������, ������� ���� ��� � 1 ��., ��� � �� 2!
    int elem=0;
    for(int i=0;i<n;i++) {
        for(int j=0;j<m;j++){
            if (a[i]==b[j]) {
                size++; // ���������� ���������, ������� ���������� ������ �����������
                masinter[elem] = { a[i] }; elem++;
            }
            else { masinter[elem] = {0}; elem++;}
        }
    }
    int*c=new int[size]; //������ �����������
    if (size==0) { cout<<endl<<"� ������ ���� �������� �� ���������� ��������� �� �����������!";}
    else {
        int k=0;
        for(int i=0;i<len;i++){
            if (masinter[i]!=0){
                c[k]=masinter[i];
                k++;
            }
        }
        cout<<endl<<"���������� ��������� ����������� ���� ������ ��������: ";
        for(int i=0;i<size;i++){
            cout<<c[i]<<" ";
        }
    }
    delete[]a,delete[]b,delete[]masinter,delete[]c;
}

// 26. ���������� �������� ���� ��������. ��������� ������ � ������� ��������.
void difference_of_two_sets() {cout<<"������� ���-�� ��������� 1-�� ���������, � ����� ���� ���������: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"������� ���-�� ��������� 2-�� ���������, � ����� ���� ���������: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int size=0; //����� ������� �����������
    int len=m*n; //����� �������, ��� ����� ��������� ���� � ��������, ������� ���� ��� � 1 ��., ��� � �� 2!
    int*masinter=new int[len]; //������, ��� ����� ��������� ���� � ��������, ������� ���� ��� � 1 ��., ��� � �� 2!
    int elem=0;
    for(int i=0;i<n;i++) {
        for(int j=0;j<m;j++){
            if (a[i]==b[j]) {
                size++; // ���������� ���������, ������� ���������� ������ �����������
                masinter[elem] = { a[i] }; elem++;
            }
            else { masinter[elem] = {0}; elem++;}
        }
    }
    for(int j=0;j<n;j++) {
        for (int z = 0; z < elem; z++) {
            if (a[j]==masinter[z]) {
                a[j]={0};
            }
        }
    }
    int*c=new int[size]; //������ ��������
    if (size==n) { cout<<endl<<"�������� ���� �������� �������� ������ ���������!";}
    else {
        cout<<endl<<"��������� �������� ���� ��������: ";
        for (int i=0;i<n;i++){
            if(a[i]!=0){
                cout<<a[i]<<" ";
            }
        }
    }
    delete[]a,delete[]b,delete[]masinter,delete[]c;
}

// 27. ��������� ���������� ���� � ���������� ������
void word_counter(){ int count=0;
    char*str=new char[1000];
    cin.getline(str,1000);
    for(int i=0; str[i]!='\0'; i++) {
        if (str[i]==' ' && str[i-1]!=' ' || str[i+1]=='\0' && str[i]!=' ') {count++;}
    }
    cout<<"� �������� ������ ����� "<<count<<" ����(�)!";
    delete[]str;
}

// 28. ��������� ����� ������������ ����� � ���������� ������.
void max_len_word(){ int len=0, maxlen=0, index=0;
    char*str=new char[1000];
    cin.getline(str,1000);
    for(int i=0; str[i]!='\0'; i++) {
        if (str[i]!=' ') { len++; if (len>maxlen) {maxlen=len; index=i;}}
        else {len=0;}
    }
    cout<<"� �������� ������ ����� � ������������ ������ ����� "<<maxlen<<" ��������!"<<endl;
    cout<<"� ���� ������ �������� �����: ";
    for(int i=index-maxlen+1;i<=maxlen+1;i++){
        cout<<str[i];
    }
    delete[]str;
}

// 29. �������� ����, ��� � ���������� ������ ���� �����-���������� (����� � ������������ �������).
int palindrom(int index_begin, int index_end, char*str){
    int i=index_begin,j=index_end,len=(index_end-index_begin)+1,k=0;
    for(int q=0;q<len;q++){
        if(str[i]==str[j]){
            k++;i++;j--;
        }
    }
    if (k==len) return 1;
    else return 0;
}
void palindromes() { char*str=new char[1000];
    cin.getline(str,1000);
    int index_begin=0, index_end=0, palindr=0;
    for(int i=0;str[i]!='\0';i++){
        if (str[i]!=' ' && str[i-1]==' ') {index_begin=i;}
        if (str[i]!=' ' && str[i+1]==' '  || str[i+1]=='\0') {index_end=i;}
        if ((index_begin==0 && index_end!=0) || (index_begin!=0 && index_end!=0)){
            if (palindrom(index_begin,index_end,str)==1) {
                palindr++;
            }
            index_begin=0; index_end=0;
        }
    }
    if (palindr!=0) {
        cout<<"� ������ ���� �����-����������, ������ �� "<<palindr<<" ����!";
    }
    else cout<<"� ������ ��� ����-�����������!";
    delete[]str;
}

// 30. ��������� ���������� ���� ���������� ������, � ������� ������ ����� ����� ���������.
void counter_mini_palindromes() { char*str=new char[1000];
    cin.getline(str,1000);
    int counter=0, index_begin=0, index_end=0;
    for(int i=0;str[i]!='\0';i++) {
        if (str[i]!=' ' && str[i-1]==' ') {index_begin=i;}
        if (str[i]!=' ' && str[i+1]==' '  || str[i+1]=='\0') {index_end=i;}
        if ((index_begin==0 && index_end!=0) || (index_begin!=0 && index_end!=0)){
            if (str[index_begin]==str[index_end]) {
                counter++; index_begin=0; index_end=0;
            }
        }
    }
    cout<<counter;
    delete[]str;
}

// 31. ��������� ����� ���������, ������� ��������� �� ������� ��������� ���������� �������.
void sum_main_diagonal() {cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum=0;
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            if (i==j) {sum+=mas[i][j];}
        }
    }
    cout<<"����� ��������� ������� ��������� ����������: "<<sum;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 32. ��������� ����� ���������, ������� ��������� �� �������� ��������� ���������� �������.
void sum_side_diagonal(){cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum=0;
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            if ((i+j)==n-1) {sum+=mas[i][j];}
        }
    }
    cout<<"����� ��������� �������� ��������� ����������: "<<sum;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 33. ��������� ����� ���������, ������� ��������� ���� (����) ������� ��������� ���������� �������.
void sum_above_and_below_the_main_diagonal(){cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum_above=0, sum_below=0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i!=j && i>j) {sum_below+=mas[i][j];}
            if (i!=j && i<j) {sum_above+=mas[i][j];}
        }
    }
    cout<<"����� ���������, ������������� ���� ������� ��������� �����: "<<sum_above<<endl;
    cout<<"����� ���������, ������������� ���� ������� ��������� �����: "<<sum_below;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 34. ��������� ����� ���������, ������� ��������� ���� (����) �������� ��������� ���������� �������.
void sum_above_and_below_the_side_diagonal() {cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum_above=0, sum_below=0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if ((i+j)<n-1) {sum_above+=mas[i][j];}
            if ((i+j)>n-1) {sum_below+=mas[i][j];}
        }
    }

    cout<<"����� ���������, ������������� ���� �������� ��������� �����: "<<sum_above<<endl;
    cout<<"����� ���������, ������������� ���� �������� ��������� �����: "<<sum_below;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 35. ��������� ������ (�������) ������������� �������, ������� ������������ ����� ���������.
void maximum_sum_of_a_row_or_column() {cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
        int sum_row=0, max_sum_row=0, sum_col=0, max_sum_col=0, index_row=0, index_col=0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                //����� ��� �����
                if (j<n-1) {sum_row+=mas[i][j];}
                if (j==n-1) {
                    sum_row+=mas[i][j];
                    if (sum_row>max_sum_row) {
                        max_sum_row=sum_row;
                        index_row=i;
                    }
                    sum_row=0;
                }
                //����� ��� ��������
                if (j<n-1) {sum_col+=mas[j][i];}
                if (j==n-1) {
                    sum_col+=mas[j][i];
                    if (sum_col>max_sum_col) {
                        max_sum_col=sum_col;
                        index_col=i;
                    }
                    sum_col=0;
                }
            }
        }
    cout<<"������ �"<<index_row+1<<" ����� ������������ �����, ������� �����: "<<max_sum_row<<", ����� ���� �����!"<<endl;
    cout<<"������� �"<<index_col+1<<" ����� ������������ �����, ������� �����: "<<max_sum_col<<", ����� ���� ��������!";
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 36. �����������, ������� �� � ������������� ������� ������ (�������), ��������� ������ �� ������� ���������.
void null_row_or_column() {cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum_row=0, sum_col=0, index_row=0, index_col=0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            //����� ��� �����
            if (j<n-1) {sum_row+=mas[i][j];}
            if (j==n-1) {
                sum_row+=mas[i][j];
                if (sum_row==0) {
                    index_row=i;
                }
                sum_row=0;
            }
            //����� ��� ��������
            if (j<n-1) {sum_col+=mas[j][i];}
            if (j==n-1) {
                sum_col+=mas[j][i];
                if (sum_col==0) {
                    index_col=i;
                }
                sum_col=0;
            }
        }
    }
    if (index_row!=0) { cout<<"� �������� ������� ���� ������, ��������� ������ �� �����, � ����� - "<<index_row+1<<endl; }
    else { cout<<"� �������� ������� ��� ������, ��������� ������ �� �����! "<<endl; }
    if (index_col!=0) { cout<<"� �������� ������� ���� �������, ��������� ������ �� �����, ��� ����� - "<<index_col+1<<endl; }
    else { cout<<"� �������� ������� ��� �������, ���������� ������ �� �����! "<<endl; }
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 37. �������� ������� ��� �������� ������ (�������) ������������� �������.
void swap_two_rows_or_columns() { cout<<"������� ���-�� ����� � �������� ������������� �������: "; int rows,cols; cin>>rows>>cols;
    int**mas=new int*[rows];
    for(int i=0;i<rows;i++){
        mas[i]=new int[cols];
    } cout<<"���������� �������: "<<endl;
    for(int i=0;i<rows;i++){
        for(int j=0;j<cols;j++){
            mas[i][j]=rand() % 10;
            cout<<mas[i][j]<<" ";
        }
        cout<<endl;
    }
    int choice; cout<<"��� �� ������ �������� �������: ��� ������ ��� ��� �������?"<<endl<<"��� ������ ����� ������� 1, ��� ������ �������� - 2"<<endl;
    cin>>choice;
    if (choice!=1 && choice!=2) {cout<<"��� ���� �� ����������� ����������, ��������� �������...";}
    if (choice==1) { int row1, row2;
        cout<<"������� ���������� ������ �����, ������� �� ������ �������� �������: "<<endl;cin>>row1>>row2;
        if ((row1<1 || row1>rows) || (row2<1 || row2>rows) || row1==row2) { cout<<"�� �������� ��� �����! ��������� �������...";}
        else {
            cout<<"���������� �������: "<<endl;
            for(int i=0;i<rows;i++){
                for(int j=0;j<cols;j++){
                    if (i==row1-1) {cout<<mas[row2-1][j]<<" ";}
                    if (i==row2-1) {cout<<mas[row1-1][j]<<" ";}
                    if (i!=row1-1 && i!=row2-1) {cout<<mas[i][j]<<" ";}
                }
                cout<<endl;
            }
        }
    }
    if (choice==2) {int col1, col2;
        cout<<"������� ���������� ������ �����, ������� �� ������ �������� �������: "<<endl;cin>>col1>>col2;
        if ((col1<1 || col1>cols) || (col2<1 || col2>cols) || col1==col2) { cout<<"�� �������� ��� �����! ��������� �������...";}
        else {
            cout<<"���������� �������: "<<endl;
            for(int i=0;i<rows;i++){
                for(int j=0;j<cols;j++){
                    if (j==col1-1) {cout<<mas[i][col2-1]<<" ";}
                    if (j==col2-1) {cout<<mas[i][col1-1]<<" ";}
                    if (j!=col1-1 && j!=col2-1) {cout<<mas[i][j]<<" ";}
                }
                cout<<endl;
            }
        }

    }
    for(int i=0;i<rows;i++){
        delete[]mas[rows];
    }
    delete[]mas;
}

// 38. ���������������� ���������� �������.
void matrix_transpose() {cout<<"������� ���-�� ����� ��.�������: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // ������ ������� ���������� ����� �� 0 �� 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    cout<<"���������� ����������������� �������: "<<endl;
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cout<<mas[j][i]<<" ";
        }
        cout<<endl;
    }
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 39. ��������� ����� ���� ������������� ������.
void sum_of_two_matrices() { cout<<"������� ���-�� ����� � �������� ������ ������������� �������: "; int rows1,cols1; cin>>rows1>>cols1;
    cout<<"������� ���-�� ����� � �������� ������ ������������� �������: "; int rows2,cols2; cin>>rows2>>cols2;
    if (rows1!=rows2 || cols1!=cols2) {
        cout<<"��� �������� ������ ���������� ������� ���������� �����������!"<<endl<<"��������� ������� �����...";
    }
    else {
        //������ �������
        int **mas1 = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            mas1[i] = new int[cols1];
        }
        cout << "���������� 1-�� �������: " << endl;
        for (int i = 0; i < rows1; i++) {
            for (int j = 0; j < cols1; j++) {
                mas1[i][j] = rand() % 10;
                cout << mas1[i][j] << " ";
            }
            cout << endl;
        }
        //������ �������
        int **mas2 = new int *[rows2];
        for (int i = 0; i < rows2; i++) {
            mas2[i] = new int[cols2];
        }
        cout << "���������� 2-�� �������: " << endl;
        for (int i = 0; i < rows2; i++) {
            for (int j = 0; j < cols2; j++) {
                mas2[i][j] = rand() % 10;
                cout << mas2[i][j] << " ";
            }
            cout << endl;
        }
        //������� �����
        int **massum = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            massum[i] = new int[cols1];
        }
        cout << "���������� ����� ������: " << endl;
        for (int i = 0; i < rows2; i++) {
            for (int j = 0; j < cols2; j++) {
                massum[i][j] = mas1[i][j] + mas2[i][j];
                cout << massum[i][j] << " ";
            }
            cout << endl;
        }

        for(int i=0; i<rows1; i++){
            delete[]mas1[rows1];
        }
        delete[]mas1;
        for(int i=0; i<rows2; i++){
            delete[]mas2[rows2];
        }
        delete[]mas2;
        for(int i=0; i<rows1; i++){
            delete[]massum[rows1];
        }
        delete[]massum;
    }
}

// 40. ��������� ������������ ���� ������������� ������
void product_of_two_matrices() {
    cout<<"������� ���-�� ����� � �������� ������ ������������� �������: "<<endl; int rows1,cols1; cin>>rows1>>cols1;
    cout<<"������� ���-�� ����� � �������� ������ ������������� �������: "<<endl; int rows2,cols2; cin>>rows2>>cols2;
    if (cols1!=rows2) {
        cout<<"�������� ��������� ���� ������ ��������� ������ � ��� ������, ���� ����� �������� � ������ ����������� ����� ����� ����� �� ������!"<<endl<<"��������� ������� �����...";
    }
    else {
        //������ �������
        int **mas1 = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            mas1[i] = new int[cols1];
        }
        cout << "���������� 1-�� �������: " << endl;
        for (int i = 0; i < rows1; i++) {
            for (int j = 0; j < cols1; j++) {
                mas1[i][j] = rand() % 10;
                cout << mas1[i][j] << " ";
            }
            cout << endl;
        }
        //������ �������
        int **mas2 = new int *[rows2];
        for (int i = 0; i < rows2; i++) {
            mas2[i] = new int[cols2];
        }
        cout << "���������� 2-�� �������: " << endl;
        for (int i = 0; i < rows2; i++) {
            for (int j = 0; j < cols2; j++) {
                mas2[i][j] = rand() % 10;
                cout << mas2[i][j] << " ";
            }
            cout << endl;
        }
        //������� ������������
        int **masprod = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            masprod[i] = new int[cols2];
        }
        cout << "���������� ������������ ������: " << endl;
        for (int i = 0; i < rows1; i++) {
            for (int j = 0; j < cols2; j++) {
                masprod[i][j]=0;
                for(int k=0;k<cols1;k++) {
                    masprod[i][j] += mas1[i][k] * mas2[k][j];
                }
                cout << masprod[i][j] << " ";
            }
            cout << endl;
        }

        for(int i=0; i<rows1; i++){
            delete[]mas1[rows1];
        }
        delete[]mas1;
        for(int i=0; i<rows2; i++){
            delete[]mas2[rows2];
        }
        delete[]mas2;
        for(int i=0; i<rows1; i++){
            delete[]masprod[rows1];
        }
        delete[]masprod;
    }
}



int main(){
    setlocale(LC_ALL, "ru");
    srand(time(NULL)); // �������������� ��������� ��������� �����.
    int N,M; cin>>N>>M;
    int**mas=new int*[N];
    for(int i=0;i<N;i++){
        mas[i]=new int[M];
    }
    for(int i=0; i<N;i++){
        for(int j=0; j<M; j++){
            cin>>mas[i][j];
        }
    }
    int k,m; cin>>k>>m; int elem=0;
    for(int i=0; i<N;i++){
        for(int j=0; j<M; j++){
            elem=mas[i][k];
            mas[i][k]=mas[m][j];
            mas[m][j]=elem;
        }
    }
    for(int i=0; i<N;i++){
        for(int j=0; j<M; j++) {
            cout << mas[i][j] <<' ';
        }
        cout<<endl;
    }


  //1.  massiv();
  //2+3.  matrica();
  //4.  sum_of_divisors();
  //5.  NOD();
  //6.  int num; cin>>num; cout<<fibonacci(num);
  //7.  int num; cin>>num; cout<<fact(num);
  //8.  degree();
  //9.  simple_integer();
  //10.  digit();
  //11.  sum_range();
  //12.  product_range();
  //13.  max_range();
  //14.  max_elems_in_masiv();
  //15.  two_max_elems_in_masiv();
  //16.  max_elem_condition();
  //17.  increasing_sequence();
  //18.  symmetric_sequence();
  //19.  sortirovka_masiva();
  //20.  binary_search();
  //21.  merging_two_arrays();
  //22.  equal_sets();
  //23.  occurrence_of_the_set();
  //24.  combining_two_sets();
  //25.  intersection_of_two_sets();
  //26.  difference_of_two_sets();
  //27.  word_counter();
  //28.  max_len_word();
  //29.  palindromes();
  //30. counter_mini_palindromes();
  //31. sum_main_diagonal();
  //32. sum_side_diagonal();
  //33. sum_above_and_below_the_main_diagonal();
  //34. sum_above_and_below_the_side_diagonal();
  //35.  maximum_sum_of_a_row_or_column();
  //36.  null_row_or_column();
  //37.  swap_two_rows_or_columns();
  //38.  matrix_transpose();
  //39.  sum_of_two_matrices();
  //40.  product_of_two_matrices();
}