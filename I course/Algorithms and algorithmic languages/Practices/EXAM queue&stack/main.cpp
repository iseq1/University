#include <iostream>
#include <queue>
#include <stack>
using namespace std;

// очередь - частный случай линейной структуры данных, для которой удобно использование односвязного списка
// работает по принципу FIFO - первый пришел, первый ушел
// причины - динамически меняет размер, требуется доступ только к двум концам, поэтому операции минимальны по трудоемкости


class Queue{
    struct Node{
        int info;
        Node* next;
        Node(int info)
        {this->info=info; next=nullptr;}
    };
    Node*head,*tail;
public:
    Queue();
    ~Queue();
    void Print();
    bool IsEmpty();
    void Push(int info);
    int Peek();
    int Pop();
};

Queue::Queue(){
    head=tail=nullptr;
}

Queue::~Queue(){
    if(!IsEmpty())
        Pop();
}

void Queue::Print(){
    cout<<"{ ";
    for(Node *cur=head; cur!= nullptr; cur=cur->next){
        cout<<(cur->info)<<" ";
    }
    cout<<"}"<<endl;
}

bool Queue::IsEmpty() {
    return head==nullptr;
}

void Queue::Push(int info) {
    if(IsEmpty()){
        head=tail=new Node(info);
    }
    else{
        tail->next=new Node(info);
        tail=tail->next;
    }
}

int Queue::Peek(){
    if(IsEmpty()) throw 1;
    return head->info;
}

int Queue::Pop(){
    if(IsEmpty()) throw 1;
    int res=head->info;
    Node* help=head;
    head=head->next;
    delete help;
    if(head==nullptr) tail=nullptr;
    return res;
}


// класс стек - принцип LIFO - последний пришел, первый ушел
// конструктору требуются уже оба параметра, так как будет работать только с одним концом
// удобным концом для этого является начало списка

class Stack{
    struct Node{
        int info;
        Node*next;
        Node(int info, Node*next)
        {this->info=info; this->next=next;}
    };
    Node*head;
public:
    Stack();
    ~Stack();
    void Print();
    bool IsEmpty();
    void Push(int info);
    int Peek();
    int Pop();
};

Stack::Stack() {
    head= nullptr;
}

Stack::~Stack(){
    while(!IsEmpty()){
        Pop();
    }
}

void Stack::Print(){
    cout<<"[ ";
    for(Node*cur=head; cur!= nullptr; cur=cur->next){
        cout<<(cur->info)<<" ";
    }
    cout<<"]"<<endl;
}

bool Stack::IsEmpty() {
    return head== nullptr;
}

void Stack::Push(int info){
    head=new Node(info, head);
}

int Stack::Peek(){
    if(IsEmpty()) throw 1;
    return head->info;
}

int Stack::Pop(){
    if(IsEmpty()) throw 1;
    int res=head->info;
    Node*help=head;
    head=head->next;
    delete help;
    return res;
}

int main() {
    setlocale(LC_ALL, "ru");
    Queue q;

    for(int i=0;i<10;i++){
        q.Push(i);
    }
    q.Print();
    cout<<"Очередь"<<endl;
    while(!q.IsEmpty())
        cout<<q.Pop()<<" ";
    cout<<endl<<endl<<endl;

    Stack s;
    for(int i=0;i<10;i++){
        s.Push(i);
    }
    s.Print();
    cout<<"Стек"<<endl;
    while(!s.IsEmpty())
        cout<<s.Pop()<<" ";

    return 0;
}
