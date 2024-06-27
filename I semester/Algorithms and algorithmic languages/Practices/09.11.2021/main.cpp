#include <iostream>
using namespace std;
int main() {
    int k=0, r=0;
    char str1[] = "World";
    char str2[] = "Tools";
    for (int i=0; i<sizeof(str1); i++) {
        if (str1[i]==str2[i]) {
            k++;
        }
        else {r++;}
    }
    if (k==sizeof(str1)) {
        cout<<"YES";
    }
    else {cout<<"NO, "<<r<<" razlichiy";}
}
