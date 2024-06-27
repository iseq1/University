#include <iostream>
#include <ctime> // в ней функция time
using namespace std; // АБСОЛЮТНО ВЕЗДЕ НЕОБХОДИМО УДАЛИТЬ ДИНМАМИЧЕСКУЮ ПАМЯТЬ!!!

// 1.Выделение памяти и ввод элементов массива
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

// 2+3.Выделение памяти и ввод элементов прямоугольной матрицы + Вывод прямоугольной матрицы
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

// 4. Получение суммы делителей целого числа
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

// 5. Получение наибольшего общего делителя двух целых чисел
void NOD() {
    int num1,num2,k1,k2; cin>>num1>>num2;
    for (int i=num1; i>0; i--) {
        if (num1%i==0 && num2%i==0) {
            cout << "nod = " << i;
            break;
        }
    }
}

// 6. Получение заданного по номеру числа Фибоначчи
int fibonacci(int num) {
    if (num == 0)
        return 0;
    if (num == 1)
        return 1;
    return fibonacci(num - 1) + fibonacci(num - 2);
}

// 7. Вычисление n!
int fact(int num) {
    if (num == 0) return 1;
    if (num == 1) return 1;
    if (num > 1) return num * fact(num - 1);
}

// 8. Вычисление x^n
void degree() {
    int x,n,itog=1; cin>>x>>n;
    for(int i=0; i<n; i++) {
        itog*=x;
    }
    cout<<itog;
}

// 9. Проверка целого числа на простоту
void simple_integer() {
    int num,k=0; cin>>num;
    for (int i=1; i<=num; i++) {
        if (num%i==0){
            k++;
        }
    }
    if (k==2) {
        cout<<num<<" простое число!";
    }
    else cout<<num<<" не простое число!";
}

// 10. Проверка того, что в записи целого числа есть заданная цифра.
void digit(){
    int num,digit,k=0,number; cin>>num>>digit; number=num;
    while (num>0){
        if (num%10==digit) k++;
        num/=10;
    }
    if (k>0) cout<<"Цифра "<<digit<<" встречается в числе "<<number<<" "<<k<<" раз(а)";
    else cout<<"Цифра "<<digit<<" не встречается в числе "<<number;
}

// 11. Получение суммы элементов заданной последовательности (без сохранения в массиве).
void sum_range(){
    int sum=0,n,elem; cout<<"Ввелите количество элементов, сами элементы последовательности: "; cin>>n;
    for (int i=0; i<n;i++) {
        cin>>elem; sum+=elem;
    }
    cout<<sum;
}

// 12. Получение произведения элементов заданной последовательности (без сохранения в массиве).
void product_range() {
    int prod=1,n,elem; cout<<"Ввелите количество элементов, сами элементы последовательности: "; cin>>n;
    for (int i=0; i<n;i++) {
        cin>>elem; prod*=elem;
    }
    cout<<prod;
}

// 13. Получение максимального из элементов заданной последовательности (без сохранения в массиве).
void max_range() {
    int k=0,n,elem; cout<<"Ввелите количество элементов, сами элементы последовательности: "; cin>>n;
    for(int i=0;i<n;i++){
        cin>>elem; if (elem>k) k=elem;
    }
    cout<<k;
}

// 14. Получение количества максимальных элементов в массиве.
void max_elems_in_masiv(){
    int n; cin>>n;
    double*mas=new double[n];
    for(int i=0;i<n;i++){
        cin>>mas[i];
    } int maxelem=0;
    for(int i=0;i<n;i++){
        if(mas[i]>maxelem) maxelem=mas[i];
    } int counter_maxelem=0;
    cout<<"В последовательности: ";
    for(int i=0;i<n;i++){
        cout<<mas[i]<<" ";
        if(mas[i]==maxelem) counter_maxelem++;
    }
    cout<<" - найден "<<counter_maxelem<<" раз(а) максимальный элемент("<<maxelem<<")";
    delete[]mas;
}

// 15. Получение двух максимальных элементов массива
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
    int second_maxelem=0; cout<<"В последовательности: ";
    for(int i=0;i<n;i++){ cout<<mas[i]<<" ";
        if(mas[i]<maxelem && mas[i]>second_maxelem) second_maxelem=mas[i];
    }
    cout<<" - найдены два максимальных элемента: "<<second_maxelem<<" "<<maxelem;
    delete[]mas;
}

