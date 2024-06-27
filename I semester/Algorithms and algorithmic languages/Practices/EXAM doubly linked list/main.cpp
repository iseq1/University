#include <iostream>
using namespace std;

class List{
    struct Node{
        int info;
        Node*next;
        Node*prev;
    };
    Node* head;
    Node* tail;

public:
    List();
    ~List();
    void Print();
    void Add(int info);
    void Remove(int info);
    void Search(int info);
    bool IsEmpty();
    void RemoveList();
};

List::List(){
    head=tail=nullptr;
}

List::~List(){
    while (head) {
        tail = head->next;
        delete head;
        head = tail;
    }
}

bool List::IsEmpty() {
    if(head == nullptr){
        return true;
    }
    else return false;
}

void List::Add(int info){
    Node *temp = new Node;               //Выделение памяти под новый элемент структуры
    temp->next = nullptr;                   //Указываем, что изначально по следующему адресу пусто
    temp->info = info;                         //Записываем значение в структуру

    if (head != nullptr)                    //Если список не пуст
    {
        temp->prev = tail;               //Указываем адрес на предыдущий элемент в соотв. поле
        tail->next = temp;               //Указываем адрес следующего за хвостом элемента
        tail = temp;                     //Меняем адрес хвоста
    }
    else //Если список пустой
    {
        temp->prev = nullptr;               //Предыдущий элемент указывает в пустоту
        head = tail = temp;              //Голова=Хвост=тот элемент, что сейчас добавили
    }

}

void List::Print(){
    cout<<"from begin:"<<endl<<"[ ";
    for(Node*cur=head;cur!= nullptr; cur=cur->next){
        cout<<cur->info<<" ";
    }
    cout<<"]"<<endl;
    cout<<"from end:"<<endl<<"[ ";
    for(Node*cur=tail; cur!= nullptr;cur=cur->prev){
        cout<<cur->info<<" ";
    }
    cout<<"]"<<endl;
}

void List::Search(int info){
    int i=1;
    Node*cur=head;
    while(info!=cur->info){
        i++; cur=cur->next;
    }
    cout<<"\""<<info<<"\""<<" has position: "<<i<<endl;
}

void List::Remove(int info) {
    Node* temp=new Node;
    Node* cur=head;
    while(info!=cur->info){
        cur=cur->next;
    }
    (cur->next)->prev=cur->prev;
    (cur->prev)->next=cur->next;
    delete cur;
    cout<<info<<" had delete from list!"<<endl;
}

void List::RemoveList() {
    Node* temp=new Node;
    for(Node*cur=head; cur!= nullptr; cur->next){
        Node* temp=cur;
       delete temp;
    }
}






int main() {
    List l;
    for(int i=0;i<5;i++){
        l.Add(i);
    }
    l.Print();
    cout<<l.IsEmpty()<<endl;
    l.Search(3);
    l.Remove(3); l.Print();
    l.RemoveList(); l.Print();

    return 0;
}
