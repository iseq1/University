#include <iostream>
using namespace std;

class List {

    struct Node {
        int info;
        Node*next;
        Node(int info, Node*next=nullptr) {
            this->info=info; this->next=next;
        }

    };

    Node*head;

public:
    List();
    ~List();
    void Add(int info, int position);
    void Remove(int p);
    void Print();

};

List::List() {
    head=nullptr;
}

List::~List() {
    while(head!= nullptr) { //запоинаем указатель в вспомогательную переменную и удаляем поэлементно лин.список
        Node* help=head;
        head=head->next;
        delete help;
    }
}

void List::Add(int info, int position) {
    if(position==0) {
        head = new Node(info, head);
        return ;
    }
    if(position<0) throw 1;
    Node*cur=head;
    int i=0;
    while(i!=position-1 && cur!=nullptr){
        i++;
        cur=cur->next;
    }
    if(cur==nullptr) throw 1;
    cur->next=new Node(info, cur->next);

}

void List::Remove(int p) {

}

void List::Print() {
    cout<<"(";
    for (Node*cur=head; cur!= nullptr; cur=cur->next) {
        cout<<(cur->info)<<" ";
    }
    cout<<")"<<endl;
}

int main() {
    setlocale(LC_ALL, "ru");

    List list;
    for(int i=0; i<5; i++) {
        list.Add(i,i);
    }
    list.Add(100,0);
    list.Add(600,6);
    list.Add(1000, 3);
    list.Print();
    return 0;
}
