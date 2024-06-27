#include <iostream>
#include <queue>
using namespace std;

class Node {
public:
    int info;
    Node *left, *right, *parent;
    Node(int pinfo, Node *pparent = nullptr, Node *pleft = nullptr, Node *pright = nullptr) {
        info = pinfo, left = pleft, right = pright;
    }
};


class Tree{
    Node*root=nullptr;
public:
    ~Tree() { }
    friend ostream&operator << (ostream&, Tree&t);
    void Append (int);
    void Print();
private:
    void Print(Node*);
    void Append (int, Node* );
    Node* Find(int pinfo);
    Node* Find(int pinfo, Node*r);
    int Max();
    int Max(Node*r);
};

Node* Tree::Find (int pinfo){
    return Find(pinfo, root);
}

Node* Tree::Find(int pinfo, Node* r){
    if (r== nullptr || r->info == pinfo) {
        return r;
    }
    if (r->info < pinfo) {

    }
}

int Tree::Max(){
    ;
}

int Tree::Max(Node*r){
    ;
}

void Tree::Append(int pinfo) {
    Append(pinfo, root);
}

void Tree::Append(int pinfo, Node* r) {
    if (r == nullptr) {
        r = new Node(pinfo, r);
    }
    else if (r->info==pinfo){
        return;
    }
    if (r->info < pinfo) {
        Append(pinfo, r->right);
    }
    else {
        Append(pinfo, r->left);
    }
}


int main() {
    Tree t;
  //  t.Append(5);
    //t.Append(15);
    //t.Append(1);
    cout<<t;
    return 0;
}

void Tree::Print(){
    if (root== nullptr){
        cout<<"[ ]"<<endl;
        return;
    }
    queue <Node*> q;
    cout<<"[";
    q.push(root);
    while (!q.empty()) {
        Node*r=q.front(); q.pop();
        cout<<" "<< r->info;
        if (r->left != nullptr)
            q.push (r->left);
        if (r->right != nullptr)
            q.push (r->right);
    }
    cout<<"]";
}


ostream&operator << (ostream& pos, Tree&t){
    pos<<"{ ";
    Print(t.root);
    pos<<" }";
    return pos;
}

void Tree::Print(Node *r) {

}

