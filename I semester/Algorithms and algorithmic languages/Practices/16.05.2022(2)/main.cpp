# include <iostream>
# include <queue>
using namespace std;
int cut=0;
const int INF = 2000000002;

class Node
{
    int info;
    Node * left = nullptr, * right=nullptr, * parent = nullptr;
public :
    Node (int pinfo, Node * pparent = nullptr, Node * pleft = nullptr, Node * pright=nullptr)
    {
        info = pinfo, left = pleft, right = pright, parent = pparent;
    }
    friend class Tree;
};

class Tree
{
    Node * root = nullptr;
public :
    ~Tree () { }

    friend ostream & operator << (ostream &, Tree &);
    void Append (int);
    void Print ();
    int Simetric(int);


    bool operator == (Tree &);
    void AppendL (int);
    void PrintN ();

private :
    int Simetric(int,Node *);
    void Print (Node *);
    void Append (int, Node * &);



};

int main ()
{
    Tree t;

    t.Append (5);
    t.Append (15);
    t.Append (1);
    t.Append (2);
    t.Append (-1);
    t.Append (0);
    t.Append (11);
    t.Append (22);
    t.Append (23);

    cout << t;

    t.Print ();


    int ny=0;
    ny=t.Simetric(5);
    if (ny==0) cout<<" the tree is symmetrical ";
    else cout<<"the tree is not symmetrical";

    return 0;
}

void Tree::Print ()
{
    if ( root == nullptr )
    {
        cout << "[ ]" << endl;
        return;
    }
    queue <Node *> q;
    cout << "[";
    q.push (root);
    while ( ! q.empty () )
    {
        Node * r = q.front (); q.pop ();
        cout << " " << r->info;
        if ( r->left != nullptr )
            q.push (r->left);
        if ( r->right != nullptr )
            q.push (r->right);
    }
    cout << " ]" << endl;
}

void Tree::Append (int pinfo)
{
    Append (pinfo, root);
}

void Tree::Append (int pinfo, Node * & r)
{
    if ( r == nullptr )
    {
        r = new Node (pinfo, r);
        return;
    }

    if ( r->info == pinfo )
        return;

    if ( r->info < pinfo )
        Append (pinfo, r->right);
    else
        Append (pinfo, r->left);
}

ostream & operator << (ostream & pos, Tree & t)
{
    pos << "{";
    t.Print (t.root);
    pos << " }" << endl;
    return pos;
}

void Tree::Print (Node * r)
{
    if ( r != nullptr )
    {
        Print (r->left);
        cout << " " << r->info;
        Print (r->right);
    }
}

int Tree::Simetric(int pinfo){
    return Simetric(pinfo, root);
}

int Tree::Simetric(int, Node *r) {
    if ( r != nullptr )
    {
        if (r->left!= nullptr && r->right!= nullptr){
            cut=cut+0;
        }
        else cut++;
    }
    if (cut==0){
        return 0;
    }
    else return 1;
}