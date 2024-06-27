#include <iostream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <cstring>
using namespace std;

// #include "Node.HPP"
class Node{

    int info;
    Node *left, *right, *parent;
public:
    Node (int pinfo, Node*pparent= nullptr, Node *pleft= nullptr, Node *pright= nullptr) {
        info=pinfo, left=pleft, right=pright;
    }

    int GetInfo(){
        return info;
    }
    Node* GetLeft(){
        return left;
    }
    Node* GetRight(){
        return right;
    }

    void SetLeft(Node*pleft){
        left=pleft ;
    }
    void SetRight(Node*pright){
        right=pright;
    }
    friend class Tree;
};



// #include "Tree.HPP"
class Tree{
    Node *root = nullptr;
public:
//  Tree();
    ~Tree();
    friend ostream&operator<<(ostream&,Tree&);
    void Append(int);
    void Append(int,Node*);
};

void Tree::Append(int pinfo){
    Append(pinfo,root);
}

void Tree::Append(int pinfo, Node*r){
    if (r== nullptr)
        r=new Node(pinfo, r);
    else if (r->GetInfo()==pinfo)
        return;
    if (r->info->pinfo)
        Append(pinfo,r->left);
    else
        Append(pinfo, r->right);
}

void PrintTree(Node*);
int MaxRoot(Node*);

int main() {
    setlocale(LC_ALL, "ru");

    Node *root= nullptr;
    root=new Node(111);

    /*
    root->left=new Node(10);
    root->left->right=new Node(15);
    root->left->left=new Node(5);
    root->left->right->right=new Node(33);
     */

    root->SetLeft(new Node(10, root));
    root->GetLeft()->SetRight(new Node(15,root->GetLeft()));
    root->GetLeft()->SetLeft(new Node(5,root->GetLeft()));
    root->GetLeft()->GetRight()->SetLeft(new Node(33,root->GetLeft()->GetRight()));
    PrintTree(root);
    cout<<endl;

   // PrintTree(root->GetLeft());    //PrintTree(root->left);
   // cout<<endl;

    cout<<MaxRoot(root);
    cout<<endl;

    Tree t;
    t.Append(111);
    t.Append(10);
    t.Append(15);
    t.Append(3);
    t.Append(33);
    t.Append(50);

    return 0;
}

// существует уйма способов вывода дерева в консоль, разберём один из них:
void PrintTree(Node *rt) {
    if(rt!= nullptr){
        //прямой обход дерева: Left -> Root -> Right
        // example: 5(L) 10(Rt) 15(Right) 33(Right) 111(Root)
        PrintTree(rt->GetLeft());    //со struct было PrintTree(rt->left);
        cout<<rt->GetInfo()<<" ";   //со struct было  cout<<rt->info()<<" ";
        PrintTree(rt->GetRight());  //PrintTree(rt->right());
    }
}

//Наибольшей корень дерева
int MaxRoot(Node *rt){
    if(rt== nullptr)
        return -11111;
    else{
        return max(rt->GetInfo(), max(MaxRoot(rt->GetLeft()), MaxRoot(rt->GetRight())));
    }
}