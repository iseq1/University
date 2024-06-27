#include <iostream>
using namespace std;

/*
класс односвязаного списка - динамической структуры данных, в которой каждый элемент списка хранится
в отдельной памяти. Для связи элементов списка необходимо вместе с элементом хранить информацию о местоположении
(указателе) следующего элемента списка
*/

// структуру хранения размещаем внутри класса List, чтобы во-первых иметь возможность работать с данными узла списка напрямую,
// во-вторых, поскольку таким образом структура узла списка будет скрыта от внешнего использования, так как
// структура узла предназначена специально для реализации односвязного списка

// https://www.bestprog.net/ru/2022/02/11/c-linear-singly-linked-list-general-information-ru/

class List{
    struct Node{
        int info;
        Node* next;
        Node(int info, Node* next)
        {this->info=info, this->next=next;}
    };
    // доступ ко всем элементам списка доступен через его первый элемент - заголовок списка
    Node* head;
public:
    List();
    ~List();
    void Add(int info, int position);
    void Remove(int position);
    void Print();

private:
    void RemoveNode(Node*& node);
};

// вспомогательная функция для удаления узла - private, так как раскрывает структуру хранения (доступ к Node)
// адрес удаляемого узла передается как параметр
// параметр передается по ссылке - т.е. в переменную, хранящую адрес удаляемого узла, можно записать адрес другого узла

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
    for(int i=0; i<10; i++){
        list.Add(i,i);
    }
    list.Print();

    list.Remove(5);
    list.Add(15,5);
    list.Print();

    list.Remove(5);
    list.Add(5,5);
    list.Print();

    return 0;
}
