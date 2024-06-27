#include <iostream>
#include <queue>
#include <stack>
#include <ctime>
using namespace std;


class Tree{

    struct Node{
        int info;
        Node* left;
        Node* right;
        Node (int info){
            this->info=info;
            left=right= nullptr;
        }
    };

    Node* main_root;

    void levelOrderPrint(Node* main_root);
    void Add(int);
private:
    void Add(int info, Node*& main_root);

};


void Tree::levelOrderPrint(Node *main_root) {
    if (main_root= nullptr) { return; }
    queue<Node *> q; // Создаем очередь
    q.push(main_root); // Вставляем корень в очередь

    while (!q.empty() ) // пока очередь не пуста
    {
        Node* temp = q.front(); // Берем первый элемент в очереди
        q.pop();  // Удаляем первый элемент в очереди
        cout << temp->info << " "; // Печатаем значение первого элемента в очереди

        if ( temp->left != NULL )
            q.push(temp->left);  // Вставляем  в очередь левого потомка

        if ( temp->right != NULL )
            q.push(temp->right);  // Вставляем  в очередь правого потомка
    }

}

void Tree::Add(int info) {
    Add(info, main_root);
}

void Tree::Add(int info, Node*& main_root){
    // если поддерево пустое, создаем единственный узел (адрес сохранится в переменной, ссылка на которую передана в качестве параметра)
    if(main_root==NULL){
        main_root = new Node(info); return;
    }
    // если значение должно быть в левом поддереве
    if(main_root->info > info)
        // добавляем значение в левое поддерево
        Add(info, main_root->left);

    else
        // добавляем значение в правое поддерево
        Add(info, main_root->right);
}








int main() {
    setlocale(LC_ALL, "ru");
    std::srand(std::time(nullptr));
    Tree t;

    int a[10]={1,2,3,4,5,6,7,8,9,10};
    for (int i=0; i<10; i++){

    }

    return 0;
}
