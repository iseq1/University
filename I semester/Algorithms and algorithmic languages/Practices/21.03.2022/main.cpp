#include <iostream>
#include <queue>
using namespace std;

class Queue{
    struct Node {
        int info;
        Node* next;
        Node (int info){this->info=info; next=nullptr;}
    };
    Node* head, *tail;
public:
    Queue();

    ~Queue(); // деструктор

    bool Empty(); // проверка на пустоту очереди

    void Push(int info); // добавление в очередь элемента

    int Pop(); // извлечение элемента из очереди

    int Size(); // Вывод длины очереди

    int Front(); // Вывод первого элемента очереди

    int Back(int num); // Вывод последнего элемента очереди
};


// инициализация пустой очередиx
Queue::Queue() {
    head=tail=nullptr;
}


// удаление всех оставлшихся оставшихся элементов - пока очередь не пуста, извлекаем очередной элемент
Queue::~Queue() {
    while(!Empty())
        Pop();
}


bool Queue::Empty() {
    return head==NULL;
}


void Queue::Push(int info) {
    // добавление элемента в очередь
    // при добавлении в пустую очередь надо сформировать единственный элемент очереди
    if(Empty()) {
        head = tail = new Node(info);
    }
    else {
    // добавление в конец очереди
        tail->next=new Node(info);
        tail=tail->next;
    }
}

int Queue::Pop() {
    if(Empty()) throw 1;
    int res=head->info;
    Node*help = head;
    head=head->next;
    delete help;
// отдельная обработка извлечения единственного элемента очереди
    if(head==NULL) tail=NULL;
    return res;
}


int Queue::Size() {
    if(Empty()) throw 1;
    cout<<"Дана очередь: < "; int k=0;
    for(Node*cur=head; cur!=NULL; cur=cur->next) {
        cout << (cur->info) << " ";
        k++;
    }
    cout<<" >"<<endl<<"Её длинна составляет: "<<k<<endl;
    return 0;
}

int Queue::Front() {
    if(Empty()) throw 1;
    else {
        cout << "Первый элемент очереди: ";
        int k=0;
        for (Node *cur = head; cur != NULL; cur = cur->next) {
            k++;
            if (k==1){
            cout << (cur->info) << " ";
            }
        }
        cout << endl;
    }
    return 0;
}


int Queue::Back(int num) {
    if(Empty()) throw 1;
    else {
        cout << "Последний элемент очереди: ";
        int k=0;
        for (Node *cur = head; cur != NULL; cur = cur->next) {
            k++;
            if (k==num){
                cout << (cur->info) << " ";
            }
        }
        cout << endl;
    }
    return 0;
}


int main() {
    setlocale(LC_ALL, "rus");
    try {
        Queue q; cout<<"Введите длинну вашей очереди:"<<endl; int num; cin>>num;
        cout<<"Вводите элементы: "<<endl;
        for (int i = 0; i < num; i++) {
            int a;
            cin>>a;
            q.Push(a);
        }

        // q.Push(1), q.Push(5), q.Push(9); Второй вариант ввода очереди

        q.Size();

        q.Front();

        q.Back(num);

        while (!q.Empty()) {
            q.Pop();
        }
        cout << "Ваша очередь  безвозвратно удалена";
    }
    catch(int error) {
        cout<<"Ваша очередь абслолютно пуста!";
    }
}
