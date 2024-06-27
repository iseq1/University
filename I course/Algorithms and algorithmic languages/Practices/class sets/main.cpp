#include <iostream>

using namespace std;

class Set {
    int *mas,k; //массив, кол-во элементов в массиве
    void Add(int); //Добавить элемент
    void Sub(int); //Удалить элемент
public:
    Set():k(0),mas(new int[0]) {};
    Set(const Set &);
    ~Set() {delete[]mas;};             //Деструктор
    void operator+=(int n) {Add(n);};  //Добавить к множеству n-ый элемент
    void operator+=(Set &);            //Объединение двух множеств
    void operator-=(int n) {Sub(n);};  //Удалить из множества n-ый элемент
    void operator-=(Set &);            //Разность двух множеств
    void operator*=(Set &);            //Пересечение двух множеств
    friend bool operator==(Set &, Set &);   //Проверка на равенство
    friend bool operator<=(Set &, Set &);   //Проверка на больше/меньше
    friend ostream& operator<<(ostream &, const Set &);
    friend istream& operator>>(istream &s, Set &);
    int Quantity() {return k;};              //Количество элементов в множестве
};

Set::Set(const Set &x):k(x.k),mas(new int[k])
{
    for(int i=0;i<k;i++)
        mas[i]=x.mas[i];
}

void Set::Add(int n)
{
    int *t,pos;
    for(pos=0;pos<k && mas[pos]<n;pos++) {}
    if (mas[pos]!=n)
    {
        t=new int[++k];
        for(int i=0;i<k-1;i++)
            t[i<pos?i:i+1]=mas[i];
        t[pos]=n;
        delete[]mas;
        mas=t;
    }
}

void Set::operator+=(Set &x)
{
    for(int i=0;i<x.k;i++)
        Add(x.mas[i]);
}

void Set::Sub(int n)
{
    if (k>0)
    {
        int *t,pos;
        for(pos=0;pos<k && mas[pos]<n;pos++) {}
        if (mas[pos]==n)
        {
            t=new int[--k];
            for(int i=0;i<k+1;i++)
                if (i!=pos) t[i<pos?i:i-1]=mas[i];
            delete[]mas;
            mas=t;
        }
    }
}

void Set::operator-=(Set &x)
{
    for(int i=0;i<x.k;i++)
        Sub(x.mas[i]);
}

void Set::operator*=(Set &x)
{
    Set t(*this);
    t-=x;
    for(int i=0;i<t.k;i++)
        Sub(t.mas[i]);
}

bool operator==(Set &x, Set &y)
{
    if (x.k!=y.k) return false;
    for (int i=0;i<x.k;i++)
        if (x.mas[i]!=y.mas[i]) return false;
    return true;
}

bool operator<=(Set &x, Set &y)
{
    int s=0;
    for (int i=0;i<x.k;i++)
        while(x.mas[i]!=y.mas[i+s])
        {
            if (x.k+s>y.k) return false;
            s++;
        }
    return true;
}

ostream &operator<<(ostream &s, const Set &p)
{
    s<<"(";
    for (int i=0;i<p.k-1;i++)
        s<<p.mas[i]<<",";
    return s<<p.mas[p.k-1]<<")";
}
istream &operator>>(istream &s, Set &p)
{
    int i;
    char c;
    s>>c;
    for (i=0;i<p.k-1;i++)
    {
        while (c!=')')
            s>> p.mas[p.k-1]>> c;
    }
    return s;

}
int main()
{
    Set a,b,c; cin>>a;
    a+=2; a+=4; a+=6; a+=10; cout<<"A: "<<a<<endl;
    b+=3; b+=5; b+=7; b+=10; cout<<"B: "<<b<<endl;
    a+=b; cout<<"A+B: "<<a<<endl;
    a-=b; cout<<"A-B: "<<a<<endl;
   // b*=a; cout<<a<<endl;

    if (a==b){
        cout<<"A==B"<<endl;
    }
    else{ cout<<"A!=B"<<endl;}

    if (a<=b) {
        cout<<"A<=B"<<endl;
    }
    else {cout<<"A>B"<<endl;}

    cout<<"Length A: "<<a.Quantity()<<endl<<"Length B: "<<b.Quantity();
    return 0;
}