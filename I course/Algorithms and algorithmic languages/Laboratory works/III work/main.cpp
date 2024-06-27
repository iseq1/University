/*
3. Найти номер заданной перестановки в лексикографическом порядке.
 В исходных данных в первой строке задаётся число n, а во второй строке сама перестановка.
*/
#include <iostream>
using namespace std;

int fact(int n) {
    if (n<2) {
        return 1;
    }
    return n * fact(n-1);
}

int main() {
    int n, number = 1;
    cin >> n;
    int *mas = new int[n];
    for (int i = 0; i < n; i++) {cin >> mas[i];}

    for (int i = 0; i < n; i++) {
        int t;
        //количество комбинаций расстановки цифр после i-ого элемента
        t = fact(n - i - 1);
        // счётчик, определяющий количество элементов меньших p[i] в  интервале от p[0] до p[i-1]
        int c = 0;
        for (int j = 0; j < i; j++) {
            if (mas[j] < mas[i]) {c++;}
        }
        t *= mas[i] - 1 - c;
        number += t;
    }
    cout << number;
    delete[]mas;
}


// ПРИНЯЛИ 12.11.2021 16:55
























 /*

    int place=1;
    for (int i=0; i<n; i++) {
        place+= ((p[i]-1) * fact(n-1));
        cout<<place;
        for (int j=1; j<n; j++) {
            place+= ((p[j] - p[i]) * fact(n-));
            cout<<place;
            break;
        }
        break;
    }

}


#include <vector>
#include <iterator>
#include <algorithm>
#include <iostream>

int fact(int n) {
    if (n<2) {
        return 1;
    }
    return n * fact(n-1);
}
using namespace std;
int main()
{
    int n = 0;
    cin >> n;

    vector<int> p;
    copy_n(istream_iterator<int>(cin), n, back_inserter(p));

    int n_prev = 0;

    for (auto it = p.begin(); it + 1 != p.end(); ++it)
    {
        int n_local_prev =
                count_if(it + 1, p.end(), [it](int v) { return v < *it; });
        n_prev += n_local_prev * fact(p.end() - it - 1);
    }

    cout << n_prev + 1 << endl;
}


#include <iostream>
using namespace std;

int main() {
    int n;
    cin>>n;
    int* p=new int[n];
    for(int i=0;i<n;i++){cin>>p[i];}
    int* fact=new int[n];
    fact[0]=1;
    for(int i=1;i<=n;i++){fact[i]=fact[i-1]*i;}

    int res=0;
    for(int i = 1; i <= n; i++){
        int inv=0;
        for(int j = i + 1; j <= n; j++)
            if (p[j] < p[i]) inv++;
        res += inv * fact[n-i];
    }
cout<<res+1;

}

#include <iostream>
using namespace std;
void swap(int *a, int i, int j)
{
    int s = a[i];
    a[i] = a[j];
    a[j] = s;
}
bool NextSet(int *a, int n)
{
    int j = n - 2;
    while (j != -1 && a[j] >= a[j + 1]) j--;
    if (j == -1)
        return false; // больше перестановок нет
    int k = n - 1;
    while (a[j] >= a[k]) k--;
    swap(a, j, k);
    int l = j + 1, r = n - 1; // сортируем оставшуюся часть последовательности
    while (l<r)
        swap(a, l++, r--);
    return true;
}
void Print(int *a, int n)  // вывод перестановки
{
    static int num = 1; // номер перестановки
    cout.width(3); // ширина поля вывода номера перестановки
    cout << num++ << ": ";
    for (int i = 0; i < n; i++)
        cout << a[i] << " ";
    cout << endl;
}
int main()
{
    int n, *a;
    cout << "N = ";
    cin >> n;
    a = new int[n];
    for (int i = 0; i < n; i++)
        a[i] = i + 1;
    Print(a, n);
    while (NextSet(a, n))
        Print(a, n);
    cin.get(); cin.get();
    return 0;
}
*/