// 16. Получение максимального элемента массива из элементов, удовлетворяющих условию (какому?)
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

// 17. Проверка того, что элементы массива образуют возрастающую последовательность.
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

// 18. Проверка того, что элементы массива образуют симметричную последовательность.
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

// 19.Сортировка массива. (относительно чего?) (пусть будет возрастающая последовательность)
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

// 20. Алгоритм бинарного поиска местонахождения заданного элемента в массиве.
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
    //имеем отсортированный массив, где все эдементы стоят в возрастающем порядке,
    //теперь можн оприступить к реализации бинарного поиска
    cout<<"Введите элемент, который необходимо найти: "; int key; cin>>key;
    bool flag = false;
    int left = 0, right = n-1, mid; // левая граница, правая граница, середина
    while ((left <= right) && (flag != true)) {
        mid = (left + right) / 2; // считываем срединный индекс отрезка [left,right]
        if (mas[mid] == key) flag = true; //проверяем ключ со серединным элементом
        if (mas[mid] > key) right = mid - 1; // проверяем, какую часть нужно отбросить
        else left = mid + 1;
    }
    if (flag) cout << "Индекс элемента " << key << " в массиве равен: " << mid;
    else cout << "Извините, но такого элемента в массиве нет";
    delete[]mas;
}

// 21. Алгоритм слияния двух отсортированных массивов
void merging_two_arrays() { cout<<"Введите кол-во элементов первого массива и сам массив: ";
    int n, m; cin>>n;
    double*a=new double[n];
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    cout<<"Введите кол-во элементов второго массива и сам массив: "; cin>>m;
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
    cout<<"Массив \"A\": ";
    for (int i = 0; i < n; i++) {
        cout<<a[i]<<" ";
    } cout<<endl;
    cout<<"Массив \"B\": ";
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
    cout<<"Слияние двух массивов: ";
    for (int i = 0; i < m+n; i++) {
        cout<<mas[i]<<" ";
    } cout<<endl;

    delete[]a; delete[]b; delete[]mas;
}

// 22. Проверка равенства двух множеств, заданных с помощью массивов.
void equal_sets() { cout<<"Введите кол-во элементов 1-го множества, а затем само множество: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"Введите кол-во элементов 2-го множества, а затем само множество: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int k=0;
    if (n!=m){
        cout<<"Два заданных множества неравны!";
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
            cout<<"Два заданных множества равны!";
        }
        else {cout<<"Два заданных множества неравны!";}
    }
    delete[]a, delete[]b;
}

// 23. Проверка вхождения одного множества в другое. Множества заданы с помощью массивов.
void occurrence_of_the_set() { cout<<"Введите кол-во элементов 1-го множества, а затем само множество: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"Введите кол-во элементов 2-го множества, а затем само множество: ";
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
    if (k==m) {cout<<"Второе множество полностью входит в первое множество!";}
    if (k<m && k!=0) {cout<<"Второе множество частично входит в первое множество!";} //может ли существовать данный вариант?
    if (k==0) {cout<<"Второе множество не входит в первое множество!";}
    delete[]a, delete[]b;
}

// 24. Нахождение объединения двух множеств. Множества заданы с помощью массивов.
void combining_two_sets() {cout<<"Введите кол-во элементов 1-го множества, а затем само множество: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"Введите кол-во элементов 2-го множества, а затем само множество: ";
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
    int*c=new int[size]; // создание массива - объединения двух множеств
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
    cout<<endl<<"Полученое множество из объединения первых двух множеств: ";
    for(int i=0;i<size;i++){
        cout<<c[i]<<" ";
    }
    delete[]a,delete[]b,delete[]c;
}

