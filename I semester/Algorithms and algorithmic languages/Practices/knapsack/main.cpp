#include <iostream>
using namespace std;
/*
2. Задача о рюкзаке.
n предметоd
рюкзак V - объем рюкзака
у каждого предмета - c_i - ценность i-ого предмета, v_i - объем предмета
надо найти такой набор предметов, который поместится в рюкзак и будет иметь максимальную ценность
метод динамического программирования
1 предмет - положить?
2 предмет - положить?
.....
n предмет - кладем в зависимости от того, влезает ли он в рюкзак
*/
// функция-адаптер
int Knapsack(int n, int* c, int* v, int V);
// рекурсивная функция
int Knapsack(int n, int* c, int* v, int V, int k);

int main() {
    int n;
    cin >> n;
    int V;
    cin >> V;
    int *c = new int[n];
    int *v = new int[n];
    for (int i = 0; i < n; i++)
        cin >> c[i];
    for (int i = 0; i < n; i++)
        cin >> v[i];
    cout << Knapsack(n, c, v, V);
    delete[] c;
    delete[] v;
}
int Knapsack(int n, int* c, int* v, int V)
{
    return Knapsack(n, c, v, V, n-1);
}
// рекурсивная функция
int Knapsack(int n, int* c, int* v, int V, int k)
{
// явный случай
    if (k==0)
        if (v[0]<=V)
            return c[0];
        else return 0;
    if (v[k]<=V)
    {
        int c1=Knapsack(n, c,v,V, k-1); // не берем
        int c2=Knapsack(n, c,v,V-v[k], k-1)+c[k]; // не берем
        return c1>c2? c1: c2;
    }
    else return Knapsack(n, c,v,V, k-1);
}