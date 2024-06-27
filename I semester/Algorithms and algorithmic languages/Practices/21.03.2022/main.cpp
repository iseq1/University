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

    ~Queue(); // ����������

    bool Empty(); // �������� �� ������� �������

    void Push(int info); // ���������� � ������� ��������

    int Pop(); // ���������� �������� �� �������

    int Size(); // ����� ����� �������

    int Front(); // ����� ������� �������� �������

    int Back(int num); // ����� ���������� �������� �������
};


// ������������� ������ �������x
Queue::Queue() {
    head=tail=nullptr;
}


// �������� ���� ����������� ���������� ��������� - ���� ������� �� �����, ��������� ��������� �������
Queue::~Queue() {
    while(!Empty())
        Pop();
}


bool Queue::Empty() {
    return head==NULL;
}


void Queue::Push(int info) {
    // ���������� �������� � �������
    // ��� ���������� � ������ ������� ���� ������������ ������������ ������� �������
    if(Empty()) {
        head = tail = new Node(info);
    }
    else {
    // ���������� � ����� �������
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
// ��������� ��������� ���������� ������������� �������� �������
    if(head==NULL) tail=NULL;
    return res;
}


int Queue::Size() {
    if(Empty()) throw 1;
    cout<<"���� �������: < "; int k=0;
    for(Node*cur=head; cur!=NULL; cur=cur->next) {
        cout << (cur->info) << " ";
        k++;
    }
    cout<<" >"<<endl<<"Ÿ ������ ����������: "<<k<<endl;
    return 0;
}

int Queue::Front() {
    if(Empty()) throw 1;
    else {
        cout << "������ ������� �������: ";
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
        cout << "��������� ������� �������: ";
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
        Queue q; cout<<"������� ������ ����� �������:"<<endl; int num; cin>>num;
        cout<<"������� ��������: "<<endl;
        for (int i = 0; i < num; i++) {
            int a;
            cin>>a;
            q.Push(a);
        }

        // q.Push(1), q.Push(5), q.Push(9); ������ ������� ����� �������

        q.Size();

        q.Front();

        q.Back(num);

        while (!q.Empty()) {
            q.Pop();
        }
        cout << "���� �������  ������������ �������";
    }
    catch(int error) {
        cout<<"���� ������� ���������� �����!";
    }
}
