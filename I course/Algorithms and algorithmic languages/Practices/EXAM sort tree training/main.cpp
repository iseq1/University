#include <iostream>
using namespace std;

class Tree{
    struct Node{
        int info;
        Node* left;
        Node* right;
        Node(int info)
        {this->info=info;  left=right= nullptr;}
    };
    Node* main_root;


public:

    Tree();
    void Add1(int info);
    void Add2def(int info);
    void PrintPref();
    void PrintInf();
    void PrintPost();

private:
    void Add2def(int info, Node*& root);
    void PrintPref(Node*root);
    void PrintInf(Node*root);
    void PrintPost(Node*root);
};

Tree::Tree(){
    main_root= nullptr;
}



void Tree::Add1(int info) {
    if(main_root== nullptr){
        main_root=new Node(info); return;
    }
    Node*cur=main_root;
    while (true) {
        if(cur->info > info) {
            if (cur->left!= nullptr){
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

void Tree::Add2def(int info) {
    Add2def(info, main_root);
}

void Tree::Add2def(int info, Node *&root) {
    if (root== nullptr){
        root=new Node(info); return;
    }
    if (root->info>info){
        Add2def(info,root->left);
    }
    if(root->info<info){
        Add2def(info,root->right);
    }
}

void Tree::PrintPref() {
    Node*root=main_root;
    PrintPref(root);
}

void Tree::PrintPref(Node *root) {
    if (root== nullptr) return;
    cout<<root->info<<" ";
    PrintPref(root->left);
    PrintPref(root->right);
}

void Tree::PrintInf() {
    Node*root=main_root;
    PrintInf(root);
}

void Tree::PrintInf (Node *root) {
    if (root== nullptr) return;
    PrintInf(root->left);
    cout<<root->info<<" ";
    PrintInf(root->right);
}

void Tree::PrintPost() {
    Node*root=main_root;
    PrintPost(root);
}

void Tree::PrintPost(Node *root) {
    if (root== nullptr) return;
    PrintPost(root->left);
    PrintPost(root->right);
    cout<<root->info<<" ";
}


int main() {
    Tree tree; Tree wood;
    int mas[]={5,1,2,8,7,6,3,4,9,10};
    for(int i=0; i<10;i++){
        tree.Add1(mas[i]);
        wood.Add2def(mas[i]);
    }
    tree.PrintPost();
    cout<<endl;
    tree.PrintInf();
    cout<<endl;
    tree.PrintPref();
    cout<<endl;
    return 0;
}
