#include <iostream>
using namespace std;
// ВЫВОДИТ МУСОР
class Tree{
    struct Node{
        int info;
        Node*left;
        Node*right;
        Node(int info){
            this->info=info;
            left=right=nullptr;
        }
    };
    Node* main_root;
public:
    Tree();
    // нерекурсивный вариант функции добавления элемента в дерево
    void Add_1(int info);
    // функция-адаптер для рекурсивного варианта функции добавления элемента в дерево
    void Add_2(int info);
    // функция-адаптер для рекурсивного варианта функции печати элементов дерева
    void Print_2();
private:
    // рекурсивные функции являются private-функциями, так как они по сути реализуют алгоритм и объект им нужен как хранилище данных
    // кроме того, параметры рекурсивной функции (ссылка на корень поддерева) фактически нарушают инкаплусяцию в случае видимости извне

    // рекурсивная функция добавления элемента в дерево (поддерево) с корнем root
    void Add_2(int info, Node*& root);
    // рекурсивная функция печати элеметов дерева
    void Print_2(Node* root);
};

Tree::Tree(){
    main_root= nullptr;
}

void Tree::Print_2() {
    if(main_root== nullptr) cout<<"Tree is empty!"<<endl;
    else Print_2(main_root);
}

void Tree::Print_2(Node *root) {
    if (root== nullptr) return;
    Print_2(root->left);
    cout<<(main_root)<<" ";
    Print_2(root->right);
}

void Tree::Add_2(int info) {
    Add_2(info, main_root);
}

void Tree::Add_2(int info, Node *&root) {
    if (root== nullptr) {
        root = new Node(info); return;
    }
    if (root->info>info) {
        Add_2(info,root->left);
    }
    else {Add_2(info,root->right); }
}

void Tree::Add_1(int info) {
    if(main_root==nullptr){
        main_root=new Node(info); return;
    }
    Node* cur=main_root;
    while (true){
        if(cur->info >info){
            if(cur->left!= nullptr){
                cur=cur->left;
            }
            else{
                cur->left=new Node(info); return;
            }
        }
        else{
            if(cur->right!= nullptr){
                cur=cur->right;
            }
            else{
                cur->right=new Node(info); return;
            }
        }
    }
}

int main() {
    setlocale(LC_ALL, "ru");

    Tree tree;
    int a[]={7,3,6,8,1,2,4,5,10};
    for(int i=0; i<9; i++){
        tree.Add_2(a[i]);
    }
    tree.Print_2();

    return 0;
}
