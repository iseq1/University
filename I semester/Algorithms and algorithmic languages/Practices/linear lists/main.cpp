// 07.03.2022

/*
Линейные списки (функции)
- печать списка с циклом и рекурсией
- добавление в начало и в конец

- печать списка в обратном порядке
*/

# include <iostream>
# include <fstream>
# include <cmath>
# include <cstdlib>
# include <cstring>

using namespace std;

struct E
{
    int info;	// data
    E * next;
    E (int pinfo, E * pnext=nullptr)
    { info = pinfo, next = pnext; }
    void Print () { cout << info << " "; }
};

int Print (E *);
int PrintR (E *);
void PrintBack (E *);
void AddFirst (E * &, E * &, int);
void AddLast (E * &, E * &, int);

int main ()
{
    setlocale (LC_ALL, "RUS");

    E * first = NULL, * last = 0;	// создали пустой линейный список
/*
	last = first = new E (7);	// добавили в список элемент 7

	last = first->next = new E (11);	// добавить в конец элемент 11

	first = new E (3, first);	// добавить в начало элемент 3

	//first->next->next->next = new E (17, nullptr);	// добавить в конец элемент 17
	last->next = new E (17, nullptr);
	last = last->next;

	first->next = new E (5, first->next);	// добавить новый элемент 5 сразу после первого
*/
    // распечатать список от начала до конца
/*
	cout << "kol-vo = " << Print (first) << endl;

	Print (first->next);

	last->Print ();
*/

    AddFirst (first, last, 7);
    AddFirst (first, last, 5);
    AddFirst (first, last, 3);
    AddLast (first, last, 11);
    AddLast (first, last, 17);

    PrintR (first);
    PrintBack (first);

    return 0;
}

void AddLast (E * & pfirst, E * & plast, int pinfo)
{
    if ( pfirst == nullptr )
        pfirst = plast = new E (pinfo);
    else
    {
        plast->next = new E (pinfo);
        plast = plast->next;
    }
}

void AddFirst (E * & pfirst, E * & plast, int pinfo)
{
    pfirst = new E (pinfo, pfirst);
    if ( plast == nullptr )
        plast = pfirst;
}

int PrintR (E * pfirst)
{
    if ( pfirst != nullptr )
    {
        pfirst->Print ();
        return PrintR (pfirst->next) + 1;
    }
    else
    {
        cout << endl;
        return 0;
    }
}

void PrintBack (E * pfirst)
{
    if ( pfirst != nullptr )
    {
        PrintBack (pfirst->next);
        pfirst->Print ();
    }
}

int Print (E * pfirst)
{
    int kol = 0;
    for ( E * p=pfirst; p != nullptr; p=p->next, kol++ )
        p->Print ();
    cout << endl;
    return kol;
}

