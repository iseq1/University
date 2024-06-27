#include <iostream>
using namespace std;

class List{
    struct Node{
        int info;                             //Значение info будет передаваться в список
        Node *next, *prev;                 //Указатели на адреса следующего и предыдущего элементов списка
    };
    Node *head, *tail;                 //Указатели на адреса начала списка и его конца
public:
    List();    //Инициализируем адреса как пустые
    ~List();                           //Прототип деструктора
    void Print();                       //Прототип функции отображения списка на экране
    void Add(int info);                   //Прототип функции добавления элементов в список
    //методы для 2 задачи ->
    void IsSim();
    int Size();
    //методы для 2 задачи <-
};

List::List(){
    head=tail= nullptr;
}

List::~List(){
    while (head)                       //Пока по адресу на начало списка что-то есть
    {
        tail = head->next;             //Резервная копия адреса следующего звена списка
        delete head;                   //Очистка памяти от первого звена
        head = tail;                   //Смена адреса начала на адрес следующего элемента
    }
}



//методы для 2 задачи ->

int List::Size(){
    int size=0;
    if(head==tail){
        size=0;
    }
    else{
        for(Node* cur=head; cur!= nullptr; cur=cur->next){
            size++;
        }
    }
    return size;
}

void List::IsSim() {
    int k=0;
    Node* curh=head;
    Node* curt=tail;
    for(int i=0; i<(Size()/2); i++){
        if(curh->info == curt->info){
            k++;
        }
        curh->next; curt->prev;
    }

    if(k==Size()/2) cout<<"Symmetrical"<<endl;
    else cout<<"not symmetrical!"<<endl;
}

//методы для 2 задачи <-











void List::Add(int info) {
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
//ВЫВОДИМ СПИСОК С КОНЦА
    Node *temp=tail;                   //Временный указатель на адрес последнего элемента

    while (temp != nullptr)               //Пока не встретится пустое значение
    {
        cout << temp->info << " ";        //Выводить значение на экран
        temp = temp->prev;             //Указываем, что нужен адрес предыдущего элемента
    }
    cout << "\n";

    //ВЫВОДИМ СПИСОК С НАЧАЛА
    temp = head;                       //Временно указываем на адрес первого элемента
    while (temp != nullptr)              //Пока не встретим пустое значение
    {
        cout << temp->info << " ";        //Выводим каждое считанное значение на экран
        temp = temp->next;             //Смена адреса на адрес следующего элемента
    }
    cout << "\n";
}

int main ()
{

    List lst; //Объявляем переменную, тип которой есть список
    lst.Add(100); //Добавляем в список элементы
    lst.Add(200);
    lst.Add(300);
    lst.Add(200);
    lst.Add(100);

    lst.Print(); //Отображаем список на экране

    lst.IsSim();

    return 0;
}