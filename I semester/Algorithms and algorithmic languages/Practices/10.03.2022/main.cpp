# include <iostream>
# include <fstream>
# include <cmath>
# include <cstdlib>
# include <cstring>
# include <stack>
using namespace  std;

struct E
{
    int info;	// data
    E * next;
    E (int pinfo, E * pnext=nullptr)
    { info = pinfo, next = pnext; }
    void Print () { cout << info << " "; }
};

class List {
    E *first, *last;
public:
    List() { first = nullptr, last = nullptr;}
    ~List();
    void AddBegin(int);
    void AddEnd(int);

    E* Find (int);
    void DeleteFirst();
    void DeleteLast();
    void Sort();
    friend ostream & operator<<(ostream &, List &);
    bool Delete (int);
    void Reverse ();
};

ostream & operator<<(ostream & pos, List & L){
    for (E*p=L.first; p!= nullptr; p=p->next ) {
        p->Print();
    }
    pos<<endl;
    return pos;
}

int main() {
    setlocale(LC_ALL, "ru");
    List L;
    L.AddEnd(3);    L.AddBegin(9);
    L.AddEnd(7);    L.AddBegin(5);
    L.AddEnd(33);   L.AddBegin(99);
    L.AddEnd(77);   L.AddBegin(55);

    L.Find(33);

    cout<<L;

    cout<<L.Find(99)->info<<endl;   //???
  //  L.Find(99)->Print();            //???
    cout<<endl;

    L.DeleteLast();
    cout<<L;

    L.Delete(9);
    cout<<L;



    L.Sort(); cout<<L;

    L.Reverse(); cout<<L;
    return 0;
}

List::~List(){
    for (E*p=first, *q; p!= nullptr; p=q){
        q=p->next;
        delete p;
    }
    cout<<endl<<"deleted";
}

void List::AddBegin(int pinfo){
    first = new E(pinfo, first);
    if ( last == nullptr ) {
        last = first;
    }
}

void List::AddEnd(int pinfo) {
    if (first==nullptr) {
        first = last = new E(pinfo);
    }
    else {
        last = last->next = new E(pinfo);
    }
}

E*List::Find(int pinfo){
    for(E*p=first; p!= nullptr; p=p->next){
        if (p->info==pinfo){
            return p;
        }
    }
    return nullptr;
}

void List::DeleteFirst() {
    if (first!=nullptr) {
        E*q=first->next;
        delete q;
        first = q;
        first=first->next;
    }

}

void List::DeleteLast() { //придётся пробегаться по списку с начала, чтобы передвинуть указать последнего элемента на предпоследний элемент
    if (first==nullptr){
        return;
    }
    if (first->next==nullptr) {
        delete first;
        first=last= nullptr;
        return;
    }
    E*p=first;
    for( ; p->next != last ; p=p->next){
        ;
    }
    delete p->next;
    p->next= nullptr;
    last=p;
}

void List::Sort(){
    if ((first= nullptr) || (first->next == nullptr)){
        return;
    }
    for (E*p=first; p!= nullptr; p=p->next){
        for (E*q=first; q->next!= nullptr; q=q->next){
            if (q->info > q->next->info){
                swap (q->info, q->next->info);
            }
        }
    }
}

bool List::Delete(int pinfo){
    if (first==nullptr){
        return false;
    }
    if (first->next== nullptr){
        if (first->info==pinfo){
           DeleteFirst();
           return true;
        }
    }

    for(E*p=first, *q; p!= nullptr; p=p->next){
        if (p->info == pinfo) {
            q=p->next->next;
            delete p->next;
            p->next = q;
            return true;
        }
    }
    return false;
}

void List::Reverse() {
    stack <int> st;
    for(E*p=first, *q; p!= nullptr; p=p->next) {
        st.push(p->info);
    }
    for(E*p=first, *q; p!= nullptr; p=p->next){
        p->info =st.top();
        st.pop();
    }
}