// 25. Нахождение пересечения двух множеств. Множества заданы с помощью массивов.
void intersection_of_two_sets() {cout<<"Введите кол-во элементов 1-го множества, а затем само множество: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"Введите кол-во элементов 2-го множества, а затем само множество: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int size=0; //длина массива пересечения
    int len=m*n; //длина массива, где будут храниться нулю и элементы, которые есть как в 1 мн., так и во 2!
    int*masinter=new int[len]; //массив, где будут храниться нулю и элементы, которые есть как в 1 мн., так и во 2!
    int elem=0;
    for(int i=0;i<n;i++) {
        for(int j=0;j<m;j++){
            if (a[i]==b[j]) {
                size++; // количество элементов, которые составляют массив пересечения
                masinter[elem] = { a[i] }; elem++;
            }
            else { masinter[elem] = {0}; elem++;}
        }
    }
    int*c=new int[size]; //массив пересечения
    if (size==0) { cout<<endl<<"У данных двух множеств не образуется множество их пересечения!";}
    else {
        int k=0;
        for(int i=0;i<len;i++){
            if (masinter[i]!=0){
                c[k]=masinter[i];
                k++;
            }
        }
        cout<<endl<<"Полученное множество пересечения двух первых множеств: ";
        for(int i=0;i<size;i++){
            cout<<c[i]<<" ";
        }
    }
    delete[]a,delete[]b,delete[]masinter,delete[]c;
}

