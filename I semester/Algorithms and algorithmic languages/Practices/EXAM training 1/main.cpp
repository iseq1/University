#include <iostream>
using namespace std;

class List{
    struct Node{
        int info;
        Node* next;
        Node(int info, Node* next)
        {this->info=info, this->next=next;}
    };

    Node* head;
public:
    List();
    ~List();
    void Add(int info, int position);
    void Remove(int position);
    void Print();

    //методы для 1 задачи ->
    void AddNewElem();
    int Min();
    int Max();
    //методы для 1 задачи <-

private:
    void RemoveNode(Node*& node);

};







int List::Min(){
    int temp=10000;
    for(Node*cur=head; cur!= nullptr; cur=cur->next){
        if((cur->info)<temp) {
            temp=(cur->info);
        }
    }
    return temp;
}

int List::Max(){
    int temp=0;
    for(Node*cur=head; cur!= nullptr; cur=cur->next){
        if((cur->info)>temp) {
            temp=(cur->info);
        }
    }
    return temp;
}

void List::AddNewElem() {
    int temp_max=Max();
    int temp_elem=((Max()+Min())/2);
    for(Node*cur = head; cur!= nullptr; cur=cur->next){
        if (cur->info==temp_max){
            cur->next=new Node(temp_elem, cur->next);
        }
    }
}












void List::RemoveNode(Node*& node){
    Node* help=node;
    node=node->next;
    delete help;
}

// конструктор списка только инициализирует заголовок, указывая, что список будет пустым
List::List(){
    head= nullptr;
}

// деструктор должен уничтожить все элементы списка
List::~List(){
    while(head!= nullptr){
        RemoveNode(head);
    }
}

void List::Add(int info, int position){
    if (position==0){
        head=new Node(info, head);
        return;
    }
    if (position<0) throw 1;

    Node* cur=head;
    int i=0;
    while(i!=position-1 && cur!= nullptr){
        i++; cur=cur->next;
    }
    if(cur== nullptr) throw 1;
    cur->next=new Node(info, cur->next);
}

void List::Remove(int position){
    if(head== nullptr) throw 1;
    if(position==0){
        RemoveNode(head);
        return;
    }
    if(position<0) throw 1;

    Node *cur=head;
    int i=0;
    while(i!=position-1 && cur->next!= nullptr){
        i++; cur=cur->next;
    }
    if(cur->next==nullptr) throw 1;
    RemoveNode(cur->next);
}

void List::Print(){
    cout<<"[ ";
    for(Node*cur = head; cur!= nullptr; cur=cur->next){
        cout<<(cur->info)<<" ";
    }
    cout<<"]"<<endl;
}



int main() {
    List list;
    for(int i=0; i<6; i++){
        list.Add(i,i);
    }
    list.Print();

    list.Remove(5);
    list.Add(15,5);
    list.Print();



    list.AddNewElem();
    list.Print();


    return 0;
}