// 26. Нахождение разности двух множеств. Множества заданы с помощью массивов.
void difference_of_two_sets() {cout<<"Введите кол-во элементов 1-го множества, а затем само множество: ";
    int n; cin>>n; int*a=new int[n];
    for(int i=0;i<n;i++){
        cin>>a[i];
    }cout<<"Введите кол-во элементов 2-го множества, а затем само множество: ";
    int m; cin>>m;
    int*b=new int[m];
    for(int i=0;i<m;i++){
        cin>>b[i];
    }
    int size=0; //длина массива пересечения
    int len=m*n; //длина массива, где будут храниться нулю и элементы, которые есть как в 1 мн., так и во 2!
    int*masinter=new int[len]; //массив, где будут храниться нулю и элементы, которые есть как в 1 мн., так и во 2!
    int elem=0;
    for(int i=0;i<n;i++) {
        for(int j=0;j<m;j++){
            if (a[i]==b[j]) {
                size++; // количество элементов, которые составляют массив пересечения
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
    int*c=new int[size]; //массив разности
    if (size==n) { cout<<endl<<"Разность двух множеств образует пустое множество!";}
    else {
        cout<<endl<<"Множество разности двух множеств: ";
        for (int i=0;i<n;i++){
            if(a[i]!=0){
                cout<<a[i]<<" ";
            }
        }
    }
    delete[]a,delete[]b,delete[]masinter,delete[]c;
}

// 27. Получение количества слов в символьной строке
void word_counter(){ int count=0;
    char*str=new char[1000];
    cin.getline(str,1000);
    for(int i=0; str[i]!='\0'; i++) {
        if (str[i]==' ' && str[i-1]!=' ' || str[i+1]=='\0' && str[i]!=' ') {count++;}
    }
    cout<<"В заданной строке ровно "<<count<<" слов(а)!";
    delete[]str;
}

// 28. Получение слова максимальной длины в символьной строке.
void max_len_word(){ int len=0, maxlen=0, index=0;
    char*str=new char[1000];
    cin.getline(str,1000);
    for(int i=0; str[i]!='\0'; i++) {
        if (str[i]!=' ') { len++; if (len>maxlen) {maxlen=len; index=i;}}
        else {len=0;}
    }
    cout<<"В заданной строке слово с максимальной длиной имеет "<<maxlen<<" символов!"<<endl;
    cout<<"И этим словом является слово: ";
    for(int i=index-maxlen+1;i<=maxlen+1;i++){
        cout<<str[i];
    }
    delete[]str;
}

// 29. Проверка того, что в символьной строке есть слова-палиндромы (слова с симметричной записью).
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
        cout<<"В строке есть слова-палиндромы, причём их "<<palindr<<" штук!";
    }
    else cout<<"В строке нет слов-палиндромов!";
    delete[]str;
}

// 30. Получение количества слов символьной строки, в которых первая буква равна последней.
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

// 31. Получение суммы элементов, которые находятся на главной диагонали квадратной матрицы.
void sum_main_diagonal() {cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
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
    cout<<"Сумма элементов главной диоганали составляет: "<<sum;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 32. Получение суммы элементов, которые находятся на побочной диагонали квадратной матрицы.
void sum_side_diagonal(){cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
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
    cout<<"Сумма элементов побочной диоганали составляет: "<<sum;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 33. Получение суммы элементов, которые находятся выше (ниже) главной диагонали квадратной матрицы.
void sum_above_and_below_the_main_diagonal(){cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
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
    cout<<"Сумма элементов, расположенных выше главной диагонали равна: "<<sum_above<<endl;
    cout<<"Сумма элементов, расположенных ниже главной диагонали равна: "<<sum_below;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 34. Получение суммы элементов, которые находятся выше (ниже) побочной диагонали квадратной матрицы.
void sum_above_and_below_the_side_diagonal() {cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
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

    cout<<"Сумма элементов, расположенных выше побочной диагонали равна: "<<sum_above<<endl;
    cout<<"Сумма элементов, расположенных ниже побочной диагонали равна: "<<sum_below;
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 35. Получение строки (столбца) прямоугольной матрицы, имеющей максимальную сумму элементов.
void maximum_sum_of_a_row_or_column() {cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
        int sum_row=0, max_sum_row=0, sum_col=0, max_sum_col=0, index_row=0, index_col=0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                //сумма для строк
                if (j<n-1) {sum_row+=mas[i][j];}
                if (j==n-1) {
                    sum_row+=mas[i][j];
                    if (sum_row>max_sum_row) {
                        max_sum_row=sum_row;
                        index_row=i;
                    }
                    sum_row=0;
                }
                //сумма для столбцов
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
    cout<<"Строка №"<<index_row+1<<" имеет максимальную сумму, которая равна: "<<max_sum_row<<", среди всех строк!"<<endl;
    cout<<"Столбец №"<<index_col+1<<" имеет максимальную сумму, которая равна: "<<max_sum_col<<", среди всех столбцов!";
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 36. Определение, имеется ли в прямоугольной матрице строка (столбец), состоящая только из нулевых элементов.
void null_row_or_column() {cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    int sum_row=0, sum_col=0, index_row=0, index_col=0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            //сумма для строк
            if (j<n-1) {sum_row+=mas[i][j];}
            if (j==n-1) {
                sum_row+=mas[i][j];
                if (sum_row==0) {
                    index_row=i;
                }
                sum_row=0;
            }
            //сумма для столбцов
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
    if (index_row!=0) { cout<<"В заданной матрице есть строка, состоящая только из нулей, её номер - "<<index_row+1<<endl; }
    else { cout<<"В заданной матрице нет строки, состоящей только из нулей! "<<endl; }
    if (index_col!=0) { cout<<"В заданной матрице есть столбец, состоящий только из нулей, его номер - "<<index_col+1<<endl; }
    else { cout<<"В заданной матрице нет столбца, состоящего только из нулей! "<<endl; }
    for(int i=0;i<n;i++){
        delete[]mas[i];
    }
    delete[]mas;
}

// 37. Поменять местами две заданные строки (столбца) прямоугольной матрицы.
void swap_two_rows_or_columns() { cout<<"Введите кол-во строк и столбцов прямоугольной матрицы: "; int rows,cols; cin>>rows>>cols;
    int**mas=new int*[rows];
    for(int i=0;i<rows;i++){
        mas[i]=new int[cols];
    } cout<<"Полученная матрица: "<<endl;
    for(int i=0;i<rows;i++){
        for(int j=0;j<cols;j++){
            mas[i][j]=rand() % 10;
            cout<<mas[i][j]<<" ";
        }
        cout<<endl;
    }
    int choice; cout<<"Что вы хотите поменять месатми: две строки или два столбца?"<<endl<<"Для выбора строк введите 1, для выбора столбцов - 2"<<endl;
    cin>>choice;
    if (choice!=1 && choice!=2) {cout<<"Ваш ввод не предсмотрен программой, повторите попытку...";}
    if (choice==1) { int row1, row2;
        cout<<"Введите порядковые номера строк, которые вы хотите поменять местами: "<<endl;cin>>row1>>row2;
        if ((row1<1 || row1>rows) || (row2<1 || row2>rows) || row1==row2) { cout<<"Вы ошиблись при вводе! Повторите попытку...";}
        else {
            cout<<"Полученная матрица: "<<endl;
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
        cout<<"Введите порядковые номера строк, которые вы хотите поменять местами: "<<endl;cin>>col1>>col2;
        if ((col1<1 || col1>cols) || (col2<1 || col2>cols) || col1==col2) { cout<<"Вы ошиблись при вводе! Повторите попытку...";}
        else {
            cout<<"Полученная матрица: "<<endl;
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

// 38. Транспонирование квадратной матрицы.
void matrix_transpose() {cout<<"Введите кол-во строк кв.матрицы: "<<endl; int n; cin>>n;
    int**mas=new int*[n];
    for(int i=0;i<n;i++){
        mas[i]=new int[n];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mas[i][j] = rand() % 10; // Каждый элемент случайному числу от 0 до 9
            cout << mas[i][j] << " ";
        }
        cout << endl;
    }
    cout<<"Полученная транспонированная матрица: "<<endl;
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

// 39. Получение суммы двух прямоугольных матриц.
void sum_of_two_matrices() { cout<<"Введите кол-во строк и столбцов первой прямоугольной матрицы: "; int rows1,cols1; cin>>rows1>>cols1;
    cout<<"Введите кол-во строк и столбцов второй прямоугольной матрицы: "; int rows2,cols2; cin>>rows2>>cols2;
    if (rows1!=rows2 || cols1!=cols2) {
        cout<<"Для сложения матриц необходимо условие одинаковой размерности!"<<endl<<"Повторите попытку ввода...";
    }
    else {
        //первая матрица
        int **mas1 = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            mas1[i] = new int[cols1];
        }
        cout << "Полученная 1-ая матрица: " << endl;
        for (int i = 0; i < rows1; i++) {
            for (int j = 0; j < cols1; j++) {
                mas1[i][j] = rand() % 10;
                cout << mas1[i][j] << " ";
            }
            cout << endl;
        }
        //вторая матрица
        int **mas2 = new int *[rows2];
        for (int i = 0; i < rows2; i++) {
            mas2[i] = new int[cols2];
        }
        cout << "Полученная 2-ая матрица: " << endl;
        for (int i = 0; i < rows2; i++) {
            for (int j = 0; j < cols2; j++) {
                mas2[i][j] = rand() % 10;
                cout << mas2[i][j] << " ";
            }
            cout << endl;
        }
        //матрица суммы
        int **massum = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            massum[i] = new int[cols1];
        }
        cout << "Полученная сумма матриц: " << endl;
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

// 40. Получение произведения двух прямоугольных матриц
void product_of_two_matrices() {
    cout<<"Введите кол-во строк и столбцов первой прямоугольной матрицы: "<<endl; int rows1,cols1; cin>>rows1>>cols1;
    cout<<"Введите кол-во строк и столбцов второй прямоугольной матрицы: "<<endl; int rows2,cols2; cin>>rows2>>cols2;
    if (cols1!=rows2) {
        cout<<"Операция умножения двух матриц выполнима только в том случае, если число столбцов в первом сомножителе равно числу строк во втором!"<<endl<<"Повторите попытку ввода...";
    }
    else {
        //первая матрица
        int **mas1 = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            mas1[i] = new int[cols1];
        }
        cout << "Полученная 1-ая матрица: " << endl;
        for (int i = 0; i < rows1; i++) {
            for (int j = 0; j < cols1; j++) {
                mas1[i][j] = rand() % 10;
                cout << mas1[i][j] << " ";
            }
            cout << endl;
        }
        //вторая матрица
        int **mas2 = new int *[rows2];
        for (int i = 0; i < rows2; i++) {
            mas2[i] = new int[cols2];
        }
        cout << "Полученная 2-ая матрица: " << endl;
        for (int i = 0; i < rows2; i++) {
            for (int j = 0; j < cols2; j++) {
                mas2[i][j] = rand() % 10;
                cout << mas2[i][j] << " ";
            }
            cout << endl;
        }
        //матрица перемножения
        int **masprod = new int *[rows1];
        for (int i = 0; i < rows1; i++) {
            masprod[i] = new int[cols2];
        }
        cout << "Полученное произведение матриц: " << endl;
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
    srand(time(NULL)); // Инициализируем генератор случайных чисел.
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